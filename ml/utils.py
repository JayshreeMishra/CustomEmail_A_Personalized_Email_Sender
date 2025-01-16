import os, sys, io
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

from config.exception import CustomException
from config.logging_config import logger


def save_obj(file_path, obj):
    try:
        dir_path= os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    

def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report={}

        for i in range(len(list(models))):
            model= list(models.values())[i]

            # Check if the model has a `verbose` or `logging_level` parameter, e.g., CatBoost
            if hasattr(model, 'verbose'):
                model.set_params(verbose=0)
            if hasattr(model, 'logging_level'):
                model.set_params(logging_level='Silent')
            
            #redirect stdout to supress output
            old_stdout= sys.stdout
            sys.stdout= io.StringIO()

            model.fit(X_train, y_train)

            #restore stdout
            sys.stdout= old_stdout

            y_train_pred= model.predict(X_train)
            y_test_pred= model.predict(X_test)

            train_model_score= r2_score(y_train, y_train_pred)
            test_model_score= r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]]= test_model_score
        
        return report
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
        
    except Exception as e:
        raise CustomException(e, sys)