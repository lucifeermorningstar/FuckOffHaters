import pickle
import codecs
from random import randint
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from DaisyX import db

welcomedb = db.welcome_text
captcha_cachedb = db.captcha_cache
gbansdb =  db.gban

chat_filters_group = 1
chatbot_group = 2
karma_positive_group = 3
karma_negative_group = 4
regex_group = 5
welcome_captcha_group = 6
antiflood_group = 7
nsfw_detect_group = 8
blacklist_filters_group = 9
pipes_group = 10


def obj_to_str(object):
    if not object:
        return False
    string = codecs.encode(pickle.dumps(object), "base64").decode()
    return string


def str_to_obj(string: str):
    object = pickle.loads(codecs.decode(string.encode(), "base64"))
    return object

#Gban

async def is_gbanned_user(user_id: int) -> bool:
    user = await gbansdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True

# Captcha

async def is_captcha_on(chat_id: int) -> bool:
    chat = await captchadb.find_one({"chat_id": chat_id})
    if not chat:
        return True
    return False


async def captcha_on(chat_id: int):
    is_captcha = await is_captcha_on(chat_id)
    if is_captcha:
        return
    return await captchadb.delete_one({"chat_id": chat_id})


async def captcha_off(chat_id: int):
    is_captcha = await is_captcha_on(chat_id)
    if not is_captcha:
        return
    return await captchadb.insert_one({"chat_id": chat_id})

""" CAPTCHA CACHE SYSTEM """


async def update_captcha_cache(captcha_dict):
    pickle = obj_to_str(captcha_dict)
    await captcha_cachedb.delete_one({"captcha": "cache"})
    if not pickle:
        return
    await captcha_cachedb.update_one(
        {"captcha": "cache"}, {"$set": {"pickled": pickle}}, upsert=True
    )


async def get_captcha_cache():
    cache = await captcha_cachedb.find_one({"captcha": "cache"})
    if not cache:
        return []
    return str_to_obj(cache["pickled"])


""" WELCOME FUNCTIONS """


async def get_welcome(chat_id: int) -> str:
    text = await welcomedb.find_one({"chat_id": chat_id})
    return text["text"]


async def set_welcome(chat_id: int, text: str):
    return await welcomedb.update_one(
        {"chat_id": chat_id}, {"$set": {"text": text}}, upsert=True
    )


async def del_welcome(chat_id: int):
    return await welcomedb.delete_one({"chat_id": chat_id})

def generate_captcha():
    # Generate one letter
    def gen_letter():
        return chr(randint(65, 90))

    def rndColor():
        return (randint(64, 255), randint(64, 255), randint(64, 255))

    def rndColor2():
        return (randint(32, 127), randint(32, 127), randint(32, 127))

    # Generate a 4 letter word
    def gen_wrong_answer():
        word = ""
        for _ in range(4):
            word += gen_letter()
        return word

    # Generate 8 wrong captcha answers
    wrong_answers = []
    for _ in range(8):
        wrong_answers.append(gen_wrong_answer())

    width = 80 * 4
    height = 100
    correct_answer = ""
    font = ImageFont.truetype("logs/fonts/arial.ttf", 55)
    file = f"assets/{randint(1000, 9999)}.jpg"
    image = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw random points on image
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())

    for t in range(4):
        letter = gen_letter()
        correct_answer += letter
        draw.text((60 * t + 50, 15), letter, font=font, fill=rndColor2())
    image = image.filter(ImageFilter.BLUR)
    image.save(file, "jpeg")
    return [file, correct_answer, wrong_answers]
