# (c) copyright 2021-2022 by lucifeermorningstar@GitHub , < https://github.com/lucifeermorningstar >
# Special Thanks To Ak Hacker who Helped me in This. 

import os
import pathlib
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
client = None
name = "daisyx"
SkemX = SkemX(name)

# Extras
version = "S.0.1"

# Enable Logging in Pyrogram
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [DAISYXUB] - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

# Modules Loading
class SkemX(Client):
    file_path = pathlib.Path(__file__).parent
    main_directory = str(file_path.parent)
    def __init__(self, name):
        name = name.lower()

        super().__init__(
            SESSION,# if SESSION is not None else name,
            api_id=API_ID,
            api_hash=API_HASH,
            plugins=dict(root=f"{name}/plugins"),
            workdir="./",
            app_version="DaisyX S.0.1",
        )


