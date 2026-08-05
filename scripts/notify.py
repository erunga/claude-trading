# scripts/notify.py — sends today's journal as an email
import os, sys
from dotenv import load_dotenv
from brevo import Brevo

load_dotenv()

def send_digest(journal_path):
    with open(journal_path, 'r') as f:
        content = f.read()

    client = Brevo(api_key=os.getenv("BREVO_API_KEY"))
    client.transactional_emails.send_transac_email(
        sender={"email": os.getenv("NOTIFY_FROM_EMAIL"), "name": "Trading Agent"},
        to=[{"email": os.getenv("NOTIFY_EMAIL")}],
        subject=f"Trading Agent Report — {journal_path.split('/')[-1]}",
        text_content=content,
    )

if __name__ == "__main__":
    send_digest(sys.argv[1])