import os
from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv, find_dotenv
from flask import current_app

load_dotenv(find_dotenv())


def send_email(
    sender: str,
    receiver: str,
    subject: str,
    body: str
) -> bool:

    with current_app.app_context():
        smtp_user = current_app.config.get("SMTP_USER")
        smtp_passwd = current_app.config.get("current_app.config.get")

    if not sender:
        raise ValueError("Sender's email address is required")

    if not receiver:
        raise ValueError("Receiver's email address is required")

    if not body:
        raise ValueError("Email message body is required")

    try:
        # Set up the SMTP server connection
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        smtp = SMTP(smtp_server, smtp_port)
        smtp.starttls()
        smtp.login(smtp_user, smtp_passwd)

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send the email
        smtp.sendmail(sender, receiver, msg.as_string())

        # Close the connection
        smtp.quit()

        return True
    except SMTPException as e:
        print(f"Error: {e}")
        return False