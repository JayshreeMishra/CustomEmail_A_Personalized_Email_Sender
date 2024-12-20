import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config.exception import CustomException


def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def send_email(recipient, subject, message, attachment=None):
    smtp_server = "smtp.gmail.com"
    smtp_user = "jayshreemishra197@gmail.com"
    smtp_password = "tvdm jitd slde uzau"  # Use an environment variable for security

    # Compose the email
    email = MIMEMultipart()
    email["Subject"] = subject
    email["From"] = smtp_user
    email["To"] = recipient

    # Attach the message body
    email.attach(MIMEText(message, 'plain'))

    # Attach file if present and allowed
    if attachment:
        if allowed_file(attachment, {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}):
            try:
                with open(attachment, "rb") as file:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{os.path.basename(attachment)}"'
                    )
                    email.attach(part)
                print("Attachment successfully added.")  # Debugging statement
            except FileNotFoundError:
                raise CustomException(f"Attachment file not found: {attachment}", sys)
        else:
            raise CustomException("Invalid file type for attachment.", sys)
    else:
        print("No attachment provided.")  # Debugging statement

    try:
        # Send the email
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, recipient, email.as_string())
        return "Email sent successfully with attachment!" if attachment else "Email sent successfully without attachment!"
    except Exception as e:
        raise CustomException(f"Failed to send email: {e}", sys)