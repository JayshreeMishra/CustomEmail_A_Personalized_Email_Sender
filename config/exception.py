import sys

def error_message_detail(error, error_detail:sys):
   
    _, _, exc_tb = error_detail.exc_info()        #the variable exc_tb will provide in which and line the exception has occured

    file_name = exc_tb.tb_frame.f_code.co_filename
    
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class CustomException(Exception):
    def __init__(self, message, sys_module):
        super().__init__(message)
        self.error_message = self.get_error_message(message, sys_module)

    @staticmethod
    def get_error_message(message, sys_module):
        _, _, exc_tb = sys_module.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error in script '{file_name}' at line {line_number}: {message}"

    def __str__(self):
        return self.error_message

    