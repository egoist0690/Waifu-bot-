import os
import requests
import asyncio
import base64
from pyrogram import Client, filters, enums
from pymongo import ReturnDocument
from gridfs import GridFS
from TEAMZYRO import application, DATABASE_ID, SUPPORT_CHAT, OWNER_ID, collection, user_collection, db, rarity_map, ZYRO, require_power, CHARA_CHANNEL_ID

IMGBB_API_KEY = "593edb35922f7a2c904ec752e2416d63"

WRONG_FORMAT_TEXT = """🌸 <b>𝐖𝐫𝐨𝐧𝐠 𝐅𝐨𝐫𝐦𝐚𝐭</b>

━━━━━━━━━━━━━━━━━━━━━

<blockquote>Please use the correct format:</blockquote>

<code>/upload character-name anime-name rarity_number</code>

<blockquote>Example:</blockquote>
<code>/upload muzan-kibutsuji Demon-slayer 3</code>

<blockquote>Available Rarities:</blockquote>
🔹 1 - ⚪️ Common
🔹 2 - 🟣 Rare
🔹 3 - 🟡 Legendary
🔹 4 - 🟢 Medium
🔹 5 - 💮 Special Edition
🔹 6 - 🔮 Limited Edition
🔹 7 - 💸 Premium Edition
🔹 8 - 🌤 Summer
🔹 9 - 🎐 Celestial
🔹 10 - ❄️ Winter
🔹 11 - 💝 Valentine
🔹 12 - 🎃 Halloween
🔹 13 - 🎄 Christmas Special
🔹 14 - 🪐 Omniversal
🔹 15 - 🎭 Cosplay Master
🔹 16 - 🧧 Events
🔹 17 - 🍑 Echhi
🔹 18 - 🎗️ AMV Edition
🔹 19 - 🌟 Luminous
🔹 20 - 🌧 Rainy
🔹 22 - 🍭 Winter event

━━━━━━━━━━━━━━━━━━━━━
💜 <b>Shinobu Kocho</b>"""

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
# SMART UPLOAD - Handles both Catbox and ImgBB
# ======================================================
def smart_upload(file_path, media_type):
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        # Try Catbox first for all files
        if media_type == "image":
            # Try ImgBB first for images
            try:
                with open(file_path, "rb") as f:
                    encoded = base64.b64encode(f.read()).decode("utf-8")

                r = requests.post(
                    "https://api.imgbb.com/1/upload",
                    data={"key": IMGBB_API_KEY, "image": encoded},
                    timeout=60
                )

                data = r.json()
                if data.get("success"):
                    return data["data"]["url"]
            except Exception as e:
                print(f"ImgBB upload failed, falling back to Catbox: {e}")

        # Fallback to Catbox
        files = {"fileToUpload": open(file_path, "rb")}
        data = {"reqtype": "fileupload"}

        r = requests.post("https://catbox.moe/user/api.php", files=files, data=data, timeout=120)

        if r.status_code == 200:
            url = r.text.strip()
            if url.startswith("https://"):
                return url

        raise Exception(f"Catbox upload failed: {r.text}")

    except Exception as e:
        raise Exception(f"Upload failed: {str(e)}")


upload_lock = asyncio.Lock()


