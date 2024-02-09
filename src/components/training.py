import os
os.chdir('D:\ML_Projects\student_performance_regressor')

import sys
from dataclasses import dataclass

import warnings
warnings.filterwarnings('ignore')
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

from src.utilities import save_object,evaluate_models

@dataclass
class ModelTrainingConfig:
    trained_model_patj = os.path.join("Artifacts","model.pkl")
    
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainingConfig()
        
    def start_model_trainer(self, train_array, test_array):
        try:
            logging.info("Model training started, splitting train and test data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            
            models = {
                'LinearReg': LinearRegression(),
                "Ridge": Ridge(),
                "Lasso": Lasso(),
                "DecisionTree": DecisionTreeRegressor(),
                "RandomForest": RandomForestRegressor(),
                "XGBoost": XGBRegressor(),
                "Adaboost": AdaBoostRegressor()
            }
            
            model_report:dict=evaluate_models(X_train=X_train, y_train=y_train, X_test = X_test, y_test = y_test, models = models)
            
            best_model_Score = max(model_report.values())
            
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_Score)
            ]
            
            best_model = models[best_model_name]
            
            if best_model_Score < 0.6:
                raise CustomException("No best model found")
            logging.info("Best model on training and test data")
            
            save_object(
                file_path= self.model_trainer_config.trained_model_patj,
                obj = best_model
            )
            
            predictions = best_model.predict(X_test)
            
            r2_squared = r2_score(y_test, predictions)
            return r2_squared
            
        except Exception as e:
            raise CustomException(e,sys)
            