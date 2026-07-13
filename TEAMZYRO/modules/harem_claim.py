# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

import asyncio
from pyrogram import Client, filters, types as t
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from TEAMZYRO import ZYRO as bot
from TEAMZYRO import user_collection, collection, user_nguess_progress, user_guess_progress, FORCE_JOIN as chat, FORCE_JOIN_LINK

claim_lock = {}

# Helper function to format time remaining until next claim
async def format_time_delta(delta):
    seconds = delta.total_seconds()
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s" if hours or minutes or seconds else "0s"

# Fetch unique characters not yet claimed by the user
async def get_unique_characters(user_id, target_rarities=['⚪️ Common', '🟡 Legendary', '🟢 Medium']):
    try:
        # Get the already claimed character ids
        user_data = await user_collection.find_one({'id': user_id}, {'characters.id': 1})
        claimed_ids = [char['id'] for char in user_data.get('characters', [])] if user_data else []

        pipeline = [
            {'$match': {'rarity': {'$in': target_rarities}, 'id': {'$nin': claimed_ids}}},
            {'$sample': {'size': 1}}  # Randomly sample one character
        ]
        cursor = collection.aggregate(pipeline)
        characters = await cursor.to_list(length=None)
        return characters if characters else []
    except Exception as e:
        print(f"Error retrieving unique characters: {e}")
        return []

# Command handler for the daily claim
@bot.on_message(filters.command(["hclaim", "claim"]))
async def mclaim(_, message: t.Message):
    user_id = message.from_user.id
    mention = message.from_user.mention
    today = datetime.utcnow().date()

    # Prevent multiple claims at the same time
    if user_id in claim_lock:
        await message.reply_text("🌸 *One moment please~* Your previous request is still being processed.")
        return

    claim_lock[user_id] = True
    try:
        # Ensure the user is in the correct chat
        if str(message.chat.id) != str(chat):
            join_button = InlineKeyboardMarkup([[InlineKeyboardButton("🌸 Join the Wisteria Garden", url=FORCE_JOIN_LINK)]])
            return await message.reply_text(
                "🌸 *Fufufu~* Before you can claim your daily spirit, you must first enter the wisteria garden! Please join our sanctuary.",
                reply_markup=join_button
            )

        # Fetch user data or create a new user if not found
        user_data = await user_collection.find_one({'id': user_id})
        if not user_data:
            user_data = {
                'id': user_id,
                'username': message.from_user.username,
                'characters': [],
                'last_daily_reward': None
            }
            await user_collection.insert_one(user_data)

        # Check if the user has already claimed today
        last_claimed_date = user_data.get('last_daily_reward')
        if last_claimed_date and last_claimed_date.date() == datetime.utcnow().date():
            remaining_time = timedelta(days=1) - (datetime.utcnow() - last_claimed_date)
            formatted_time = await format_time_delta(remaining_time)
            return await message.reply_text(f"🌸 *Ara ara~* You've already welcomed a spirit today! Your next guest arrives in `{formatted_time}`.")

        # Fetch a unique character for the user
        unique_characters = await get_unique_characters(user_id)
        if not unique_characters:
            return await message.reply_text("🌸 *Oh my~* The garden seems empty today. Please try again tomorrow for a new spirit to arrive.")

        # Update user data with the new character and claim time
        await user_collection.update_one(
            {'id': user_id},
            {'$push': {'characters': {'$each': unique_characters}}, '$set': {'last_daily_reward': datetime.utcnow()}}
        )

        # Send the character's image and info
        for character in unique_characters:
            await message.reply_photo(
                photo=character['img_url'],
                caption=(
                    f"🌸 *A new butterfly has arrived in your garden!* 🦋\n\n"
                    f"✨ **Name:** {character['name']}\n"
                    f"🌈 **Rarity:** {character['rarity']}\n"
                    f"⛩️ **Anime:** {character['anime']}\n\n"
                    f"*Fufufu~* Treat them well! I'll send another spirit your way tomorrow, so do visit again~ 🌸"
                )
            )

    except Exception as e:
        print(f"Error in mclaim command: {e}")
        await message.reply_text("🌸 *Ara ara~* An unexpected breeze disturbed the garden. Please try again later.")

    finally:
        # Remove the user from claim lock to allow future claims
        claim_lock.pop(user_id, None)
