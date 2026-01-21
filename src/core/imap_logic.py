from imap_tools import MailBox, AND
from database import db_handler

def sync_emails(host, user, password, db_path):
    try:
        with MailBox(host).login(user, password) as mailbox:
            for msg in mailbox.fetch(limit=20, reverse=True):
                # We send the data to a helper in db_handler
                db_handler.insert_email(
                    db_path,
                    msg.uid, 
                    msg.from_, 
                    msg.subject, 
                    msg.html or msg.text, 
                    str(msg.date), 
                    1 if 'Seen' in msg.flags else 0
                )
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}