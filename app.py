from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
import traceback

app = Flask(__name__)

# Email configuration - Gmail SMTP for LOCAL USE
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', '')

mail = Mail(app)

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
        
        email_list = [e.strip() for e in emails_string.split(',') if e.strip()]
        email_list = email_list[:3]
        
        if not email_list:
            return jsonify({
                'status': 'error',
                'message': 'Please provide valid email address(es)'
            }), 400
        
        sent_count = 0
        for email in email_list:
            msg = Message(
                subject='Test Email from MailZap',
                recipients=[email],
                html=html_content
            )
            mail.send(msg)
            sent_count += 1
        
        return jsonify({
            'status': 'success',
            'message': f'✓ Test email sent successfully to {sent_count} address(es)!'
        })
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            'status': 'error',
            'message': f'Error sending email: {str(e)}'
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
