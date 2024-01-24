import sys

def error_message_details(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    err_msg = "Error in script: [{0}] line number [{1}] error message [{2}]".format(
    file_name,exc_tb.tb_lineno,str(error)
    )
    
    return err_msg
    
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_detail)
        
    def __str__(self):
        return self.error_message
        
# import os
# os.getcwd()

# from src.logger import logging

# try:
#     a = 10/0
# except Exception as a:
#     logging.info('Dividing by 0 error occured!')
#     raise CustomException(a,sys)