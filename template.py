import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name= "CustomEmail_A_Personalized_Email_Sender"

list_of_files = [
    "app/__init__.py",
    "app/email_sender.py",
    "app/utils.py",
    "app/static/placeholder.js",
    "app/static/styles.css",
    "app/templates/email_form.html",
    "artifacts/",
    "config/__init__.py",
    "config/exception.py",
    "config/logging_config.py",
    "logs/",
    "ml/__init__.py",
    "ml/utils.py",
    "ml/components/spam_detection/data_ingestion.py",
    "ml/components/spam_detection/data_transformation.py",
    "ml/components/spam_detection/model_trainer.py",
    "ml/components/spelling_corrector/data_ingestion.py",
    "ml/components/spelling_corrector/data_transformation.py",
    "ml/components/spelling_corrector/model_trainer.py",
    "ml/data/",
    "ml/notebook_experiment/spam_classification.ipynb",
    "ml/notebook_experiment/spelling_corrector.ipynb",
    "ml/pipeline/predict_pipeline_spam_detection.py",
    "ml/pipeline/predict_pipeline_spelling_corrector.py",
    "tests/",
    "upload/",
    "__init__.py",
    ".gitignore",
    "LICENSE",
    "main.py",
    "README.md",
    "requirements.txt",
    "setup.py",
    "template.py",
]

for filepath in list_of_files:
    filepath= Path(filepath)

    filedir, filename=os.path.split(filepath)

    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")