import os
from flask import Flask, request
from pyrogram import Client, __version__
from bot import Bot  # Imports your main bot class

app = Flask(__name__)

# Initialize the Pyrogram client without starting the long-polling loop
bot_app = Bot()

@app.route('/', methods=['GET', 'POST'])
def handle_webhook():
    if request.method == 'POST':
        # Safely convert the incoming Telegram update into json
        update = request.get_json()
        if update:
            # Tell Pyrogram to process this single update instantly
            bot_app.app.process_update(update)
        return 'OK', 200
    return f"Bot is running on Pyrogram v{__version__}!", 200

# Vercel needs this entry point to serve the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
