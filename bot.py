#(©)Codexbotz / TechVJ
import sys
import os
from datetime import datetime
from pyrogram import Client
from pyrogram.enums import ParseMode
import pyromod.listen

# Import environment config values
from config import (
    API_HASH, 
    APP_ID, 
    LOGGER, 
    TG_BOT_TOKEN, 
    TG_BOT_WORKERS, 
    FORCE_SUB_CHANNEL, 
    CHANNEL_ID, 
    PORT
)

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot_Instance",
            api_id=APP_ID,
            api_hash=API_HASH,
            bot_token=TG_BOT_TOKEN,
            workers=TG_BOT_WORKERS,
            plugins={"root": "plugins"},
            parse_mode=ParseMode.HTML
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = datetime.now()
        
        # Verify force subscription requirements if configured
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Please double check the FORCE_SUB_CHANNEL value. Make sure the Bot is Admin in that channel.")
                sys.exit()

        # Verify the File database channel configuration
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Vercel Webhook Deployment Active Check")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Bot failed to read the Storage Channel ID ({CHANNEL_ID}). Confirm the Bot is an Admin there.")
            sys.exit()

        self.LOGGER(__name__).info(f"{me.first_name} Client Initialized Successfully on Webhook Mode.")

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot Stopped.")

# Global reference mapping instantiation for app.py layout 
app = Bot()

# WARNING FOR VERCEL COMPATIBILITY:
# The native app.run() activation has been completely stripped out here.
# Vercel relies completely on app.py to route transactions dynamically.
                            
