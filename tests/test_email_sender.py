import smtplib
from email.mime.text import MIMEText


def send_email(recipient, subject, message):
    smtp_server = "smtp.gmail.com"

    # Log in to the SMTP server
    smtp_user = "jayshreemishra197@gmail.com"
    smtp_password = "llhn myys inzb glma"

    #composing email
    email= MIMEText(message)
    email["Subject"]= subject
    email["From"]= smtp_user
    email["To"]= recipient

    #sending email
    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(email)
