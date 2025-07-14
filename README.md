# Discord OAuth2 Auto-Add Bot Example

This is a minimal example of how to implement Discord OAuth2 flow with the `guilds.join` scope to automatically add authorized users to a Discord server.

## Prerequisites

- Python 3.7+
- Discord Application with a bot created on the [Discord Developer Portal](https://discord.com/developers/applications)
- Flask and requests Python packages

## Setup

1. Clone or download this repository.

2. Install dependencies:

```bash
pip install flask requests
```

3. Create a Discord application and bot:

- Go to https://discord.com/developers/applications
- Create a new application or select an existing one.
- Copy the **Application ID** and set it as `CLIENT_ID` in `main.py`.
- Go to the **Bot** tab, create a bot, and copy the bot token. Set it as `BOT_TOKEN`.
- Go to the **OAuth2** tab:
  - Set the **Redirect URI** to `http://localhost:5000/callback`
  - Select the scopes: `identify` and `guilds.join`

4. Get your Discord server (guild) ID:

- Enable Developer Mode in Discord settings.
- Right-click your server icon and click "Copy ID".
- Set this as `GUILD_ID` in `main.py`.

5. Update `main.py` with your credentials:

```python
CLIENT_ID = "your_client_id_here"
CLIENT_SECRET = "your_client_secret_here"
BOT_TOKEN = "your_bot_token_here"
GUILD_ID = "your_guild_id_here"
```

## Running the app

Run the Flask app:

```bash
python main.py
```

Open your browser and go to:

```
http://localhost:5000/
```

Click "Login with Discord" and authorize the app. Upon successful authorization, you will be automatically added to the Discord server.

## Notes

- Make sure your bot has the `guilds.join` OAuth2 scope and the necessary permissions in the server.
- This example is for local testing and learning purposes. For production, consider deploying securely and handling tokens safely.

## Troubleshooting

- If you get errors related to redirect URI mismatch, double-check the Redirect URI in the Discord Developer Portal matches exactly with the one in the code.
- Ensure your bot token and client secret are kept private.

---
