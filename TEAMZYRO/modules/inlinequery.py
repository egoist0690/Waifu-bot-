# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

import re
import time
from html import escape
from cachetools import TTLCache
from telegram import Update, InlineQueryResultPhoto, InlineQueryResultVideo
from telegram.ext import InlineQueryHandler, CallbackContext
from TEAMZYRO import application  # Assuming 'application' is the main bot object
from TEAMZYRO.unit.zyro_inline import *

# Rarity Mapping Dict
RARITY_MAP = {
    1: "⚪️ Common",
    2: "🟣 Rare",
    3: "🟢 Medium",
    4: "🟡 Legendary",
    5: "💮 Special Edition",
    6: "🔮 Limited Edition",
    7: "💸 Premium Edition",
    8: "🌤 Summer",
    9: "🎐 Enchanted",
    10: "❄️ Frozen",
    11: "💝 Romantic",
    12: "🎃 Haunted",
    13: "🎄 Chrimsum",
    14: "🧧 Festive",
    15: "🍑 Naughty",
    16: "🎗️ AMV Edition",
    17: "🌧 Cloudy",
    18: "🦠 Mythgard",
}

def format_rarity(rarity_val) -> str:
    """Helper function to parse rarity integers or preserve string formatting."""
    if isinstance(rarity_val, int):
        return RARITY_MAP.get(rarity_val, f"🔮 {rarity_val}")
    elif isinstance(rarity_val, str) and rarity_val.isdigit():
        return RARITY_MAP.get(int(rarity_val), f"🔮 {rarity_val}")
    return str(rarity_val)


all_characters_cache = TTLCache(maxsize=10000, ttl=36000)  # Cache for all characters
user_collection_cache = TTLCache(maxsize=10000, ttl=60)  # Cache for user collections


async def inlinequery(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    offset = int(update.inline_query.offset) if update.inline_query.offset else 0

    # Check if query is for a user's collection
    if query.startswith('collection.'):
        user_id, *search_terms = query.split(' ')[0].split('.')[1], ' '.join(query.split(' ')[1:])
        if user_id.isdigit():
            user = user_collection_cache.get(user_id) or await get_user_collection(user_id)
            if user:
                user_collection_cache[user_id] = user  # Cache the result
                all_characters = list({char['id']: char for char in user['characters'] if 'id' in char}.values())  # Deduplicate by ID
                
                if search_terms:
                    regex = re.compile(' '.join(search_terms), re.IGNORECASE)
                    all_characters = [char for char in all_characters if regex.search(char['name']) or regex.search(char['anime'])]
            else:
                all_characters = []
        else:
            all_characters = []
    else:
        # General character search
        if query:
            all_characters = await search_characters(query)
        else:
            all_characters = all_characters_cache.get('all_characters') or await get_all_characters()
            all_characters_cache['all_characters'] = all_characters  # Cache the result

    # Filter characters based on whether they have a video or image
    if '.AMV' in query:
        all_characters = [char for char in all_characters if 'vid_url' in char]
    else:
        all_characters = [char for char in all_characters if 'img_url' in char]

    # Pagination logic
    characters = all_characters[offset:offset + 50]
    next_offset = str(offset + len(characters)) if len(characters) == 50 else None

    # Construct results for inline query
    results = []
    for character in characters:
        rarity_text = format_rarity(character.get('rarity', ''))
        
        # Generate Shinobu-styled captions
        if 'user' in locals():
            user_character_count = sum(1 for char in user['characters'] if 'id' in char and char['id'] == character['id'])
            caption = (
                f"🦋 <b>ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ ʀᴇᴄᴏʀᴅs</b> 🌸\n"
                f"👤 <b>sʟᴀʏᴇʀ:</b> <a href='tg://user?id={user['id']}'>{escape(user.get('first_name', 'User'))}</a>\n\n"
                f"<blockquote>"
                f"🌸 <b>ɴᴀᴍᴇ:</b> {character['name']} (x{user_character_count})\n"
                f"🧬 <b>ᴀɴɪᴍᴇ:</b> {character['anime']}\n"
                f"🧪 <b>ʀᴀʀɪᴛʏ:</b> {rarity_text}\n"
                f"🆔 <b>ɪᴅ:</b> <code>{character['id']}</code>"
                f"</blockquote>\n\n"
                f"<i>~ Ara ara! A fine addition to the collection.</i>"
            )
        else:
            caption = (
                f"🧪 <b>ʙᴜᴛᴛᴇʀғʟʏ ᴍᴀɴsɪᴏɴ ᴀɴᴛɪᴅᴏᴛᴇ ʟᴏɢs</b> 🦋\n\n"
                f"<blockquote>"
                f"🌸 <b>ɴᴀᴍᴇ:</b> {character['name']}\n"
                f"🧬 <b>ᴀɴɪᴍᴇ:</b> {character['anime']}\n"
                f"🧪 <b>ʀᴀʀɪᴛʏ:</b> {rarity_text}\n"
                f"🆔 <b>ɪᴅ:</b> <code>{character['id']}</code>"
                f"</blockquote>\n\n"
                f"<i>~ Medical data successfully retrieved from the laboratory!</i>"
            )

        # If the character has a video URL, create a video result
        if 'vid_url' in character:
            thumbnail_url = character.get('thum_url', 'https://envs.sh/6Y3.jpg')  # Use a default thumbnail if missing
            results.append(
                InlineQueryResultVideo(
                    id=f"{character['id']}_{time.time()}",
                    video_url=character['vid_url'],
                    mime_type="video/mp4",
                    thumbnail_url=thumbnail_url,
                    title=character['name'],
                    description=f"From: {character['anime']} | Rarity: {rarity_text}",
                    caption=caption,
                    parse_mode='HTML'
                )
            )
        elif 'img_url' in character:
            # Add photo result to inline query results
            results.append(
                InlineQueryResultPhoto(
                    thumbnail_url=character['img_url'],
                    id=f"{character['id']}_{time.time()}",
                    photo_url=character['img_url'],
                    caption=caption,
                    parse_mode='HTML'
                )
            )

    # Send the results with pagination
    await update.inline_query.answer(results, next_offset=next_offset, cache_time=5)
    
# Add the handler to your bot's application
application.add_handler(InlineQueryHandler(inlinequery, block=False))
