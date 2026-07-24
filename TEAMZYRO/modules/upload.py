# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

import os
import requests
from bson.objectid import ObjectId
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from TEAMZYRO import app as ZYRO, DATABASE_ID, db, collection, require_power, rarity_map

# Define wrong format message
WRONG_FORMAT_TEXT = """🌸 <b>𝐖𝐫𝐨𝐧𝐠 𝐅𝐨𝐫𝐦𝐚𝐭</b>

━━━━━━━━━━━━━━━━━━━━━

<blockquote>Please use the correct format:</blockquote>

<code>/addchar character-name anime-name</code>

<blockquote>Example:</blockquote>
<code>/addchar muzan-kibutsuji Demon-slayer</code>

━━━━━━━━━━━━━━━━━━━━━
💜 <b>Shinobu Kocho</b>"""

upload_collection = db.uploads

# Catbox upload function
def upload_to_catbox(file_path=None, file_url=None, expires=None, secret=None):
    url = "https://catbox.moe/user/api.php"
    with open(file_path, "rb") as file:
        response = requests.post(
            url,
            data={"reqtype": "fileupload"},
            files={"fileToUpload": file}
        )
        if response.status_code == 200 and response.text.startswith("https"):
            return response.text.strip()
        else:
            raise Exception(f"Error uploading to Catbox: {response.text}")

# Find next available ID
async def find_available_id():
    cursor = collection.find().sort('id', 1)
    ids = []
    async for doc in cursor:
        if 'id' in doc:
            try:
                ids.append(int(doc['id']))
            except:
                continue
    if ids:
        return str(max(ids) + 1).zfill(2)
    return '01'

