import os, sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config.exception import CustomException
from config.logging_config import logger
from app.utils import attach_file, authenticate_user



def send_email(sender_email, sender_password, recipient, subject, message, attachment=None):
    try:
        #Authenticate sender email
        smtp_server, smtp_user, smtp_password= authenticate_user(sender_email, sender_password) 

        # Compose the email
        email = MIMEMultipart()
        email["Subject"] = subject
        email["From"] = smtp_user
        email["To"] = recipient

        # Attach the message body
        email.attach(MIMEText(message, 'plain'))

        # Attach file if present and allowed
        if attachment:
            logger.info(f"Attaching file: {attachment}")
            attach_file(email, attachment)
        
        # Send the email
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipient, email.as_string())
        return "Email sent successfully with attachment!" if attachment else "Email sent successfully without attachment!"
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise CustomException(f"Failed to send email: {e}", sys)