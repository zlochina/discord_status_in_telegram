import configparser

from logger_config import setup_logger

# Set up logger
logger = setup_logger("configuration")


class DiscordConfiguration:
    def __init__(self):
        self.token = ""
        self.guild_id = ""

    def set_values(self, dictionary):
        self.token = dictionary["token"]
        self.guild_id = dictionary["guild_id"]


class TelegramConfiguration:
    def __init__(self):
        self.token = ""
        self.chat_id = ""

    def set_values(self, dictionary):
        self.token = dictionary["token"]
        self.chat_id = dictionary["chat_id"]


class ConfigurationHolder:
    CONFIG_FILEPATH = "config.ini"

    def __init__(self):
        self.discord = DiscordConfiguration()
        self.telegram = TelegramConfiguration()
        self.load_config()

    def load_config(self):
        logger.info("Loading configuration")
        self.config = configparser.ConfigParser()
        logger.info(f"Reading configuration from {self.CONFIG_FILEPATH}")
        self.config.read(self.CONFIG_FILEPATH)
        logger.info("Configuration loaded successfully.")
        logger.debug(f"Configuration: {self.config}")

        self.discord.set_values(self.config["Discord"])
        self.telegram.set_values(self.config["Telegeram"])
        self.update_interval = self.config["General"]["update_interval"]

    def get_config(self):
        return self.config

    def get(self, key):
        return self.config[key]
