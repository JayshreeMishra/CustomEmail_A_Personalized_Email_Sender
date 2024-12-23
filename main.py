import os, sys
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import email

from app.email_sender import send_email
from config.logging_config import logger
from config.exception import CustomException

template_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')

app= Flask(__name__, static_folder='app/static', template_folder=template_folder_path)
app.secret_key = 'mysecretkey'

# File upload folder
upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
os.makedirs(upload_folder, exist_ok=True)

# Home route: Display emailform
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        sender_email= request.form.get('sender_email')
        sender_password= request.form.get('sender_app_password')
        recipient_input= request.form.get('recipients')
        recipient_names_input= request.form.get('recipient_names')
        recipient_company_input= request.form.get('recipient_companies')
        subject= request.form.get('subject')
        message= request.form.get('message')

        # Process recipients
        recipients= [email.strip() for email in recipient_input.split('\n') if email.strip()]
        recipient_names= [email.strip() for email in recipient_names_input.split('\n') if email.strip()]
        recipient_companies= [email.strip() for email in recipient_company_input.split('\n') if email.strip()]

         # Ensure the lists are of the same length
        if len(recipients) != len(recipient_names) or len(recipients) != len(recipient_companies):
            logger.error("The number of recipients, names, and companies must match.")
            flash("The number of recipients, names, and companies must match.", "danger")
            return render_template('email_form.html', error=True)

        #file upload
        file= request.files.get('file')
        attachment= None

        if file:
            file_name= secure_filename(file.filename)
            file_path= os.path.join(upload_folder, file_name)
            file.save(file_path)
            attachment= file_path


        #Send email
        if recipients and subject and message:
            try:
                result = send_email(sender_email, sender_password, recipients, subject, message, recipient_names, recipient_companies, attachment)
            except Exception as e:
                result = f"Error sending email: {str(e)}"
        else:
            result = "All fields are required!"

        # Display success or error messages
        if not result:
            result = "An unexpected error occurred!"
        flash(result, "success" if "successfully" in result else "danger")

    return render_template('email_form.html')


if __name__== '__main__':
    app.run(debug=True)
