import time
import urllib.parse

import requests
from configuration import ConfigurationHolder
from flask import Flask, Response, request
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
API_ENDPOINT = "https://discord.com/api/v10"
OAUTH_ENDPOINT = "https://discord.com/api/oauth2/authorize"


class DiscordApp:

    def __init__(self):
        logger.info("Initializing DiscordApp")
        self.ch = ConfigurationHolder()
        self.client_id = self.ch.discord.client_id
        self.client_secret = self.ch.discord.client_secret
        self.redirect_uri = self.ch.discord.redirect_uri
        self.app = Flask(__name__)
        self.scopes = self.ch.discord.scopes
        self.permissions = self.ch.discord.permissions
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

        logger.info("Requesting access token")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri + "/discord/callback",
        }
        logger.debug("Data: %s" % data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(
            "%s/oauth2/token" % API_ENDPOINT,
            data=data,
            headers=headers,
            auth=(self.client_id, self.client_secret),
        )

        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logger.error("Response: %s" % r.json())
            logger.error("Error: %s" % e)

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

    def create_authorization_link(self):
        """
        Create the Discord authorization link and prompt the user to visit it.

        :param scopes: List of OAuth2 scopes to request
        """

        def custom_uri_encode(s):
            return urllib.parse.quote(s, safe="+")

        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri + "/discord/callback",
            "response_type": "code",
            "permissions": self.permissions,
            "integration_type": 0,
            "scope": "+".join(self.scopes),
        }

        encoded_params = "&".join(
            f"{custom_uri_encode(str(k))}={custom_uri_encode(str(v))}"
            for k, v in params.items()
        )
        auth_url = f"{OAUTH_ENDPOINT}?{encoded_params}"

        print("Please visit the following URL to authorize the application:")
        print(auth_url)
        print(
            "\nAfter authorizing, you will be redirected to a page that may not load properly."
        )
        print(
            "This is expected. You can close that page once you see the 'Authorization Complete' message."
        )

    def run_application(self):
        logger.info("Running Discord application")
        self.app.run(debug=True, port=8000)

    def start_authorization_flow(self):
        """
        Start the authorization flow by creating the link and running the Flask app.

        :param scopes: List of OAuth2 scopes to request
        """
        self.create_authorization_link()
        self.run_application()
