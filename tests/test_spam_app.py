from flask import Flask, request, jsonify, render_template
from ml.pipeline.predict_pipeline_spam_detection import SpamPredictPipeline
import logging

app = Flask(__name__, template_folder='test_template')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return render_template('spam_index.html') 

@app.route('/spampredict', methods=['POST'])
def predict():
    try:

        logger.info("Request headers: %s", request.headers)
        
        data = request.form

        if 'mail_text' not in data or not data['mail_text'].strip():
            return jsonify({"error": "No mail_text provided or it is empty"}), 400

        mail_text = data['mail_text']

        pipeline = SpamPredictPipeline()

        result = pipeline.predict(mail_text)

        result = int(result[0]) 

        return jsonify({"prediction": result})

    except Exception as e:
        logger.error("Error in prediction: %s", str(e), exc_info=True)
        return jsonify({"error": "An error occurred during prediction"}), 500

if __name__ == '__main__':
    app.run(debug=True)
