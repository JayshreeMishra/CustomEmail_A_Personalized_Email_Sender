import sys
import os
from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename

from app.email_sender import send_email
from config.exception import CustomException as ex

template_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'templates')

app= Flask(__name__, template_folder=template_folder_path)
app.secret_key = 'mysecretkey'

# File upload folder
upload_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload')
os.makedirs(upload_folder, exist_ok=True)

# Home route: Display emailform
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        recipient= request.form.get('recipient')
        subject= request.form.get('subject')
        message= request.form.get('message')

        #file upload
        file= request.files.get('file')
        attachment= None

        if file:
            file_name= secure_filename(file.filename)
            file_path= os.path.join(upload_folder, file_name)
            file.save(file_path)
            attachment= file_path


        #Send email
        if recipient and subject and message:
            try:
                result = send_email(recipient, subject, message, attachment)
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
