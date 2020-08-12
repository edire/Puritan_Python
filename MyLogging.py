

import os
import logging
import datetime as dt



file_name = 'log_' + str(dt.datetime.today().strftime('%Y%m%d_%H%M%S')) + '.txt'
directory = os.path.join(os.getcwd(), 'logs')


def LogDirectory(directory_new):
    global directory
    directory = directory_new


def NewLogger(logger_name):
    if not os.path.exists(directory):
        os.makedirs(directory)
    log_file =  os.path.join(directory, file_name)
    
    logger = logging.getLogger(logger_name)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

    
def SetLoggingLevel(log_level):
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(log_level)


#NOTSET 0
#DEBUG 10
#INFO 20
#WARNING 30
#ERROR 40
#CRITICAL 50