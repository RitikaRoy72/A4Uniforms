"""
mailer.py — email sending for password reset.

Configure via environment variables (or a .env file with python-dotenv):

    MAIL_SERVER   smtp.gmail.com          (default)
    MAIL_PORT     587                     (default)
    MAIL_USE_TLS  true                    (default)
    MAIL_USERNAME your@email.com
    MAIL_PASSWORD your-app-password
    MAIL_FROM     Det520 Uniforms <your@email.com>   (optional)

If MAIL_USERNAME is not set the app still runs but sending will fail
gracefully with a logged warning rather than a crash.
"""

import os
from flask_mail import Mail, Message

mail = Mail()


def init_mail(app):
    app.config["MAIL_SERVER"]   = os.environ.get("MAIL_SERVER",   "smtp.gmail.com")
    app.config["MAIL_PORT"]     = int(os.environ.get("MAIL_PORT", 587))
    app.config["MAIL_USE_TLS"]  = os.environ.get("MAIL_USE_TLS",  "true").lower() == "true"
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME", "")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD", "")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get(
        "MAIL_FROM",
        f"Det 520 Uniforms <{os.environ.get('MAIL_USERNAME', 'noreply@det520.edu')}>"
    )
    mail.init_app(app)


def send_reset_email(to_email: str, cadet_name: str, reset_url: str) -> bool:
    """
    Send a password-reset link. Returns True on success, False on failure.
    """
    if not os.environ.get("MAIL_USERNAME"):
        print(f"[mailer] MAIL_USERNAME not set — skipping email to {to_email}")
        print(f"[mailer] Reset URL would have been: {reset_url}")
        return False

    try:
        msg = Message(
            subject="Det 520 Uniform Portal — Password Reset",
            recipients=[to_email],
        )
        # Plain-text body
        msg.body = (
            f"Hi {cadet_name},\n\n"
            f"A password reset was requested for your Det 520 Uniform Portal account.\n\n"
            f"Click the link below to set a new password (expires in 30 minutes):\n\n"
            f"  {reset_url}\n\n"
            f"If you did not request this, you can safely ignore this email.\n\n"
            f"— Det 520 A4 Uniforms"
        )
        # HTML body
        msg.html = f"""
        <div style="font-family:sans-serif;max-width:480px;margin:auto;padding:32px;">
          <h2 style="color:#c8a84b;letter-spacing:2px;">DET 520 · UNIFORMS</h2>
          <p>Hi <strong>{cadet_name}</strong>,</p>
          <p>A password reset was requested for your account.</p>
          <p>
            <a href="{reset_url}"
               style="display:inline-block;padding:12px 24px;background:#4a90d9;
                      color:#fff;text-decoration:none;border-radius:4px;
                      font-weight:bold;">
              Reset My Password
            </a>
          </p>
          <p style="color:#888;font-size:0.85em;">
            This link expires in 30 minutes.<br/>
            If you did not request this, ignore this email.
          </p>
        </div>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"[mailer] Failed to send email: {e}")
        return False
