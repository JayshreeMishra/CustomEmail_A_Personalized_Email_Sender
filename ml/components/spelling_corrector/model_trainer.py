import os, sys
import pandas as pd
import pickle
from dataclasses import dataclass
import torch
from symspellpy import SymSpell
from language_tool_python import LanguageTool

from config.logging_config import logger
from config.exception import CustomException

@dataclass
class SpellingModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "spell_model.pkl")
    combined_dictionary_file_path = os.path.join("artifacts", "combined_dictionary.txt")

class SpellingModelTrainer:
    def __init__(self):
        self.model_trainer_config = SpellingModelTrainerConfig()
        self.language_tool = LanguageTool('en')

    def correct_spelling(self, texts, sym_spell):
        corrected_texts = []
        for text in texts:
            suggestions = sym_spell.lookup_compound(text, max_edit_distance=2)
            corrected_texts.append(suggestions[0].term if suggestions else text)
        return corrected_texts
    
    def correct_grammar(self, texts):
        corrected_texts = []
        for text in texts:
            corrected_text = self.language_tool.correct(text)
            corrected_texts.append(corrected_text)
        return corrected_texts

    def initiate_model_trainer(self, train_data_path: str, test_data_path: str):
        try:
            logger.info("starting model training")

            # Load train and test datasets
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)

            # Combine spelling dictionaries into a single file
            logger.info("Preparing combined dictionary for SymSpell")
            sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
            dictionary_path = self.model_trainer_config.combined_dictionary_file_path

            combined_data = pd.concat([
                pd.read_csv(r"ml/data/en-80k.txt", sep="\t", header=None, names=["term", "count"]),
                pd.read_csv(r"ml/data/core-wordnet.txt", sep="\t", header=None, names=["term", "relation", "definition"]),
                pd.read_csv(r"ml/data/teleological-links.txt", sep="\t", header=None, names=["word1", "relation", "word2"]),
                pd.read_csv(r"ml/data/morphosemantic-links.txt", sep="\t", header=None, names=["word1", "relation", "word2", "gloss1", "gloss2"])
            ])
            combined_data.to_csv(dictionary_path, sep="\t", index=False, header=False)

            logger.info("Combined dictionary saved as 'combined_dictionary.txt'")

            sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

            logger.info("Applying spelling correction")
            spelling_corrected_train = self.correct_spelling(train_data['input_text'], sym_spell)
            spelling_corrected_test = self.correct_spelling(test_data['input_text'], sym_spell)

            logger.info("Applying grammar correction")
            grammar_corrected_train = self.correct_grammar(spelling_corrected_train)
            grammar_corrected_test = self.correct_grammar(spelling_corrected_test)

            # Save corrected data
            train_data['corrected_text'] = grammar_corrected_train
            test_data['corrected_text'] = grammar_corrected_test

            train_data.to_csv(train_data_path, index=False)
            test_data.to_csv(test_data_path, index=False)

            # Model Evaluation: Print first 5 corrected predictions and references
            logger.info("Model evaluation:")
            for corrected_pred, ref in zip(grammar_corrected_test[:5], test_data['target_text'][:5]):
                logger.info(f"Corrected Prediction: {corrected_pred}")
                logger.info(f"Reference: {ref}")
                logger.info("")

            # Save the model (SymSpell object)
            with open(self.model_trainer_config.trained_model_file_path, 'wb') as f:
                pickle.dump(sym_spell, f)

            logger.info(f"Model saved as {self.model_trainer_config.trained_model_file_path}")
            logger.info("Model training completed successfully")
        
        except Exception as e:
            raise CustomException(e, sys)
