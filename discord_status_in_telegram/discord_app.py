import discord
import requests
from configuration import ConfigurationHolder
from flask import Flask, redirect, request
from logger_config import setup_logger

# Set up logging
logger = setup_logger(__name__)


class DiscordApp:

    def __init__(self):
        logger.info("Initializing DiscordApp")
        self.ch = ConfigurationHolder()
        self.client_id = self.ch.discord.client_id
        self.client_secret = self.ch.discord.client_secret
        self.redirect_uri = self.ch.discord.redirect_uri
        self.access_token = None
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/discord/callback")
        def discord_callback():
            logger.info("Handling Discord callback")
            # Get the authorization code from the query parameters
            code = request.args.get("code")

            # Handle the authorization code and exchange it for an access token
            self.handle_authorization_code(code)

            # Update configuration with new value
            self.update_config()

            # For now, let's just redirect back to the homepage
            return redirect("/")

    def handle_authorization_code(self, code):
        logger.info("Handling authorization code")
        # Exchange the authorization code for an access token
        API_ENDPOINT = "https://discord.com/api/v10"

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(
            "%s/oauth2/token" % API_ENDPOINT,
            data=data,
            headers=headers,
            auth=(self.client_id, self.client_secret),
        )
        r.raise_for_status()

        # now get all data to configurationholder
        # TODO

    def update_config(self):
        logger.info("Updating access token")
        self.ch.set("Discord", "token", self.access_token)
        logger.info("Updating something")

    def run_applicaiton(self):
        logger.info("Running Discord application")
        self.app.run(debug=True, port=8000)
