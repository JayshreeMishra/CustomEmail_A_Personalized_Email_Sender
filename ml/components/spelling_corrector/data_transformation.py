import os, sys
import pandas as pd
from dataclasses import dataclass
from transformers import AutoTokenizer
from config.exception import CustomException
from config.logging_config import logger


@dataclass
class SpellingDataTransformationConfig:
    transformed_train_data_path: str = os.path.join("artifacts", "transformed_train.csv")
    transformed_test_data_path: str = os.path.join("artifacts", "transformed_test.csv")

class SpellingDataTransformation:
    def __init__(self):
        self.transformation_config = SpellingDataTransformationConfig()
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=False)

    def preprocess_function(self, examples):
        inputs = self.tokenizer(
            examples['input_text'], max_length=128, truncation=True, padding='max_length'
        )
        targets = self.tokenizer(
            examples['target_text'], max_length=128, truncation=True, padding='max_length'
        )

        labels = [
            [(label if label != self.tokenizer.pad_token_id else -100) for label in label_seq]
            for label_seq in targets['input_ids']
        ]
        inputs['labels'] = labels
        return inputs

    def initiate_data_transformation(self, train_data_path, test_data_path):
        logger.info("Entered the data transformation component")
        try:
            # Load datasets
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)

            # Tokenize the datasets
            train_dataset = train_data.to_dict(orient='list')
            test_dataset = test_data.to_dict(orient='list')

            tokenized_train_dataset = self.preprocess_function(train_dataset)
            tokenized_test_dataset = self.preprocess_function(test_dataset)

            # Save transformed datasets
            os.makedirs(os.path.dirname(self.transformation_config.transformed_train_data_path), exist_ok=True)
            pd.DataFrame(tokenized_train_dataset).to_csv(self.transformation_config.transformed_train_data_path, index=False)
            pd.DataFrame(tokenized_test_dataset).to_csv(self.transformation_config.transformed_test_data_path, index=False)

            logger.info("Data transformation completed successfully")

            return (
                self.transformation_config.transformed_train_data_path,
                self.transformation_config.transformed_test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)
