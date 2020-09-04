

import os
import logging
import datetime as dt



file_name = 'log_' + str(dt.datetime.today().strftime('%Y-%m-%d')) + '.txt'
# '%Y%m%d_%H%M%S'
directory = os.path.join(os.getcwd(), 'logs')
log_level = 20


def LogDirectory(directory_new):
    global directory
    directory = os.path.join(directory_new, 'logs')


def LogLevel(level_new):
    global log_level
    log_level = level_new


def NewLogger(logger_name, use_cd=False):
    if use_cd:
        LogDirectory(os.path.dirname(logger_name))
    if not os.path.exists(directory):
        os.makedirs(directory)
    log_file =  os.path.join(directory, file_name)

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s: %(name)s: %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


def SetLoggingLevel(log_level):
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(log_level)



# MyLogging.LogDirectory(os.path.dirname(__file__))
# logger = MyLogging.NewLogger(__file__)

#NOTSET 0
#DEBUG 10
#INFO 20
#WARNING 30
#ERROR 40
#CRITICAL 50





### Add computer name to log example


# import logging
# import socket

# class HostnameFilter(logging.Filter):
#     hostname = socket.gethostname()

#     def filter(self, record):
#         record.hostname = HostnameFilter.hostname
#         return True


# logger = logging.getLogger()
# logger.setLevel(20)
# stream_handler = logging.StreamHandler()
# stream_handler.addFilter(HostnameFilter())
# formatter = logging.Formatter('%(asctime)s %(hostname)s: %(levelname)s: %(message)s')
# stream_handler.setFormatter(formatter)
# logger.addHandler(stream_handler)

# logger.info('test')