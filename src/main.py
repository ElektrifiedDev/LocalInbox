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
import PyQt5
import qtpy

from datetime import datetime
from PyQt5 import QtWidgets, QtCore, QtGui, QtWebEngineWidgets

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
            json.dump([], f)
        print("Initialized empty credentials file.")

def save_credentials(name, email_address, password, host):
    try:
        data = load_credentials()
        new_profile = {
            "id": len(data) + 1, # Add this so JS can track which profile is which
            "name": name,
            "email": email_address,
            "password": password, 
            "host": host
        }
        data.append(new_profile) # Append to the list we just loaded
        
        with open(CREDS_PATH, 'w') as f:
            json.dump(data, f, indent=4) # indent makes the file readable for you!

        return {"status": "success", "message": "Credentials saved."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def load_credentials():
    if not os.path.exists(CREDS_PATH):
        return []   
    try:
        with open(CREDS_PATH, 'r') as f:
            data = json.load(f)
            print("Loaded credentials:", data)  
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []

db_handler.init_db(LOCAL_EMAIL_DB_PATH)

def get_email_address(uid):
    profiles = load_credentials()
    for profile in profiles:
        if profile["id"] == uid:
            return profile["email"]
    return None

def get_email_password(uid):
    profiles = load_credentials()
    for profile in profiles:
        if profile["id"] == uid:
            return profile["password"]
    return None

def get_email_host(uid):
    profiles = load_credentials()
    for profile in profiles:
        if profile["id"] == uid:
            return profile["host"]
    return None

def start_gui():
    window = pywebview.create_window('LocalInbox', UI_PATH, width=1200, height=800)

    window.expose(save_credentials, load_credentials, imap_logic.sync_emails, get_email_address, get_email_password, get_email_host)
    pywebview.start(gui='qt')

if __name__ == '__main__':
    start_gui()