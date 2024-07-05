import configparser

from logger_config import setup_logger

# Set up logger
logger = setup_logger("configuration")


class DiscordConfiguration:
    def __init__(self):
        self.token = None
        self.guild_id = None
        self.client_id = None
        self.client_secret = None
        self.redirect_uri = None
        self.refresh_token = None
        self.expiration_timestamp = None

    def set_values(self, dictionary):
        self.token = dictionary.get("token", None)
        self.guild_id = dictionary.get("guild_id", None)
        self.client_id = dictionary.get("client_id", None)
        self.client_secret = dictionary.get("client_secret", None)
        self.redirect_uri = dictionary.get("redirect_uri", None)
        self.refresh_token = dictionary.get("refresh_token", None)
        self.expiration_timestamp = dictionary.get("expiration_timestamp", None)


class TelegramConfiguration:
    def __init__(self):
        self.token = ""
        self.chat_id = ""

    def set_values(self, dictionary):
        self.token = dictionary.get("token", "")
        self.chat_id = dictionary.get("chat_id", "")


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

        logger.info("Setting configuration values")
        self.discord.set_values(self.config["Discord"])
        self.telegram.set_values(self.config["Telegram"])
        self.update_interval = self.config["General"]["update_interval"]

        logger.debug(
            f"""Configuration values:
Discord:
    token: {self.discord.token}
    guild_id: {self.discord.guild_id}
    client_id: {self.discord.client_id}
    client_secret: {self.discord.client_secret}
    redirect_uri: {self.discord.redirect_uri}
    refresh_token: {self.discord.refresh_token}
    expiration_timestamp: {self.discord.expiration_timestamp}
Telegram:
    token: {self.telegram.token}
    chat_id: {self.telegram.chat_id}
General:
    update_interval: {self.update_interval}
                     """
        )

    def get_config(self):
        return self.config

    def get(self, key):
        return self.config[key]

    def set(self, section, key, value):
        logger.info(f"Setting {key} in section {section}")
        logger.debug(f"Setting {key} to {value} in section {section}")
        # add a new section if it doesnt exist
        if section not in self.config:
            self.config[section] = {}

        # add/update a key-value pair
        self.config[section][key] = value

        # update configuration file
        with open(self.CONFIG_FILEPATH, "w") as configfile:
            self.config.write(configfile)
        logger.info("Configuration updated successfully.")
