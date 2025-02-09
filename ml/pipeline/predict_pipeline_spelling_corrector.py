
import sys, os
import pickle
import pandas as pd
from config.exception import CustomException

"""
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
"""
#Changes made for deplyment
class SpellingPredictPipeline:
    def __init__(self):
        # Use cross-platform file paths
        model_path = os.path.join("artifacts", "spelling_model.pkl")
        preprocessor_path = os.path.join("artifacts", "spelling_preprocessor.pkl")

        # Debugging: Check if files exist
        if not os.path.exists(model_path) or not os.path.exists(preprocessor_path):
            print("❌ Model or preprocessor file is missing!")
            print("Current Directory:", os.getcwd())
            if os.path.exists("artifacts"):
                print("Contents of artifacts/:", os.listdir("artifacts"))
            else:
                print("❌ artifacts/ folder is missing!")
        
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

            # Correct spelling and track changes
            spelling_corrected_text, changed_words = self.model.correct_spelling(preprocessed_text)

            # Correct grammar (optional, if needed)
            grammar_corrected_text, _ = self.model.correct_grammar(spelling_corrected_text)

            return grammar_corrected_text, changed_words

        except Exception as e:
            raise CustomException(e, sys)