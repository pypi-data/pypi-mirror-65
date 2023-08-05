import logging
import logging.config
import os
import inspect
import time

import openlab.credentials as credentials

#import user settings
log = credentials.log
log_level = credentials.log_level

#Get the location of the installed OpenLab Library
current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

#Save log to same directory tree as openlab module
log_file = "openlab.log"
log_path = os.path.join(current_directory, log_file)

# Remove old log first
with open(log_path, 'w') as f:
    f.write('')

def setUpRootLog():
    """
    Sets up root log when none are present:
    Retrives log and log_level from openlab.credentials.py
    If log == true, console uses log_level, and file logger uses DEBUG
    If log == false, log_level for both handlers are overriden to critical
    File log path uses <openlab directory>.openlab.log and it gets overwridden everytime
    """
    level = log_level
    if log is False:
        level = logging.CRITICAL
    
    rootLogger = logging.getLogger('')
    
    # Check if there are already root handlers. Otherwise we duplicate logs
    if len(rootLogger.handlers) == 0:
        # Create File Handler and Console Handler
        fh = logging.FileHandler(log_path)
        ch = logging.StreamHandler()

        # Formatter for file(f) and console(c) handlers
        fh_fmt = '%(asctime)s.%(msecs)03d  [%(levelname)s] %(name)s<%(module)s.%(funcName)s> - %(message)s'
        fh_datefmt = '%Y-%m-%d %H:%M:%S'
        fh_formatter = logging.Formatter(fh_fmt, fh_datefmt)

        ## Saved for later maybe ##
        ## When level is default and openlab is root logger, just print normal
        #if level == logging.INFO:
        #    ch_fmt = '%(message)s'
        #else:
        #    ch_fmt = '%(asctime)s [%(levelname)s] %(message)s'

        ch_fmt = '%(asctime)s [%(levelname)s] %(message)s'
        ch_datefmt = '%H:%M:%S'
        ch_formatter = logging.Formatter(ch_fmt, ch_datefmt)

        # Finish setup                
        fh.setLevel(level)
        fh.setFormatter(fh_formatter)
        
        ch.setLevel(level)
        ch.setFormatter(ch_formatter)
        
        rootLogger.addHandler(fh)
        rootLogger.addHandler(ch)
        
    return


def makeLogger(name):
    """
    Returns a logger with settings from openlab.credentials.py.
    No handlers are attached so setUpRootLog() must be called locally
    """
    # Create a logger
    logger = logging.getLogger(name)
    
    # Override log_level if log is set to False
    level = log_level
    if log is False:
        level = logging.CRITICAL
    
    logger.setLevel(level)
    
    return logger