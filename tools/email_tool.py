"""
Email Tool for Jarvis
Send and read emails using SMTP and IMAP
"""
from langchain.tools import tool
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from datetime import datetime


# Email configuration from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password for Gmail
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """
    Send an email to a recipient.
    
    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
    
    Examples:
        - "Send email to john@example.com about meeting" 
        - "Email test@example.com with subject 'Hello' and message 'How are you?'"
    
    Returns:
        Confirmation message
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return "Email not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, to, text)
        server.quit()
        
        return f"✅ Email sent to {to} with subject '{subject}'"
        
    except Exception as e:
        logging.error(f"Email send error: {e}")
        return f"❌ Failed to send email: {str(e)}"


@tool
def read_latest_emails(count: int = 5) -> str:
    """
    Read the latest emails from inbox.
    
    Args:
        count: Number of emails to read (default: 5)
    
    Examples:
        - "Read my latest emails"
        - "Show me my last 3 emails"
        - "What are my recent emails?"
    
    Returns:
        List of recent emails
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return "Email not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
    
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('inbox')
        
        # Search for all emails
        result, data = mail.search(None, 'ALL')
        email_ids = data[0].split()
        
        # Get the latest N emails
        latest_ids = email_ids[-count:] if len(email_ids) >= count else email_ids
        
        emails_info = []
        for email_id in reversed(latest_ids):  # Most recent first
            result, msg_data = mail.fetch(email_id, '(RFC822)')
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract email details
            from_addr = msg.get('From')
            subject = msg.get('Subject')
            date = msg.get('Date')
            
            # Get email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
            
            # Truncate long bodies
            if len(body) > 200:
                body = body[:200] + "..."
            
            emails_info.append(f"📧 From: {from_addr}\n   Subject: {subject}\n   Date: {date}\n   Preview: {body}\n")
        
        mail.close()
        mail.logout()
        
        if emails_info:
            return f"Latest {len(emails_info)} emails:\n\n" + "\n".join(emails_info)
        else:
            return "No emails found in inbox."
            
    except Exception as e:
        logging.error(f"Email read error: {e}")
        return f"❌ Failed to read emails: {str(e)}"


@tool
def check_unread_count() -> str:
    """
    Check how many unread emails are in the inbox.
    
    Examples:
        - "Do I have any unread emails?"
        - "How many unread emails do I have?"
        - "Check my inbox"
    
    Returns:
        Number of unread emails
    """
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        return "Email not configured. Please set EMAIL_ADDRESS and EMAIL_PASSWORD in .env file."
    
    try:
        # Connect to IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        mail.select('inbox')
        
        # Search for unread emails
        result, data = mail.search(None, 'UNSEEN')
        unread_ids = data[0].split()
        
        mail.close()
        mail.logout()
        
        count = len(unread_ids)
        if count == 0:
            return "📬 No unread emails"
        elif count == 1:
            return "📬 You have 1 unread email"
        else:
            return f"📬 You have {count} unread emails"
            
    except Exception as e:
        logging.error(f"Email check error: {e}")
        return f"❌ Failed to check emails: {str(e)}"


# Quick test
if __name__ == "__main__":
    print("Email tools created. Configure EMAIL_ADDRESS and EMAIL_PASSWORD in .env to use.")
