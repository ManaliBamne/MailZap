## 1. What MailZap Does (for a user)

- Paste raw HTML email.
- Enter 1–3 email addresses.
- Click “Send Test Email”.
- MailZap uses **Gmail SMTP** from your own machine to send the test.

***

## 2. Files that matter

- `app.py` – Flask backend and email sending logic.
- `templates/index.html` – Frontend form (HTML/CSS/JS).
- `requirements.txt` – Python dependencies.
- `venv/` – Your local virtualenv (not committed).

***

## 3. Local setup steps (for anyone running the code)

1. **Create and activate virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   `requirements.txt` should include at least:

   ```text
   Flask
   Flask-Mail
   ```

3. **Create Gmail app password**

   - Turn on 2‑Step Verification in your Google account.
   - Go to Security → App passwords.
   - Create a new app password (e.g. “MailZap”).
   - Copy the 16‑character password.

4. **Set environment variables for this terminal session**

   **Windows (CMD):**

   ```bash
   set MAIL_USERNAME=yourgmail@gmail.com
   set MAIL_PASSWORD=your_16_char_app_password
   ```

   **macOS / Linux:**

   ```bash
   export MAIL_USERNAME=yourgmail@gmail.com
   export MAIL_PASSWORD=your_16_char_app_password
   ```

***

## 4. How the code works (high level)

### `app.py`

- Configures Gmail SMTP using env vars:

  ```python
  app.config['MAIL_SERVER'] = 'smtp.gmail.com'
  app.config['MAIL_PORT'] = 587
  app.config['MAIL_USE_TLS'] = True
  app.config['MAIL_USE_SSL'] = False
  app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
  app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
  app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME', '')
  ```

- `index()` route renders `index.html`.

- `/send-test` route:

  1. Reads JSON from the frontend: `html` and `emails`.
  2. Validates that both are present.
  3. Splits the emails by comma, trims them, keeps up to 3.
  4. For each email, builds a `Message` and calls `mail.send(msg)`.
  5. Returns a JSON success or error message.
  6. On any exception, logs the traceback and returns an error JSON.

- App entry point:

  ```python
  if __name__ == '__main__':
      app.run(debug=True)
  ```

### `templates/index.html`

- Simple form:
  - `<textarea id="htmlCode">` for HTML.
  - `<input id="testEmails">` for email addresses.
  - “Send Test Email” button.

- JS `sendTest()`:

  1. Reads textarea + input values.
  2. Sends `fetch('/send-test', { method: 'POST', body: JSON.stringify({ html, emails }) })`.
  3. Shows success or error message based on JSON response.

***

## 5. How to run and test

1. Activate venv, set env vars, run:

   ```bash
   python app.py
   ```

2. Visit `http://localhost:5000`.

3. Paste sample HTML:

   ```html
   <h1>MailZap local test</h1><p>If you see this, it worked.</p>
   ```

4. Enter your own Gmail in the email input.

5. Click **Send Test Email**.

6. Check your inbox (and Spam/Promotions).

***

## 6. Notes / limitations

- Intended for **local testing only**, not production sending.
- Depends on Gmail app passwords; if email fails:
  - Re‑generate the app password.
  - Re‑set `MAIL_PASSWORD` in terminal.
- Max 3 recipients per send to avoid abuse.