# Command: /addchar
@ZYRO.on_message(filters.command(["addchar"]))
async def request_upload(client, message):
    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.document):
        return await message.reply_text(
            "🌸 <i>Please reply to a photo or document.</i>",
            parse_mode=enums.ParseMode.HTML
        )

    args = message.text.split()
    if len(args) != 3:
        return await message.reply_text(
            WRONG_FORMAT_TEXT,
            parse_mode=enums.ParseMode.HTML
        )

    processing_message = await message.reply(
        "🌸 <i>Processing your request...</i>",
        parse_mode=enums.ParseMode.HTML
    )

    character_name = args[1].replace('-', ' ').title()
    anime = args[2].replace('-', ' ').title()
    path = await reply.download()

    try:
        from TEAMZYRO.modules.upload import get_user_server, upload_to_catbox, upload_to_imgbb
        server = await get_user_server(message.from_user.id)

        # Check if document is a non-image
        is_doc_non_image = False
        if reply.document:
            mime = getattr(reply.document, "mime_type", "") or ""
            if not mime.startswith("image/"):
                is_doc_non_image = True

        if server == "imgbb" and not is_doc_non_image:
            try:
                catbox_url = upload_to_imgbb(path)
            except Exception:
                catbox_url = upload_to_catbox(path)
        else:
            catbox_url = upload_to_catbox(path)

        upload_data = {
            'name': character_name,
            'anime': anime,
            'img_url': catbox_url,
            'requested_by': {
                'id': message.from_user.id,
                'name': message.from_user.first_name
            }
        }

        result = await upload_collection.insert_one(upload_data)

        # Build rarity buttons (4 per row)
        rarity_buttons = []
        rarity_items = list(rarity_map.items())
        for i in range(0, len(rarity_items), 4):
            row = [
                InlineKeyboardButton(text=value, callback_data=f"rarity_{result.inserted_id}_{key}")
                for key, value in rarity_items[i:i+4]
            ]
            rarity_buttons.append(row)

        # Cancel button
        rarity_buttons.append([InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{result.inserted_id}")])

        keyboard = InlineKeyboardMarkup(rarity_buttons)

        await client.send_photo(
            chat_id=DATABASE_ID,
            photo=catbox_url,
            caption=(
                f"🌸 <b>𝐖𝐢𝐬𝐭𝐞𝐫𝐢𝐚 𝐔𝐩𝐥𝐨𝐚𝐝 𝐑𝐞𝐪𝐮𝐞𝐬𝐭</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📛 <b>Character:</b> {character_name}\n"
                f"⛩️ <b>Anime:</b> {anime}\n"
                f"👤 <b>Requested by:</b> <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>\n\n"
                f"<blockquote>Select a rarity to upload the character or cancel the request:</blockquote>"
            ),
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.HTML
        )

        await processing_message.edit_text(
            "✅ <b>Request submitted successfully!</b>\n\n"
            "🦋 The wisteria spirits will review your offering.",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        await processing_message.edit_text(
            f"❌ <b>Upload failed.</b>\n\n"
            f"<code>{str(e)}</code>",
            parse_mode=enums.ParseMode.HTML
        )
    finally:
        try:
            os.remove(path)
        except:
            pass

@ZYRO.on_callback_query(filters.create(lambda _, __, q: q.data.startswith("cancel_")))
@require_power("add")
async def handle_cancel(client, callback_query):
    try:
        _, request_id = callback_query.data.split("_")
        result = await upload_collection.delete_one({"_id": ObjectId(request_id)})

        if result.deleted_count > 0:
            await callback_query.edit_message_caption(
                caption="❌ <b>Request Canceled</b>\n\n"
                       "The upload request has been canceled.",
                reply_markup=None,
                parse_mode=enums.ParseMode.HTML
            )
            await callback_query.answer("Request canceled successfully.")
        else:
            await callback_query.answer("Request not found or already processed.", show_alert=True)
    except Exception as e:
        print(f"Error in handle_cancel: {str(e)}")
        await callback_query.answer("An error occurred while canceling the request.", show_alert=True)

@ZYRO.on_callback_query(filters.create(lambda _, __, q: q.data.startswith("rarity_")))
@require_power("app")
async def handle_callback(client, callback_query):
    try:
        _, request_id, new_rarity = callback_query.data.split("_")
        new_rarity = int(new_rarity)
        new_rarity_text = rarity_map[new_rarity]

        request = await upload_collection.find_one({"_id": ObjectId(request_id)})
        if not request:
            return await callback_query.answer("Request not found or already processed.", show_alert=True)

        available_id = await find_available_id()
        request['id'] = available_id
        request['rarity'] = new_rarity_text

        await collection.insert_one(request)
        await upload_collection.delete_one({"_id": ObjectId(request_id)})

        await callback_query.edit_message_caption(
            caption=(
                f"🌸 <b>𝐖𝐢𝐬𝐭𝐞𝐫𝐢𝐚 𝐔𝐩𝐥𝐨𝐚𝐝 𝐂𝐨𝐦𝐩𝐥𝐞𝐭𝐞</b>\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"✅ <b>Character Uploaded Successfully</b>\n\n"
                f"📛 <b>Name:</b> {request['name']}\n"
                f"⛩️ <b>Anime:</b> {request['anime']}\n"
                f"🌈 <b>Rarity:</b> {new_rarity_text}\n"
                f"🆔 <b>ID:</b> {available_id}\n"
                f"👤 <b>Uploaded by:</b> <a href='tg://user?id={callback_query.from_user.id}'>{callback_query.from_user.first_name}</a>\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🦋\n"
                f"<i>\"Every butterfly finds its place\n"
                f"beneath the wisteria.\"</i>\n\n"
                f"💜 <b>Shinobu Kocho</b>"
            ),
            reply_markup=None,
            parse_mode=enums.ParseMode.HTML
        )

        await callback_query.answer(f"Character uploaded with rarity: {new_rarity_text}")
    except Exception as e:
        print(f"Error in handle_callback: {str(e)}")
        await callback_query.answer("An error occurred while processing the request.", show_alert=True)

# Command: /rarity
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
                '🎐 Enchanted': '🎐',
                '❄️ Frozen': '❄️',
                '💝 Romantic': '💝',
                '🎃 Haunted': '🎃',
                '🎄 Chrimsum': '🎄',
                '🧧 Festive': '🧧',
                '🍑 Naughty': '🍑',
                '🎗️ AMV Edition': '🎗️',
                '🌧 Cloudy': '🌧',
                '🦠 Mythgard': '🦠'
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
