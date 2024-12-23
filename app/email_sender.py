import os, sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from config.exception import CustomException
from config.logging_config import logger
from app.utils import attach_file, authenticate_user



def send_email(sender_email, sender_password, recipients, subject, message, recipient_names, recipient_companies, attachment=None):
    try:
        #Authenticate sender email
        smtp_server, smtp_user, smtp_password= authenticate_user(sender_email, sender_password) 

        # Iterate over each recipient to send an individual email
        for recipient, name, company in zip(recipients, recipient_names, recipient_companies):
        # Compose the email
            email = MIMEMultipart()
            email["Subject"] = subject
            email["From"] = smtp_user
            email["To"] = recipient

            # Customize the message with placeholders
            customized_message = message.replace('|recipient name|', name).replace('|recipient company|', company)
            email.attach(MIMEText(customized_message, 'plain'))

            # Attach file if present and allowed
            if attachment:
                logger.info(f"Attaching file: {attachment}")
                attach_file(email, attachment)
            
            try:
                # Send the email
                with smtplib.SMTP(smtp_server, 587) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(smtp_user, recipient, email.as_string())
                logger.info(f"Email sent successfully to {recipient}")
            except Exception as e:
                logger.error(f"Failed to send email to {recipient}: {e}")

        return "Email sent successfully with attachment!" if attachment else "Email sent successfully without attachment!"
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise CustomException(f"Failed to send email: {e}", sys)
    



    
        
        