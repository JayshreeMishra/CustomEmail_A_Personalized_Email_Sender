import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

# Adding the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from config.exception import CustomException
from config.logging_config import logger

@dataclass
class SpamDataIngestionConfig:
    train_data_path: str=os.path.join("artifacts", "spam_train.csv")
    test_data_path: str=os.path.join("artifacts", "spam_test.csv")
    raw_data_path: str=os.path.join("artifacts", "spam_raw.csv")

class SpamDataIngestion:
    def __init__(self):
        self.ingestion_config= SpamDataIngestionConfig()

    def initiate_data_ingestion(self):
        logger.info("Entered the spam data ingestion component")
        try:
            df=pd.read_csv(r"ml\data\email_spam_classification.csv")
            logger.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logger.info("Train test split initiated")
            train_set, test_set= train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header= True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header= True)

            logger.info("Data ingestion completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)
        


#this is to test the data ingestion component
if __name__=="__main__":
    obj= SpamDataIngestion()
    obj.initiate_data_ingestion()
