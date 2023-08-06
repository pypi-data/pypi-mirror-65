
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from apminsight.constants import agent_logger_name, logs_dir, base_dir, log_name, log_format

agentlogger = None

def check_and_create_dirs():
    base_path = os.path.join(os.getcwd(), base_dir)
    logs_path = os.path.join(base_path, logs_dir)

    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    
    return logs_path


def initalize():
    global agentlogger
    if agentlogger is not None:
        return

    try:
        logs_dir = check_and_create_dirs()
        log_file = os.path.join(logs_dir, log_name)
        handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024, 
                                    backupCount=10, encoding=None, delay=0)
        agentlogger = create_logger(handler)
    except Exception as e:
        print('apminsight agent log file initialization error', e)
        log_to_sysout()


def log_to_sysout():
    global agentlogger
    try:
        handler = logging.StreamHandler(sys.stdout)
        agentlogger = create_logger(handler)
    except Exception as e:
        print('not able to print apminsight agent logs to sysout', e)


def create_logger(handler):
    logger = logging.getLogger(agent_logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


initalize()
