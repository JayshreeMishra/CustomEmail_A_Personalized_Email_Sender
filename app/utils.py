import os, sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional
from ensure import ensure_annotations

from config.exception import CustomException
from config.logging_config import logger

@ensure_annotations
def allowed_file_type(filename: str) -> bool:
    allowed_extensions = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'xls', 'xlsx',
        'ppt', 'pptx', 'csv', 'zip', 'rar', '7z', 'bmp', 'tiff', 'svg', 'html',
        'xml', 'json', 'mp3', 'wav', 'mp4', 'avi', 'mov', 'mkv', 'log'
    }
    is_allowed = '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions
    logger.info(f"File type allowed: {is_allowed} for file: {filename}")
    return is_allowed

#@ensure_annotations
def attach_file(email: MIMEMultipart, attachment: Optional[str]) -> None:
    if attachment:
        if allowed_file_type(attachment):
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
                    logger.info("Attachment successfully added.")
            except FileNotFoundError:
                raise CustomException(f"Attachment file not found: {attachment}", sys)
            except Exception as e:
                raise CustomException(f"An error occurred while attaching the file: {str(e)}", sys)
            


def authenticate_user(sender_email, sender_password):
    try:
        smtp_servers = {
            "gmail.com": "smtp.gmail.com",
            "outlook.com": "smtp-mail.outlook.com",
            "hotmail.com": "smtp-mail.outlook.com",
            "live.com": "smtp-mail.outlook.com",
            "yahoo.com": "smtp.mail.yahoo.com",
            "ymail.com": "smtp.mail.yahoo.com",
            "proton.me": "protonmail.com",
            "protonmail.com": "protonmail.com",
            "zohomail.com": "smtp.zoho.com",
            "icloud.com": "smtp.mail.me.com",
            "me.com": "smtp.mail.me.com",
            "mac.com": "smtp.mail.me.com",
            "gmx.com": "mail.gmx.com",
            "gmx.net": "mail.gmx.com",
            "mail.com": "smtp.mail.com",
        }

        email_domain= sender_email.split("@")[-1]

        smtp_server= smtp_servers.get(email_domain)
        if not smtp_server:
            raise ValueError(f"Unsupported email domain: {email_domain}")

        logger.info(f"Authentication successful for {sender_email}")
        return smtp_server, sender_email, sender_password
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise CustomException(f"An error occurred while authenticating the user: {str(e)}")