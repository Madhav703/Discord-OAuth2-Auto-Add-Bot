from flask import Flask, request, redirect, session, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
GUILD_ID = os.getenv("GUILD_ID")
BOT_TOKEN = os.getenv("BOT_TOKEN")

OAUTH_SCOPE = "identify guilds.join"

DISCORD_API_BASE_URL = "https://discord.com/api"

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login")
def login():
    discord_oauth_url = (
        f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&response_type=code&scope={OAUTH_SCOPE}"
    )
    return redirect(discord_oauth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code provided", 400

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": OAUTH_SCOPE,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = requests.post(f"{DISCORD_API_BASE_URL}/oauth2/token", data=data, headers=headers)
    r.raise_for_status()
    token_data = r.json()
    access_token = token_data["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    user_resp = requests.get(f"{DISCORD_API_BASE_URL}/users/@me", headers=headers)
    user_resp.raise_for_status()
    user = user_resp.json()

    
    add_guild_url = f"{DISCORD_API_BASE_URL}/guilds/{GUILD_ID}/members/{user['id']}"
    add_guild_headers = {
        "Authorization": f"Bot {BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    add_guild_data = {
        "access_token": access_token
    }
    add_resp = requests.put(add_guild_url, json=add_guild_data, headers=add_guild_headers)
    if add_resp.status_code == 201 or add_resp.status_code == 204:
        return f"Successfully added {user['username']} to the server!"
    else:
        return f"Failed to add user: {add_resp.status_code} - {add_resp.text}"

if __name__ == "__main__":
    app.run(debug=True)
