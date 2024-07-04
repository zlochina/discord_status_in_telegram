import discord
from flask import Flask, redirect, request


class DiscordClient:
    def __init__(self, token, guild_id):
        intents = discord.Intents.default()
        intents.members = True
        self.client = discord.Client(intents=intents)
        self.token = token
        self.guild_id = int(guild_id)
        self.setup_events()

    def setup_events(self):
        @self.client.event
        async def on_ready(self):
            print(f"{self.client.user.name} has connected to Discord!")

    async def start(self):
        await self.client.start(self.token)

    async def close(self):
        await self.client.close()

    async def get_voice_channels_status(self):
        await self.client.login(self.token)
        guild = self.client.get_guild(self.guild_id)

        status = []
        for channel in guild.voice_channels:
            status.append(
                {
                    "name": channel.name,
                    "members": [member.name for member in channel.members],
                }
            )

        await self.client.close()
        return status


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

        # For now, let's just redirect back to the homepage
        return redirect("/")

    def run_applicaiton(self):
        self.app.run(debug=True, port=8000)
