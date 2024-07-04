import discord
from configuration import ConfigurationHolder
from flask import Flask, redirect, request


class DiscordApp:
    app = Flask(__name__)

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def handle_authorization_code(self, code):
        # Exchange the authorization code for an access token
        self.access_token = discord.utils.oauth_complete(
            self.client_id, self.client_secret, code
        )

    @app.route("/discord/callback")
    def discord_callback(self):
        # Get the authorization code from the query parameters
        code = request.args.get("code")

        # Handle the authorization code and exchange it for an access token
        self.handle_authorization_code(code)

        # Update configuration with new value
        self.update_access_token()

        # For now, let's just redirect back to the homepage
        return redirect("/")

    def update_access_token(self):
        ch = ConfigurationHolder()
        ch.set("Discord", "token", self.access_token)

    def run_applicaiton(self):
        self.app.run(debug=True, port=8000)
