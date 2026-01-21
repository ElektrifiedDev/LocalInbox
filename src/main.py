import imap_tools
import smtplib
import email
import hashlib
import json
import os
import sys
import datetime
import sqlite3
import webview as pywebview
import cryptography

from datetime import datetime

from database import db_handler
from core import imap_logic, mail_manager

current_dir = os.path.dirname(os.path.abspath(__file__))

APP_DATA_PATH = os.path.join(os.environ['APPDATA'], 'LocalInbox')
if not os.path.exists(APP_DATA_PATH):
    os.makedirs(APP_DATA_PATH)

DATA_DIR = os.path.join(APP_DATA_PATH, 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOCAL_EMAIL_DB_PATH = os.path.join(DATA_DIR, 'local_emails.db')
CREDS_PATH = os.path.join(DATA_DIR, 'credentials.json')

UI_PATH = os.path.join(current_dir, 'ui', 'index.html')

def init_credentials():
    # If the file doesn't exist, create it with an empty dictionary
    if not os.path.exists(CREDS_PATH):
        with open(CREDS_PATH, 'w') as f:
            json.dump({}, f)
        print("Initialized empty credentials file.")

def save_credentials(email_address, password, host):
    data = {
        "email": email_address,
        "password": password, # In the future, encrypt this!
        "host": host
    }
    with open(CREDS_PATH, 'w') as f:
        json.dump(data, f)

def load_credentials():
    if not os.path.exists(CREDS_PATH):
        return None
    with open(CREDS_PATH, 'r') as f:
        data = json.load(f)
    return data

db_handler.init_db(LOCAL_EMAIL_DB_PATH)

def test_db_write():
    # Call your db_handler to insert a fake email
    db_handler.insert_email(
        LOCAL_EMAIL_DB_PATH, 
        "test-123", 
        "system@local", 
        "Hello World", 
        "It works!", 
        "2026-01-21", 
        0
    )
    return print("Successfully wrote to SQLite in AppData!")

def start_gui():
    window = pywebview.create_window('LocalInbox', UI_PATH, width=1200, height=800)

    window.expose(save_credentials, load_credentials, imap_logic.sync_emails, test_db_write)

    pywebview.start(gui='qt')

if __name__ == '__main__':
    start_gui()