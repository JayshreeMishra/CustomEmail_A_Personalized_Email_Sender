import sys
import pickle
import pandas as pd
from config.exception import CustomException


class SpellingPredictPipeline:
    def __init__(self):
        model_path = r"artifacts\spelling_model.pkl"
        preprocessor_path=r"artifacts\spelling_preprocessor.pkl"
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            
            with open(preprocessor_path, 'rb') as f:
                self.preprocessor = pickle.load(f)
        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, text):
        try:
            preprocessed_text = self.preprocessor.transform(pd.Series([text]))[0]

            if not isinstance(preprocessed_text, str):
                preprocessed_text = str(preprocessed_text)

            spelling_corrected_text = self.model.correct_spelling([text])[0]

            grammar_corrected_text = self.model.correct_grammar([spelling_corrected_text])[0]

            return grammar_corrected_text

        except Exception as e:
            raise CustomException(e, sys)
