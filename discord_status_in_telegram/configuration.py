import configparser

from logger_config import setup_logger

# Set up logger
logger = setup_logger("configuration")


class ConfigurationHolder:
    CONFIG_FILEPATH = "config.ini"

    def __init__(self):
        self.config = {}
        self.load_config()

    def load_config(self):
        logger.info("Loading configuration")
        self.config = configparser.ConfigParser()
        logger.info(f"Reading configuration from {self.CONFIG_FILEPATH}")
        self.config.read(self.CONFIG_FILEPATH)
        logger.info("Configuration loaded successfully.")
        logger.debug(f"Configuration: {self.config}")

    def get_config(self):
        return self.config

    def get(self, key):
        return self.config[key]
