# (c) copyright 2021-2022 by lucifeermorningstar@GitHub , < https://github.com/lucifeermorningstar >
# Special Thanks To Ak Hacker who Helped me in This. 

import os
import pathlib
import logging

from pyrogram import Client
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler



# General Details
API_ID = os.environ.get("API_ID", None) 
API_HASH = os.environ.get("API_HASH", None) 
SESSION = os.environ.get("SESSION", None) 

# StartTime
StartTime = datetime.now()

# Pyrogram Clients
app = Client(
      session_name=SESSION,
      api_id=API_ID,
      api_hash=API_HASH,
      sleep_threshold=180,
)
'''
assist = Client(
        "MyAssistant",
        api_id=API_ID,
        api_hash= API_HASH,
        bot_token=TOKEN,
        sleep_threshold=180,
    )
'''
# Extras
__version__ = "S.0.1"

# Logging at the start to catch everything From PaperPlane
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
    handlers=[
        TimedRotatingFileHandler(
            "logs/DaisyX.log",
            when="midnight",
            encoding=None,
            delay=False,
            backupCount=10,
        ),
        logging.StreamHandler(),
    ],
)
LOGS = logging.getLogger(__name__)

# Modules Loading From PaperLane
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

    async def start(self):
        await super().start()
        await super().send_message("me", "DaisyX started")

        print("DaisyX started. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("DaisyX stopped. Bye.")

    async def restart(self, *args, git_update=False, pip=False):
        """ Shoutout to the Userg team for this."""
        await self.stop()
        try:
            c_p = psutil.Process(os.getpid())
            for handler in c_p.open_files() + c_p.connections():
                os.close(handler.fd)
        except Exception as c_e:
            print(c_e)

        if git_update:
            os.system("git reset --hard")
            os.system("git pull")
        if pip:
            os.system("pip install -U -r requirements.txt")

        os.execl(sys.executable, sys.executable, "-m", self.__class__.__name__.lower())
        sys.exit()

# Scheduler
scheduler = AsyncIOScheduler()

# Global Variables
CMD_HELP = {}
client = None
name = "daisyx"
SkemX = SkemX(__version__)

