# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

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
        f"🦋 <b>Ara ara~ Welcome to the Butterfly Mansion!</b> 🌸\n\n"
        f"<i>I am {bot_name}. It seems you've wandered straight into my laboratory. Don't worry, the fresh wisteria fragrance will keep you safe from any nasty demons here.</i>\n\n"
        f"<blockquote>━━━━━━━▧▣▧━━━━━━━\n"
        f"⦾ <b>MISSION:</b> I track down roaming Slayers and trap wandering Demons in your chats.\n"
        f"⦾ <b>TRAINING:</b> Add me to your group and use /help to read my custom training manuals.\n"
        f"━━━━━━━▧▣▧━━━━━━━\n"
        f"⚡ <b>PULSE:</b> {ping} ms\n"
        f"⏳ <b>REST ZONE:</b> {uptime}</blockquote>"
    )

    buttons = [
        [InlineKeyboardButton("🦋 Deploy To Your Squad ", url=f"https://t.me/{bot_user.username}?startgroup=true")],
        [InlineKeyboardButton("💜 Support Mansion", url="https://t.me/+fPjchISAGnc3OGJl")], 
        [InlineKeyboardButton("📢 Laboratory", url="https://t.me/+wjJbHQ9DQzM1OTE1")],
        [InlineKeyboardButton("🧪 Training Manual", callback_data="open_help")],
        [InlineKeyboardButton("Owner", url=f"https://t.me/xeno_kakarot")],
    ]
    
    return caption, buttons

# 🔹 Function to Generate Group Start Message & Buttons (Shinobu Custom Design)
async def generate_group_start_message(client):
    bot_user = await client.get_me()
    caption = (
        f"🦋 <i>Flap, flap... I am</i> <b>{bot_user.first_name}</b> 🌸\n\n"
        f"<blockquote>I am currently monitoring this chat area to detect and expose hidden demons through message flows.\n\n"
        f"Use /help to access my specialized medical and combat manuals!</i></blockquote>"
    )
    buttons = [
        [
            InlineKeyboardButton("🦋 Summon Me", url=f"https://t.me/{bot_user.username}?startgroup=true"),
            InlineKeyboardButton("💜 Support", url=SUPPORT_CHAT)
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
        text=f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>\n<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}",
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
        button_name = module_data.get("HELP_NAME", "Unknown")
        buttons.append(InlineKeyboardButton(button_name, callback_data=f"help_{module_name}"))
    return [buttons[i : i + 3] for i in range(0, len(buttons), 3)]

# 🔹 Help Button Click Handler (Shinobu Custom Design)
@app.on_callback_query(filters.regex("^open_help$"))
async def show_help_menu(client, query: CallbackQuery):
    time.sleep(1)
    buttons = find_help_modules()
    buttons.append([InlineKeyboardButton("⬅️ Return to Mansion", callback_data="back_to_home")])

    text = (
        "⚙️ <b>🦋 BUTTERFLY MANSION HELP MENU</b>\n\n"
        "<blockquote>Select a target directory below to read our execution manuals and treatment guides.\n\n"
        "All commands inside must be deployed using the prefix symbol: /</blockquote>"
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
        help_text = module_data.get("HELP", "Is module ka koi help nahi hai.")
        buttons = [[InlineKeyboardButton("⬅️ Back to Laboratory", callback_data="open_help")]]
        
        full_text = f"🧪 <b>{module_name.upper()} Clinical Records:</b>\n\n{help_text}"
        
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
        await query.answer("Antidote logs could not be loaded properly!")

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
