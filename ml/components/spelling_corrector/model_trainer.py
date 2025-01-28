import os
import sys
import pickle
import pandas as pd
from dataclasses import dataclass
from symspellpy import SymSpell
from language_tool_python import LanguageTool

from config.logging_config import logger
from config.exception import CustomException


@dataclass
class SpellingModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "spelling_model.pkl")
    combined_dictionary_file_path: str = os.path.join("artifacts", "combined_dictionary.txt")


class SpellingModel:
    def __init__(self):
        self.sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        self.language_tool = LanguageTool('en')

    def correct_spelling(self, texts):
        corrected_texts = []
        for text in texts:
            suggestions = self.sym_spell.lookup_compound(text, max_edit_distance=2)
            corrected_texts.append(suggestions[0].term if suggestions else text)
        return corrected_texts

    def correct_grammar(self, texts):
        corrected_texts = []
        for text in texts:
            corrected_text = self.language_tool.correct(text)
            corrected_texts.append(corrected_text)
        return corrected_texts

    # Custom methods for pickling
    def __getstate__(self):
        # Excluded language_tool from being pickled
        state = self.__dict__.copy()
        state['language_tool'] = None
        return state

    def __setstate__(self, state):
        # Restore the object and recreate the language_tool instance
        self.__dict__.update(state)
        self.language_tool = LanguageTool('en')



class SpellingModelTrainer:
    def __init__(self):
        self.model_trainer_config = SpellingModelTrainerConfig()

    def initiate_model_trainer(self, train_data_path: str, test_data_path: str):
        try:
            logger.info("Starting model training.")

            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)

            logger.info("Preparing combined dictionary for SymSpell.")
            model = SpellingModel()

            dictionary_path = self.model_trainer_config.combined_dictionary_file_path
            combined_data = pd.concat([
                pd.read_csv(r"ml/data/en-80k.txt", sep="\t", header=None, names=["term", "count"]),
                pd.read_csv(r"ml/data/core-wordnet.txt", sep="\t", header=None, names=["term", "relation", "definition"]),
                pd.read_csv(r"ml/data/teleological-links.txt", sep="\t", header=None, names=["word1", "relation", "word2"]),
                pd.read_csv(r"ml/data/morphosemantic-links.txt", sep="\t", header=None, names=["word1", "relation", "word2", "gloss1", "gloss2"])
            ])
            combined_data[['term', 'count']].to_csv(dictionary_path, sep="\t", index=False, header=False)

            model.sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)
            logger.info("Combined dictionary saved and loaded into SymSpell.")

            logger.info("Applying spelling and grammar correction to training and testing data.")
            spelling_corrected_train = model.correct_spelling(train_data['input_text'])
            spelling_corrected_test = model.correct_spelling(test_data['input_text'])

            grammar_corrected_train = model.correct_grammar(spelling_corrected_train)
            grammar_corrected_test = model.correct_grammar(spelling_corrected_test)

            corrected_train_path = train_data_path.replace(".csv", "_corrected.csv")
            corrected_test_path = test_data_path.replace(".csv", "_corrected.csv")
            train_data['corrected_text'] = grammar_corrected_train
            test_data['corrected_text'] = grammar_corrected_test

            train_data.to_csv(corrected_train_path, index=False)
            test_data.to_csv(corrected_test_path, index=False)

            logger.info("Saving the trained SpellingModel.")
            try:
                with open(self.model_trainer_config.trained_model_file_path, 'wb') as f:
                    pickle.dump(model, f)
                logger.info(f"Model saved at {self.model_trainer_config.trained_model_file_path}.")
            except Exception as e:
                logger.error("Failed to save the model.")
                raise CustomException(e, sys)

            logger.info("Model training completed successfully.")

        except Exception as e:
            raise CustomException(e, sys)
