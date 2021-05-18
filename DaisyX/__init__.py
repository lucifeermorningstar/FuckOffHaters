import os
import logging

from pyrogram import Client
from datetime import datetime


# General Details
API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
SESSION = os.environ.get("SESSION", None) 

# StartTime
StartTime = time.time()

# Pyrogram Clients
app = Client(
      session_name=SESSION,
      api_id=API_ID,
      api_hash=API_HASH,
      sleep_threshold=180,
)

assist = Client(
        "MyAssistant",
        api_id=API_ID,
        api_hash= API_HASH,
        bot_token=TOKEN,
        sleep_threshold=180,
    )

# Global Variables
CMD_HELP = {}

# Extras
version = S.0.1


