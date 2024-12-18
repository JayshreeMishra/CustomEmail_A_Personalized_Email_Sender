import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

project_name= "CustomEmail_A_Personalized_Email_Sender"


list_of_files= [
    f"app/__init__.py",
    f"app/routes.py",
    f"app/templates/index.html",
    f"app/static/style.css",
    f"app/forms.py",
    f"app/utils.py",
    f"ml/__init__.py",
    f"ml/model.py",
    f"ml/preprocess.py",
    f"ml/training/train.py",
    f"ml/training/config.yaml",
    f"ml/training/artifacts/",
    f"ml/tests/test_ml.py",
    f"tests/test_app.py",
    f"config/app_config.py",
    f"config/logging_config.py",
    f"config/secrets.yaml",
    f"database/__init__.py",
    f"database/models.py",
    f"database/queries.py",
    f"docs/api_docs.md",
    f"docs/usage.md",
    f"logs/app.log",
    "main.py",
    "setup.py",
    "requirements.txt",
    "__init__.py",
    "README.md"

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