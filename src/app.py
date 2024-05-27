import discord
from flask import Flask, redirect, request

from constants import CLIENT_ID, CLIENT_SECRET

app = Flask(__name__)


def handle_authorization_code(code):
    # Replace with your bot's client ID and client secret
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET

    # Exchange the authorization code for an access token
    access_token = discord.utils.oauth_complete(client_id, client_secret, code)

    return access_token


@app.route("/discord/callback")
def discord_callback():
    # Get the authorization code from the query parameters
    code = request.args.get("code")

    # Handle the authorization code and exchange it for an access token
    # (This part will depend on the Discord API and the library you're using)
    access_token = handle_authorization_code(code)

    # After obtaining the access token, you can use it to authenticate your bot
    # and perform actions on behalf of the user

    # For now, let's just redirect back to the homepage
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=8000)
