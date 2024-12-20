import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import Flask, render_template, request, flash
from test_email_sender import send_email
from config.exception import CustomException as ex

app= Flask(__name__, template_folder='test_template')
app.secret_key = 'mysecretkey'

# Home route: Display emailform
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method=='POST':
        recipient= request.form.get('recipient')
        subject= request.form.get('subject')
        message= request.form.get('message')

        #Send email
        if recipient and subject and message:
            try:
                send_email(recipient, subject, message)
                flash("Email sent sucessfully!", "success")
            except Exception as e:
                flash(f"Failed to send email: {str(e)}", "danger")
        else:
             flash("All fields are required!", "warning")

    return render_template('test_index.html')


if __name__== '__main__':
    app.run(debug=True)