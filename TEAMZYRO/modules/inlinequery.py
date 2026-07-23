# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultPhoto, InlineQueryResultVideo, InlineQueryResultDocument, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from TEAMZYRO import app, collection, rarity_map
from TEAMZYRO.unit.zyro_rarity import rarity_map as zyro_rarity_map
import re

@app.on_inline_query()
async def inline_query_handler(client, inline_query):
    query = inline_query.query.strip()
    
    if not query:
        # Show popular characters or help
        results = []
        cursor = collection.find().sort("id", 1).limit(20)
        async for char in cursor:
            rarity_text = char.get('rarity', 'Unknown')
            caption = (
                f"🎴 <b>{char.get('name', 'Unknown')}</b>\n"
                f"📺 {char.get('anime', 'Unknown')}\n"
                f"⭐ {rarity_text}\n"
                f"🆔 {char.get('id', 'N/A')}"
            )
            
            if 'img_url' in char:
                results.append(
                    InlineQueryResultPhoto(
                        photo_url=char['img_url'],
                        thumb_url=char['img_url'],
                        title=char.get('name', 'Unknown'),
                        description=f"{char.get('anime', 'Unknown')} - {rarity_text}",
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("➕ Add Character", callback_data=f"add_{char.get('id', '0')}")]
                        ])
                    )
                )
            elif 'vid_url' in char:
                results.append(
                    InlineQueryResultVideo(
                        video_url=char['vid_url'],
                        thumb_url=char.get('thum_url', ''),
                        title=char.get('name', 'Unknown'),
                        description=f"{char.get('anime', 'Unknown')} - {rarity_text}",
                        caption=caption,
                        parse_mode=ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton("➕ Add Character", callback_data=f"add_{char.get('id', '0')}")]
                        ])
                    )
                )
        
        await inline_query.answer(results, cache_time=5)
        return
    
    # Search by name, anime, or rarity
    search_query = query.lower()
    
    # Check if searching by rarity
    rarity_match = False
    rarity_number = None
    for num, name in rarity_map.items():
        if search_query in name.lower():
            rarity_match = True
            rarity_number = num
            break
    
    if rarity_match:
        # Search by rarity number
        cursor = collection.find({'rarity_number': rarity_number}).limit(50)
    else:
        # Search by name or anime
        cursor = collection.find({
            '$or': [
                {'name': {'$regex': search_query, '$options': 'i'}},
                {'anime': {'$regex': search_query, '$options': 'i'}}
            ]
        }).limit(50)
    
    results = []
    async for char in cursor:
        rarity_text = char.get('rarity', 'Unknown')
        caption = (
            f"🎴 <b>{char.get('name', 'Unknown')}</b>\n"
            f"📺 {char.get('anime', 'Unknown')}\n"
            f"⭐ {rarity_text}\n"
            f"🆔 {char.get('id', 'N/A')}"
        )
        
        if 'img_url' in char:
            results.append(
                InlineQueryResultPhoto(
                    photo_url=char['img_url'],
                    thumb_url=char['img_url'],
                    title=char.get('name', 'Unknown'),
                    description=f"{char.get('anime', 'Unknown')} - {rarity_text}",
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("➕ Add Character", callback_data=f"add_{char.get('id', '0')}")]
                    ])
                )
            )
        elif 'vid_url' in char:
            results.append(
                InlineQueryResultVideo(
                    video_url=char['vid_url'],
                    thumb_url=char.get('thum_url', ''),
                    title=char.get('name', 'Unknown'),
                    description=f"{char.get('anime', 'Unknown')} - {rarity_text}",
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("➕ Add Character", callback_data=f"add_{char.get('id', '0')}")]
                    ])
                )
            )
    
    await inline_query.answer(results, cache_time=5)

@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    
    if data.startswith("add_"):
        char_id = data.split("_")[1]
        user_id = callback_query.from_user.id
        
        # Check if user already has this character
        user_data = await user_collection.find_one({'_id': user_id})
        if user_data:
            for char in user_data.get('characters', []):
                if char.get('id') == char_id:
                    await callback_query.answer("You already have this character!", show_alert=True)
                    return
        
        # Get character from collection
        char_data = await collection.find_one({'id': char_id})
        if char_data:
            # Add to user's collection
            char_copy = char_data.copy()
            char_copy.pop('_id', None)
            
            await user_collection.update_one(
                {'_id': user_id},
                {'$push': {'characters': char_copy}},
                upsert=True
            )
            await callback_query.answer("Character added successfully!", show_alert=True)
        else:
            await callback_query.answer("Character not found!", show_alert=True)
