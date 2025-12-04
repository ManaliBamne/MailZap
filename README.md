# MailZap – Free HTML Email Testing Tool

MailZap is a lightweight HTML email tester inspired by the now‑retired Litmus PutsMail. It gives email marketers and developers a quick way to send test emails without logging into a heavy platform or setting up full campaigns.

🔗 **Live demo:** https://mailzap-e9en.onrender.com  

---

## What MailZap Does

- Paste your HTML email code into a simple web UI.  
- Enter up to 3 test recipient addresses (comma‑separated).  
- Click **“Send test email”** to send live previews and check layout, links, and basic rendering in real inboxes.  
- See clear success or error messages when something goes wrong (invalid input, send failures, etc.).

The Render‑hosted version uses an email API (not Gmail SMTP) to work around SMTP port blocking on Render’s free tier and to make delivery more reliable.

---

## Tech Stack

- **Frontend:** HTML, CSS (no framework)  
- **Backend:** Python, Flask  
- **Email Sending (Render):** Mailgun HTTP API  
- **Hosting:** Render (free web service)

---

## Running Locally (Quick Overview)

If you want to run MailZap yourself:

1. Clone the repo and create a virtual environment.  
2. Install dependencies from `requirements.txt`.  
3. Set the required environment variables for your email provider (e.g., Mailgun API key, domain, from address).  
4. Run `python app.py` and open `http://localhost:5000`.

(Exact env var names and API details are in `app.py`.)

---

## Notes & Constraints

- The Render deployment is designed for low‑volume testing, not high‑throughput sending.  
- SMTP via Gmail is **not** used on Render, due to blocked ports and provider restrictions; the app relies on an HTTP‑based transactional email API instead.  
- For serious production use, you should:
  - Bring your own verified sending domain.
  - Configure your own email provider and quotas.
  - Add authentication, rate limiting, and logging to match your needs.

---

## Why This Project

MailZap was built to replace a concrete workflow: quickly testing HTML emails after PutsMail was retired. It focuses on the small things that matter in day‑to‑day work-speed, low friction, and honest handling of real infrastructure limits-rather than trying to be a full email platform.
