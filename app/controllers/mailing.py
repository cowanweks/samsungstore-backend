import os
from smtplib import SMTP, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWD = os.getenv("SMTP_PASSWD")


if not SMTP_USER or not SMTP_PASSWD:
    raise ValueError("SMTP_USER and SMTP_PASSWD environment variables must be set")


def send_email(
    sender: str,
    receiver: str,
    subject: str,
    body: str
) -> bool:
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
        smtp.login(SMTP_USER, SMTP_PASSWD)

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