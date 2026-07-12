import os
import requests
import asyncio
import base64
from pyrogram import Client, filters
from pymongo import ReturnDocument
from gridfs import GridFS
from TEAMZYRO import application, DATABASE_ID, SUPPORT_CHAT, OWNER_ID, collection, user_collection, db, rarity_map, ZYRO, require_power, CHARA_CHANNEL_ID

IMGBB_API_KEY = "593edb35922f7a2c904ec752e2416d63"


WRONG_FORMAT_TEXT = """Wrong ❌ format...  eg. /upload reply to photo muzan-kibutsuji Demon-slayer 3

rarity_map = {
    1: "⚪️ Common",
    2: "🟣 Rare",
    3: "🟡 Legendary",      
    4: "🟢 Medium",  
    5: "💮 Special Edition", 
    6: "🔮 Limited Edition", 
    7: "💸 Premium Edition", 
    8: "🌤 Summer",
    9: "🎐 Celestial", 
    10: "❄️ Winter", 
    11: "💝 Valentine", 
    12: "🎃 Halloween", 
    13: "🎄 Christmas Special", 
    14: "🪐 Omniversal", 
    15: "🎭 Cosplay Master 🎭",
    16: "🧧 Events",
    17: "🍑 Echhi",
    18: "🎗️ AMV Edition",
    19: "🌟 Luminous",
    20: "🌧 Rainy",
    22: "🍭 Winter event",
}
"""


# ======================================================
# FIND NEXT ID
# ======================================================
async def find_available_id():
    cursor = collection.find().sort("id", 1)
    ids = []
    async for doc in cursor:
        if "id" in doc:
            try:
                ids.append(int(doc["id"]))
            except:
                continue

    ids.sort()
    for i in range(1, len(ids) + 2):
        if i not in ids:
            return str(i).zfill(2)

    return str(len(ids) + 1).zfill(2)


# ======================================================
#    🔥 FIXED: DIRECT URL GENERATOR (Telegram-safe)
# ======================================================
def smart_upload(file_path, media_type):

    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError("file_path missing")

    # ======================= IMAGE → IMGBB =======================
    if media_type == "image":
        with open(file_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        r = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": IMGBB_API_KEY, "image": encoded},
            timeout=60
        )

        data = r.json()
        if data.get("success"):
            # ✔ Direct media URL
            return data["data"]["url"]

        raise Exception("ImgBB upload failed")

    # ======================= VIDEO / DOC → CATBOX =======================
    else:
        files = {"fileToUpload": open(file_path, "rb")}
        data = {"reqtype": "fileupload"}

        r = requests.post("https://catbox.moe/user/api.php", files=files, data=data, timeout=120)

        if r.status_code == 200:
            url = r.text.strip()

            # ✔ FIXED — Telegram accepts ONLY direct file URLs
            if url.startswith("https://files.catbox.moe/"):
                return url

        raise Exception("CatBox upload failed")


upload_lock = asyncio.Lock()


# ======================================================
# UPLOAD COMMAND
# ======================================================
@ZYRO.on_message(filters.command(["upload"]))
@require_power("add_character")
async def ul(client, message):

    if upload_lock.locked():
        return await message.reply_text("Another upload is in progress...")

    async with upload_lock:

        reply = message.reply_to_message
        if not reply:
            return await message.reply_text("Reply to a file/photo/video with /upload")

        args = message.text.strip().split()
        if len(args) != 4:
            return await client.send_message(message.chat.id, WRONG_FORMAT_TEXT)

        try:
            character_name = args[1].replace('-', ' ').title()
            anime = args[2].replace('-', ' ').title()
            rarity = int(args[3])
        except:
            return await message.reply_text("Invalid format")

        if rarity not in rarity_map:
            return await message.reply_text("Invalid rarity value")

        rarity_text = rarity_map[rarity]
        available_id = await find_available_id()

        character = {
            "name": character_name,
            "anime": anime,
            "rarity": rarity_text,
            "rarity_number": rarity,
            "id": available_id
        }

        processing_message = await message.reply_text("ᴜᴘʟᴏᴀᴅɪɴɢ....")

        path = None
        thumb_path = None

        try:
            # download media
            path = await reply.download()
            if not path:
                raise Exception("Failed to download media")

            # IMAGE
            if reply.photo:
                url = smart_upload(path, "image")
                character["img_url"] = url

            # DOCUMENT
            elif reply.document:
                if "image" in reply.document.mime_type:
                    url = smart_upload(path, "image")
                    character["img_url"] = url
                else:
                    url = smart_upload(path, "video")
                    character["vid_url"] = url

            # VIDEO
            elif reply.video:
                url = smart_upload(path, "video")
                character["vid_url"] = url

                try:
                    thumbs = getattr(reply.video, "thumbs", None)
                    if thumbs:
                        thumb_path = await client.download_media(thumbs[0].file_id)
                        turl = smart_upload(thumb_path, "video")
                        character["thum_url"] = turl
                except:
                    pass

            caption_text = (
                f"Character Name: {character_name}\n"
                f"Anime Name: {anime}\n"
                f"Rarity: {rarity_text}\n"
                f"ID: {available_id}\n"
                f"Added by [{message.from_user.first_name}](tg://user?id={message.from_user.id})"
            )

            # SEND TO CHANNEL
            if "img_url" in character:
                await client.send_photo(CHARA_CHANNEL_ID, character["img_url"], caption=caption_text)

            elif "vid_url" in character:
                await client.send_video(CHARA_CHANNEL_ID, character["vid_url"], caption=caption_text)

            else:
                await client.send_document(CHARA_CHANNEL_ID, path, caption=caption_text)

            await collection.insert_one(character)

            await message.reply_text(
                f"➲ Added By: {message.from_user.first_name}\n"
                f"➥ ID: {available_id}\n"
                f"➥ {character_name}"
            )

        except Exception as e:
            await message.reply_text(f"Character Upload Unsuccessful. Error: {e}")

        finally:
            if path and os.path.exists(path): os.remove(path)
            if thumb_path and os.path.exists(thumb_path): os.remove(thumb_path)

            try: await processing_message.delete()
            except: pass