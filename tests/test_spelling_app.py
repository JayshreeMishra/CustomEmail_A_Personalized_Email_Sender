import sys
from flask import Flask, request, render_template
from ml.pipeline.predict_pipeline_spelling_corrector import SpellingPredictPipeline
from config.logging_config import logger
from config.exception import CustomException

app = Flask(__name__, template_folder='test_template')

@app.route('/')
def home():
    return render_template('spelling_index.html')

@app.route('/spellingpredict', methods=['POST'])
def spellingpredict():
    try:
        data = request.form

        if 'mail_text' not in data or not data['mail_text'].strip():
            return {"error": "No mail_text provided or it is empty"}, 400

        mail_text = data['mail_text']
        pipeline = SpellingPredictPipeline()

        result = pipeline.predict(mail_text)

        return {"corrected_text": result}, 200

    except Exception as e:
        raise CustomException(e, sys)
    
if __name__=='__main__':
    app.run(debug=True)