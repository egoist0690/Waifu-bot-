import os
import importlib.util
import random
import time
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from TEAMZYRO import *
from TEAMZYRO.unit.zyro_help import HELP_DATA  

# 🔹 Function to Calculate Uptime
START_TIME = time.time()

def get_uptime():
    uptime_seconds = int(time.time() - START_TIME)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}h {minutes}m {seconds}s"

# START_MEDIA is imported from TEAMZYRO package

# 🔹 Function to Generate Private Start Message & Buttons (Shinobu Custom Design)
async def generate_start_message(client, message):
    bot_user = await client.get_me()
    bot_name = bot_user.first_name
    ping = round(time.time() - message.date.timestamp(), 2)
    uptime = get_uptime()

    caption = (
        f"<tg-emoji custom_emoji_id=\"5213273001205874214\">🌸</tg-emoji> <b>ᴀʀᴀ ᴀʀᴀ~ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ!</b> <tg-emoji custom_emoji_id=\"5213273001205874214\">🌸</tg-emoji>\n\n"
        f"<i>ɪ ᴀᴍ {bot_name}. ɪᴛ sᴇᴇᴍs ʏᴏᴜ'ᴠᴇ ᴡᴀɴᴅᴇʀᴇᴅ sᴛʀᴀɪɢʜᴛ ɪɴᴛᴏ ᴍʏ ʟᴀʙᴏʀᴀᴛᴏʀʏ. ᴅᴏɴ'ᴛ ᴡᴏʀʀʏ, ᴛʜᴇ ғʀᴇsʜ ᴡɪsᴛᴇʀɪᴀ ғʀᴀɢʀᴀɴᴄᴇ ᴡɪʟʟ ᴋᴇᴇᴘ ʏᴏᴜ sᴀғᴇ ғʀᴏᴍ ᴀɴʏ ɴᴀsᴛʏ ᴅᴇᴍᴏɴs ʜᴇʀᴇ.</i>\n\n"
        f"<blockquote>━━━━━━━▧▣▧━━━━━━━\n"
        f"<tg-emoji custom_emoji_id=\"5213273001205874214\">⦾</tg-emoji> <b>ᴍɪssɪᴏɴ:</b> ɪ ᴛʀᴀᴄᴋ ᴅᴏᴡɴ ʀᴏᴀᴍɪɴɢ sʟᴀʏᴇʀs ᴀɴᴅ ᴛʀᴀᴘ ᴡᴀɴᴅᴇʀɪɴɢ ᴅᴇᴍᴏɴs ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛs.\n"
        f"<tg-emoji custom_emoji_id=\"5213273001205874214\">⦾</tg-emoji> <b>ᴛʀᴀɪɴɪɴɢ:</b> ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴜsᴇ /help ᴛᴏ ʀᴇᴀᴅ ᴍʏ ᴄᴜsᴛᴏᴍ ᴛʀᴀɪɴɪɴɢ ᴍᴀɴᴜᴀʟs.\n"
        f"━━━━━━━▧▣▧━━━━━━━\n"
        f"<tg-emoji custom_emoji_id=\"5213273001205874214\">⚡</tg-emoji> <b>ᴘᴜʟsᴇ:</b> <code>{ping}</code> ᴍs\n"
        f"<tg-emoji custom_emoji_id=\"5213273001205874214\">⏳</tg-emoji> <b>ʀᴇsᴛ ᴢᴏɴᴇ:</b> <code>{uptime}</code></blockquote>"
    )

    buttons = [
        [InlineKeyboardButton("<tg-emoji custom_emoji_id=\"5213273001205874214\">🦋</tg-emoji> ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [
            InlineKeyboardButton("<tg-emoji custom_emoji_id=\"5213273001205874214\">💜</tg-emoji> sᴜᴘᴘᴏʀᴛ", url="https://t.me/+fPjchISAGnc3OGJl"),
            InlineKeyboardButton("<tg-emoji custom_emoji_id=\"5213273001205874214\">📢</tg-emoji> ᴜᴘᴅᴀᴛᴇs", url="https://t.me/+wjJbHQ9DQzM1OTE1")
        ],
        [
            InlineKeyboardButton("<tg-emoji custom_emoji_id=\"5213273001205874214\">🧪</tg-emoji> ʜᴇʟᴘ", callback_data="open_help"),
            InlineKeyboardButton("<tg-emoji custom_emoji_id=\"5213273001205874214\">👤</tg-emoji> ᴏᴡɴᴇʀ", url=f"https://t.me/EGOIST_6969")
        ]
    ]

    return caption, buttons

# 🔹 Function to Generate Group Start Message & Buttons (Shinobu Custom Design)
async def generate_group_start_message(client):
    bot_user = await client.get_me()
    caption = (
        f"<tg-emoji custom_emoji_id=\"5213273001205874214\">🦋</tg-emoji> <i>ғʟᴀᴘ, ғʟᴀᴘ... ɪ ᴀᴍ</i> <b>{bot_user.first_name}</b> <tg-emoji custom_emoji_id=\"5213273001205874214\">🌸</tg-emoji>\n\n"
        f"<blockquote>ɪ ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ ᴍᴏɴɪᴛᴏʀɪɴɢ ᴛʜɪs ᴄʜᴀᴛ ᴀʀᴇᴀ ᴛᴏ ᴅᴇᴛᴇᴄᴛ ᴀɴᴅ ᴇxᴘᴏsᴇ ʜɪᴅᴅᴇɴ ᴅᴇᴍᴏɴs ᴛʜʀᴏᴜɢʜ ᴍᴇssᴀɢᴇ ғʟᴏᴡs.\n\n"
        f"ᴜsᴇ /help ᴛᴏ ᴀᴄᴄᴇss ᴍʏ sᴘᴇᴄɪᴀʟɪᴢᴇᴅ ᴍᴇᴅɪᴄᴀʟ ᴀɴᴅ ᴄᴏᴍʙᴀᴛ ᴍᴀɴᴜᴀʟs!</blockquote>"
    )
    buttons = [
        [
            InlineKeyboardButton("<tg-emoji custom_emoji_id=\"5213273001205874214\">💜</tg-emoji> sᴜᴘᴘᴏʀᴛ", url="https://t.me/+fPjchISAGnc3OGJl"),
            InlineKeyboardButton("<tg-emoji custom_emoji_id=\"5213273001205874214\">📢</tg-emoji> ᴜᴘᴅᴀᴛᴇs", url="https://t.me/+wjJbHQ9DQzM1OTE1")
        ]
    ]
    return caption, buttons

# 🔹 Send Media (Helper)
async def send_media_message(message, media, caption, buttons):
    if media.lower().endswith(('.png', '.jpg', '.jpeg')):
        await message.reply_photo(photo=media, caption=caption, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML)
    elif media.lower().endswith('.gif'):
        await message.reply_animation(animation=media, caption=caption, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply_video(video=media, caption=caption, reply_markup=InlineKeyboardMarkup(buttons), parse_mode=enums.ParseMode.HTML)

# 🔹 Private Start Command Handler
@app.on_message(filters.command("start") & filters.private)
async def start_private_command(client, message):
    existing_user = await user_collection.find_one({"id": message.from_user.id})

    if not existing_user:
        user_data = {
            "id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "start_time": time.time()
        }
        await user_collection.insert_one(user_data)

    caption, buttons = await generate_start_message(client, message)
    media = random.choice(START_MEDIA)

    await app.send_message(
        chat_id=BOT_LOGGING,
        text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
    )

    await send_media_message(message, media, caption, buttons)

# 🔹 Group Start Command Handler
@app.on_message(filters.command("start") & filters.group)
async def start_group_command(client, message):
    caption, buttons = await generate_group_start_message(client)
    media = random.choice(START_MEDIA)
    await send_media_message(message, media, caption, buttons)

# 🔹 Function to Find Help Modules
def find_help_modules():
    buttons = []
    for module_name, module_data in HELP_DATA.items():
        button_name = module_data.get("HELP_NAME", "ᴜɴᴋɴᴏᴡɴ")
        buttons.append(InlineKeyboardButton(
            f"<tg-emoji custom_emoji_id=\"5213273001205874214\">📋</tg-emoji> {button_name}",
            callback_data=f"help_{module_name}"
        ))
    return [buttons[i : i + 2] for i in range(0, len(buttons), 2)]  # Changed to 2 columns for better balance

# 🔹 Help Button Click Handler (Shinobu Custom Design)
@app.on_callback_query(filters.regex("^open_help$"))
async def show_help_menu(client, query: CallbackQuery):
    time.sleep(1)
    buttons = find_help_modules()
    buttons.append([InlineKeyboardButton(
        "<tg-emoji custom_emoji_id=\"5213273001205874214\">⬅️</tg-emoji> ʀᴇᴛᴜʀɴ ᴛᴏ ᴍᴀɴsɪᴏɴ",
        callback_data="back_to_home"
    )])

    text = (
        "<tg-emoji custom_emoji_id=\"5213273001205874214\">⚙️</tg-emoji> <b>🦋 ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ ʜᴇʟᴘ ᴍᴇɴᴜ</b>\n\n"
        "<blockquote>sᴇʟᴇᴄᴛ ᴀ ᴛᴀʀɢᴇᴛ ᴅɪʀᴇᴄᴛᴏʀʏ ʙᴇʟᴏᴡ ᴛᴏ ʀᴇᴀᴅ ᴏᴜʀ ᴇxᴇᴄᴜᴛɪᴏɴ ᴍᴀɴᴜᴀʟs ᴀɴᴅ ᴛʀᴇᴀᴛᴍᴇɴᴛ ɢᴜɪᴅᴇs.\n\n"
        "ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ɪɴsɪᴅᴇ ᴍᴜsᴛ ʙᴇ ᴅᴇᴘʟᴏʏᴇᴅ ᴜsɪɴɢ ᴛʜᴇ ᴘʀᴇғɪx sʏᴍʙᴏʟ: <code>/</code></blockquote>"
    )

    try:
        await query.message.edit_caption(
            caption=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        await query.message.edit_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )

# 🔹 Individual Module Help Handler
@app.on_callback_query(filters.regex(r"^help_(.+)"))
async def show_help(client, query: CallbackQuery):
    time.sleep(1)
    module_name = query.data.split("_", 1)[1]
    try:
        module_data = HELP_DATA.get(module_name, {})
        help_text = module_data.get("HELP", "ɪs ᴍᴏᴅᴜʟᴇ ᴋᴀ ᴋᴏɪ ʜᴇʟᴘ ɴᴀʜɪ ʜᴀɪ.")
        buttons = [[InlineKeyboardButton(
            "<tg-emoji custom_emoji_id=\"5213273001205874214\">⬅️</tg-emoji> ʙᴀᴄᴋ ᴛᴏ ʟᴀʙᴏʀᴀᴛᴏʀʏ",
            callback_data="open_help"
        )]]

        full_text = (
            f"<tg-emoji custom_emoji_id=\"5213273001205874214\">🧪</tg-emoji> <b>{module_name.upper()} ᴄʟɪɴɪᴄᴀʟ ʀᴇᴄᴏʀᴅs:</b>\n\n"
            f"<blockquote>{help_text}</blockquote>"
        )

        try:
            await query.message.edit_caption(
                caption=full_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
        except Exception:
            await query.message.edit_text(
                text=full_text,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
    except Exception as e:
        await query.answer("ᴀɴᴛɪᴅᴏᴛᴇ ʟᴏɢs ᴄᴏᴜʟᴅ ɴᴏᴛ ʙᴇ ʟᴏᴀᴅᴇᴅ ᴘʀᴏᴘᴇʀʟʏ!")

# 🔹 Back to Home
@app.on_callback_query(filters.regex("^back_to_home$"))
async def back_to_home(client, query: CallbackQuery):
    time.sleep(1)
    caption, buttons = await generate_start_message(client, query.message)
    try:
        await query.message.edit_caption(
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        await query.message.edit_text(
            text=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=enums.ParseMode.HTML
        )
