import json
import os
import yaml
import logging
from logging import handlers


class Load_Config():
    def __init__(self, env, app_path):
        self.env = env
        print ('Reading from ENVIRONMENT')
        with open(os.path.join(app_path,'config','base.yml'), 'r') as f:
            config = yaml.load(f)
        self.config = {}
        for k, v in config['base'].items():
            self.config[k] = v
        with open(os.path.join(app_path,'config',env+'.yml'), 'r') as f:
            config = yaml.load(f)
        for k, v in config[env].items():
            self.config[k] = v	


    def __repr__(self):
        return str(self.__dict__)

    def get_logger(self):
        LOG_LEVEL = int(self.config["log_level"])
        LOG_FORMAT = "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s"
        logger = None
        log_file = self.config["log_file"]
        logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
        logger = logging.getLogger(self.config["logger_name"])
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=int(self.config["filesize"])*100,
        backupCount=int(self.config["backupcount"]))
        formatter = logging.Formatter(LOG_FORMAT)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = 0
        return logger
  
