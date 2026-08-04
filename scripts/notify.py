# scripts/notify.py — sends today's journal as an email
import os, sys
import sendgrid
from sendgrid.helpers.mail import Mail

def send_digest(journal_path):
    with open(journal_path, 'r') as f:
        content = f.read()
    
    sg = sendgrid.SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    message = Mail(
        from_email="agent@yourdomain.com",
        to_emails=os.getenv("NOTIFY_EMAIL"),
        subject=f"Trading Agent Report — {journal_path.split('/')[-1]}",
        plain_text_content=content
    )
    sg.send(message)

if __name__ == "__main__":
    send_digest(sys.argv[1])