import sys
import pandas as pd
from config.exception import CustomException
from ml.utils import load_object

class SpamPredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = r"artifacts\spam_model.pkl"
            vectorizer_path = r"artifacts\tfidf_vectorizer.pkl"
            preprocessor_path = r"artifacts\spam_text_preprocessor.pkl"

            model = load_object(file_path=model_path)
            vectorizer = load_object(file_path=vectorizer_path)
            preprocessor = load_object(file_path=preprocessor_path)

            transformed_features = preprocessor.transform_text(features)
            vectorized_features = vectorizer.transform([transformed_features])  # Input must be a list

            prediction = model.predict(vectorized_features)

            return prediction

        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self, mail_text: str):
        if not mail_text:
            raise ValueError("Mail text must not be empty")
        self.mail_text = mail_text

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "Mail_Text": [self.mail_text]
            }
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