# ======================================================
# UPLOAD COMMAND
# ======================================================
@ZYRO.on_message(filters.command(["upload"]))
@require_power("add")
async def ul(client, message):
    if upload_lock.locked():
        return await message.reply_text(
            "🌸 <i>Another upload is in progress...</i>",
            parse_mode=enums.ParseMode.HTML
        )

    async with upload_lock:
        reply = message.reply_to_message
        if not reply:
            return await message.reply_text(
                "🌸 <i>Please reply to a file/photo/video with /upload</i>",
                parse_mode=enums.ParseMode.HTML
            )

        args = message.text.strip().split()
        if len(args) != 4:
            return await client.send_message(
                message.chat.id, 
                WRONG_FORMAT_TEXT,
                parse_mode=enums.ParseMode.HTML
            )

        try:
            character_name = args[1].replace('-', ' ').title()
            anime = args[2].replace('-', ' ').title()
            rarity = int(args[3])
        except:
            return await message.reply_text(
                "🌸 <i>Invalid format. Please check your input.</i>",
                parse_mode=enums.ParseMode.HTML
            )

        if rarity not in rarity_map:
            return await message.reply_text(
                f"🌸 <i>Invalid rarity value. Available rarities: {', '.join(map(str, rarity_map.keys()))}</i>",
                parse_mode=enums.ParseMode.HTML
            )

        rarity_text = rarity_map[rarity]
        available_id = await find_available_id()

        character = {
            "name": character_name,
            "anime": anime,
            "rarity": rarity_text,
            "rarity_number": rarity,
            "id": available_id
        }

        processing_message = await message.reply_text(
            "🌸 <i>Uploading to the wisteria garden...</i>",
            parse_mode=enums.ParseMode.HTML
        )

        path = None
        thumb_path = None

        try:
            # Download media
            path = await reply.download()
            if not path:
                raise Exception("Failed to download media")

            # Handle different media types
            if reply.photo:
                url = smart_upload(path, "image")
                character["img_url"] = url

            elif reply.document:
                if "image" in reply.document.mime_type:
                    url = smart_upload(path, "image")
                    character["img_url"] = url
                else:
                    url = smart_upload(path, "video")
                    character["vid_url"] = url

            elif reply.video:
                url = smart_upload(path, "video")
                character["vid_url"] = url

                try:
                    thumbs = getattr(reply.video, "thumbs", None)
                    if thumbs:
                        thumb_path = await client.download_media(thumbs[0].file_id)
                        turl = smart_upload(thumb_path, "image")
                        character["thum_url"] = turl
                except Exception as e:
                    print(f"Thumbnail upload failed: {e}")

            else:
                raise Exception("Unsupported media type")

            caption_text = (
                f"🌸 <b>𝐖𝐢𝐬𝐭𝐞𝐫𝐢𝐚 𝐔𝐩𝐥𝐨𝐚𝐝</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📛 <b>Character:</b> {character_name}\n"
                f"⛩️ <b>Anime:</b> {anime}\n"
                f"🌈 <b>Rarity:</b> {rarity_text}\n"
                f"🆔 <b>ID:</b> {available_id}\n"
                f"👤 <b>Added by:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🦋\n"
                f"<i>\"Every butterfly finds its place\n"
                f"beneath the wisteria.\"</i>\n\n"
                f"💜 <b>Shinobu Kocho</b>"
            )

            # Send to channel
            if "img_url" in character:
                await client.send_photo(
                    CHARA_CHANNEL_ID, 
                    character["img_url"], 
                    caption=caption_text,
                    parse_mode=enums.ParseMode.HTML
                )
            elif "vid_url" in character:
                await client.send_video(
                    CHARA_CHANNEL_ID, 
                    character["vid_url"], 
                    caption=caption_text,
                    parse_mode=enums.ParseMode.HTML
                )
            else:
                await client.send_document(
                    CHARA_CHANNEL_ID, 
                    path, 
                    caption=caption_text,
                    parse_mode=enums.ParseMode.HTML
                )

            # Insert into database
            await collection.insert_one(character)

            await processing_message.edit_text(
                f"✅ <b>Character Uploaded Successfully!</b>\n\n"
                f"📛 <b>Name:</b> {character_name}\n"
                f"🆔 <b>ID:</b> {available_id}\n"
                f"🌈 <b>Rarity:</b> {rarity_text}\n\n"
                f"🦋 The butterfly has joined the garden!",
                parse_mode=enums.ParseMode.HTML
            )

        except Exception as e:
            await processing_message.edit_text(
                f"❌ <b>Upload Failed</b>\n\n"
                f"<code>{str(e)}</code>\n\n"
                f"🌸 <i>Please check your input and try again.</i>",
                parse_mode=enums.ParseMode.HTML
            )

        finally:
            # Clean up temporary files
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass
            if thumb_path and os.path.exists(thumb_path):
                try:
                    os.remove(thumb_path)
                except:
                    pass


# ======================================================
# RARITY COUNT COMMAND
# ======================================================
@ZYRO.on_message(filters.command("rarity"))
async def rarity_count(client, message):
    try:
        text = "🌸 <b>𝐖𝐢𝐬𝐭𝐞𝐫𝐢𝐚 𝐑𝐚𝐫𝐢𝐭𝐲 𝐋𝐞𝐝𝐠𝐞𝐫</b>\n"
        text += "━━━━━━━━━━━━━━━━━━━━━\n\n"

        total = 0

        for rarity_no in sorted(rarity_map.keys()):
            rarity_name = rarity_map[rarity_no]

            count = await collection.count_documents(
                {"rarity_number": rarity_no}
            )

            total += count

            # Get emoji for rarity
            rarity_emoji = {
                '⚪️ Common': '⚪',
                '🟢 Medium': '🟢',
                '🟣 Rare': '🟣',
                '🟡 Legendary': '🟡',
                '💮 Special Edition': '💮',
                '🔮 Limited Edition': '🔮',
                '💸 Premium Edition': '💸',
                '🌤 Summer': '🌤',
                '🎐 Celestial': '🎐',
                '❄️ Winter': '❄️',
                '💝 Valentine': '💝',
                '🎃 Halloween': '🎃',
                '🎄 Christmas Special': '🎄',
                '🪐 Omniversal': '🪐',
                '🎭 Cosplay Master': '🎭',
                '🧧 Events': '🧧',
                '🍑 Echhi': '🍑',
                '🎗️ AMV Edition': '🎗️',
                '🌟 Luminous': '🌟',
                '🌧 Rainy': '🌧',
                '🍭 Winter event': '🍭'
            }.get(rarity_name, '🌸')

            text += (
                f"{rarity_emoji} <b>{rarity_name}</b>\n"
                f"   ↬ {count} souls\n\n"
            )

        text += "━━━━━━━━━━━━━━━━━━━━━\n"
        text += f"🦋 <b>Total Souls</b> ↬ {total}\n\n"
        text += "<i>\"Every butterfly has its place\n"
        text += "beneath the wisteria.\"</i>\n\n"
        text += "💜 <b>Shinobu Kocho</b>"

        await message.reply_text(
            text,
            parse_mode=enums.ParseMode.HTML
        )

    except Exception as e:
        await message.reply_text(
            f"🌸 <i>Error:</i> <code>{e}</code>",
            parse_mode=enums.ParseMode.HTML
        )
