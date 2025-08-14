import logging 
import os

class LogManager:

    ERROR = logging.ERROR
    INFO = logging.INFO
    DEBUG = logging.DEBUG

    def __init__(self, logDir = "logs"):
        self.logDir = logDir
        os.makedirs(self.logDir, exist_ok=True)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def setupLogger(self, name, logFile, level=INFO):
        if logging.getLogger(name).handlers:
            return logging.getLogger(name)
        
        handler = logging.FileHandler(os.path.join(self.logDir, logFile))
        handler.setFormatter(self.formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)


        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(self.formatter)

        logger.addHandler(consoleHandler)

        return logger

