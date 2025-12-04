from flask import Flask, render_template, request, jsonify
import os
import traceback
import requests

app = Flask(__name__)

# Mailgun configuration via environment variables
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', '')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', '')
MAIL_FROM = os.environ.get('MAIL_FROM', '')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-test', methods=['POST'])
def send_test():
    try:
        data = request.get_json()
        html_content = data.get('html', '')
        emails_string = data.get('emails', '')
        
        if not html_content or not emails_string:
            return jsonify({
                'status': 'error',
                'message': 'Please provide both HTML code and email address(es)'
            }), 400
        
        # Clean and limit recipients
        email_list = [e.strip() for e in emails_string.split(',') if e.strip()]
        email_list = email_list[:3]
        
        if not email_list:
            return jsonify({
                'status': 'error',
                'message': 'Please provide valid email address(es)'
            }), 400
        
        if not MAILGUN_API_KEY or not MAILGUN_DOMAIN or not MAIL_FROM:
            return jsonify({
                'status': 'error',
                'message': 'Server email configuration is missing.'
            }), 500
        
        sent_count = 0
        errors = []
        
        for email in email_list:
            try:
                response = requests.post(
                    f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
                    auth=("api", MAILGUN_API_KEY),
                    data={
                        "from": MAIL_FROM,
                        "to": email,
                        "subject": "Test Email from MailZap",
                        "html": html_content
                    },
                    timeout=15
                )
                
                if response.status_code == 200:
                    sent_count += 1
                else:
                    errors.append(f"{email}: {response.status_code} {response.text[:100]}")
            
            except Exception as inner_e:
                errors.append(f"{email}: {str(inner_e)}")
        
        if sent_count == 0:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send to all recipients: ' + '; '.join(errors)
            }), 500
        
        message = f"✓ Test email sent successfully to {sent_count} address(es)!"
        if errors:
            message += f" Some addresses failed: {'; '.join(errors)}"
        
        return jsonify({
            'status': 'success',
            'message': message
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Error sending email: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
