from imap_tools import MailBox, AND
from database import db_handler
from main import LOCAL_EMAIL_DB_PATH

def sync_emails(host, email_address, password, db_path=LOCAL_EMAIL_DB_PATH):
    try:
        with MailBox(host).login(email_address, password) as mailbox:
            for msg in mailbox.fetch(limit=20, reverse=True):
                # We send the data to a helper in db_handler
                db_handler.insert_email(
                    db_path,
                    msg.uid, 
                    msg.to,
                    msg.from_, 
                    msg.subject, 
                    msg.html or msg.text, 
                    str(msg.date), 
                    1 if 'Seen' in msg.flags else 0
                )
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def fetch_emails(email_address, db_path=LOCAL_EMAIL_DB_PATH):
    emails = []
    fetched_emails = db_handler.load_emails(email_address, db_path)
    for i in fetched_emails:
        emails.append(i)