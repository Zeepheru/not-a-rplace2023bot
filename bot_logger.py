import os
import logging
import sys
from datetime import datetime

class colorFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    cformat = "%(message)s"

    FORMATS = {
        logging.DEBUG: grey + cformat + reset,
        logging.INFO: grey + cformat + reset,
        logging.WARNING: yellow + cformat + reset,
        logging.ERROR: red + cformat + reset,
        logging.CRITICAL: bold_red + cformat + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def setupLogger(enableLogFile: bool, consolelevel = "debug"):
    if not os.path.exists("logs"):
        os.makedirs("logs")

    #current logs. 
    if os.path.exists("logs/clogs.txt"):
        os.remove("logs/clogs.txt")

    logger = logging.getLogger("main")
    logger.setLevel(level=logging.DEBUG)

    fullformat = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
    message_onlyformat = logging.Formatter('%(message)s')

    #consoleHandler - all
    cH = logging.StreamHandler()
    if consolelevel == "debug":
        cH.setLevel(logging.DEBUG)
    else:
        cH.setLevel(logging.INFO)
        
    cH.setStream(sys.stdout)
    cH.setFormatter(colorFormatter())

    #fileHandler
    c_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    fH = logging.FileHandler(filename="logs/"+c_time+".txt")
    fH.setLevel(logging.DEBUG)
    fH.setFormatter(fullformat)
    #currentlogs.txt
    fH2 = logging.FileHandler(filename="logs/"+"clogs"+".txt")
    fH2.setLevel(logging.DEBUG)
    fH2.setFormatter(fullformat)

    logger.addHandler(cH)
    if enableLogFile:
        logger.addHandler(fH)
        logger.addHandler(fH2)

    return logger


def main():
    print("a")
    logger = setupLogger(consolelevel = "debug", enableLogFile=False)
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

if __name__ == "__main__":
    main()