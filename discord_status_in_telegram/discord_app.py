import time

import discord
import requests
from configuration import ConfigurationHolder
from flask import Flask, Response
from logger_config import setup_logger

# Set up logging
logger = setup_logger(__name__)

# "Close page" type response
close_page_html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Authorization Complete</title>
            </head>
            <body>
                <h1>Authorization Complete</h1>
                <p>This page will close automatically in 5 seconds.</p>
                <p>If it doesn't, you can close it manually.</p>
                <script>
                    setTimeout(function() {
                        window.close();
                    }, 5000);
                </script>
            </body>
            </html>
            """


class DiscordApp:

    def __init__(self):
        logger.info("Initializing DiscordApp")
        self.ch = ConfigurationHolder()
        self.client_id = self.ch.discord.client_id
        self.client_secret = self.ch.discord.client_secret
        self.redirect_uri = self.ch.discord.redirect_uri
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

            # Print message, wait, and close
            logger.info("Closing the page")
            return Response(close_page_html_content, mimetype="text/html")

    def handle_authorization_code(self, code):
        logger.info("Handling authorization code")
        # Exchange the authorization code for an access token
        API_ENDPOINT = "https://discord.com/api/v10"

        logger.info("Requesting access token")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri.append("/discord/callback"),
        }
        logger.debug("Data: %s" % data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(
            "%s/oauth2/token" % API_ENDPOINT,
            data=data,
            headers=headers,
            auth=(self.client_id, self.client_secret),
        )
        r.raise_for_status()

        logger.debug("Response: %s" % r.json())

        # now get all data to configurationholder
        # I'll get access_token, token_type (not needed), expires_in and refresh_token
        self.token = r.json()["access_token"]
        expires_in = r.json()["expires_in"]
        self.expiration_timestamp = str(int(time.time()) + expires_in)
        self.refresh_token = r.json()["refresh_token"]

    def update_config(self):
        logger.info("Updating access token")
        self.ch.set("Discord", "token", self.token)
        logger.info("Updating expiration timestamp")
        self.ch.set("Discord", "expiration_timestamp", self.expiration_timestamp)
        logger.info("Updating refresh token")
        self.ch.set("Discord", "refresh_token", self.refresh_token)

    def run_applicaiton(self):
        logger.info("Running Discord application")
        self.app.run(debug=True, port=8000)
