import os
os.chdir('D:\ML_Projects\student_performance_regressor')

import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src import logger
from src import exception

@dataclass
class DataIngestnConfig:
    # create a data class that has all the path related stuff related to data
    train_data_path: str=os.path.join('Artifacts','train.csv')
    test_data_path: str=os.path.join('Artifacts','test.csv')
    raw_data_path: str=os.path.join('Artifacts','raw.csv')
    
class DataIngestn:
    def __init__(self):
        self.config = DataIngestnConfig()
        
    def start_data_ingestn(self):
        # read data from source
        logger.logging.info("Started Data Ingestion Component")
        try:
            df = pd.read_csv('D:\ML_Projects\student_performance_regressor\\research\stud.csv')
            logger.logging.info("Data reading completed.")
            
            os.makedirs(os.path.dirname(self.config.raw_data_path), exist_ok= True) #If the path already exists, it doesn;t create a new directry
            
            df.to_csv(self.config.raw_data_path, index=False, header=True)
            
            logger.logging.info("Splitting the data to train and test")
            train_Set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            
            train_Set.to_csv(self.config.train_data_path,index=False, header=True)
            
            test_set.to_csv(self.config.test_data_path,index=False, header=True)
            logger.logging.info("Loading data completed.")
            
            return (
                self.config.train_data_path,
                self.config.test_data_path
            )
        except Exception as a:
            logger.logging.warning("Error occured")
            raise exception.CustomException(a,sys)
        
if __name__ == '__main__':
    obj = DataIngestn()
    obj.start_data_ingestn()
