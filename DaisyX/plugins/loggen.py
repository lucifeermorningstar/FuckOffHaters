

from bs4 import *
import shutil
import requests
import os
import base64
import sys
import random
import requests
from pyrogram import filters

from DaisyX import SkemX, command
from DaisyX.functions.basic_helpers import edit_or_reply, get_text


def download_images(images): 
    count = 0
    print(f"Total {len(images)} Image Found!") 
    if len(images) != 0:
        for i, image in enumerate(images):
            try:
                image_link = image["data-srcset"] 
            except: 
                try: 
                    image_link = image["data-src"] 
                except:
                    try:
                        image_link = image["data-fallback-src"] 
                    except:
                        try:
                            image_link = image["src"] 
                        except: 

                            pass
            try: 
                r = requests.get(image_link).content 
                try:

                    r = str(r, 'utf-8')
                except UnicodeDecodeError:
                    with open("logo@DaisyXOT.jpg", "wb+") as f: 
                        f.write(r)
                    count += 1
            except: 
                pass


def mainne(name, typeo):
    url = f"https://www.brandcrowd.com/maker/logos?text={name}&searchtext={typeo}&searchService="
    r = requests.get(url) 
    soup = BeautifulSoup(r.text, 'html.parser') 
    images = soup.findAll('img') 
    random.shuffle(images)
    if images is not None:
       print("level 1 pass")
    download_images(images)


@SkemX.on_message(command("logogen") & filters.me) 
async def logogen(client, message):
    pablo = await edit_or_reply(message, "`Creating The Logo.....`")
    Godzilla = get_text(message)
    if not Godzilla:
        await pablo.edit("`Please Give Me A Valid Input. You Can Check Help Menu To Know More!`")
        return
    lmao = Godzilla.split(":", 1)
    try:
        typeo = lmao[1]
    except BaseException:
        typeo = "name"
        await pablo.edit(
             "Give name and type for logo Idiot. like `.logogen messi:football`")
    name = lmao[0]
    mainne(name, typeo)
    caption = "<b>Logo Generated By DaisyX. Get DaisyX From @DaisyXOT<b>"
    pate = "logo@DaisyXOT.jpg"
    await client.send_photo(message.chat.id, pate)
    try:
        os.remove(pate)
    except:
        pass
    await pablo.delete()


