import os, sys
import pandas as pd
from dataclasses import dataclass
from transformers import AutoTokenizer
from config.exception import CustomException
from config.logging_config import logger


@dataclass
class SpellingDataTransformationConfig:
    transformed_train_data_path: str = os.path.join("artifacts", "spelling_transformed_train.csv")
    transformed_test_data_path: str = os.path.join("artifacts", "spelling_transformed_test.csv")

class SpellingDataTransformation:
    def __init__(self):
        self.transformation_config = SpellingDataTransformationConfig()
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased', use_fast=False)

    def preprocess_text(self, text):
        return text.strip().lower()
    
    def transform_data(self, data):
        try:
            logger.info("Starting data preprocessing transformation")
            data['input_text'] = data['input_text'].apply(self.preprocess_text)
            logger.info("Data transformation completed successfully")
            return data
        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_data_path, test_data_path):
        logger.info("Entered the data transformation component")
        try:
            logger.info("Reading train and test datasets")
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)

            logger.info("Applying data transformation to train and test datasets")
            transformed_train_data = self.transform_data(train_data)
            transformed_test_data = self.transform_data(test_data)

            # Save transformed datasets
            os.makedirs(os.path.dirname(self.transformation_config.transformed_train_data_path), exist_ok=True)
            transformed_train_data.to_csv(self.transformation_config.transformed_train_data_path, index=False)
            transformed_test_data.to_csv(self.transformation_config.transformed_test_data_path, index=False)

            logger.info("Transformed data saved successfully")

            return (
                self.transformation_config.transformed_train_data_path,
                self.transformation_config.transformed_test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)
