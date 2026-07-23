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
        await message.reply_text(
            "🌸 <i>One moment please~</i> Your previous request is still being processed.",
            parse_mode=enums.ParseMode.HTML
        )
        return

    claim_lock[user_id] = True
    try:
        # Ensure the user is in the correct chat
        if str(message.chat.id) != str(chat):
            join_button = InlineKeyboardMarkup([[InlineKeyboardButton("🌸 Join the Wisteria Garden", url=FORCE_JOIN_LINK)]])
            return await message.reply_text(
                "🌸 <b>𝐖꯭𝐢꯭𝐬꯭𝐭꯭𝐞꯭𝐫꯭𝐢꯭𝐚 𝐆꯭𝐚꯭𝐭꯭𝐞</b>\n\n"
                "<blockquote>Before you can receive your daily blessing, you must first enter the wisteria garden!</blockquote>",
                reply_markup=join_button,
                parse_mode=enums.ParseMode.HTML
            )

        # Fetch user data or create a new user if not found
        user_data = await user_collection.find_one({'id': user_id})
        if not user_data:
            user_data = {
                'id': user_id,
                'username': message.from_user.username,
                'characters': [],
                'last_daily_reward': None,
                'balance': 0
            }
            await user_collection.insert_one(user_data)

        # Check if the user has already claimed today
        last_claimed_date = user_data.get('last_daily_reward')
        if last_claimed_date and last_claimed_date.date() == datetime.utcnow().date():
            remaining_time = timedelta(days=1) - (datetime.utcnow() - last_claimed_date)
            formatted_time = await format_time_delta(remaining_time)
            
            # Cooldown message with Shinobu theme
            return await message.reply_text(
                f"🌸 <b>𝐖꯭𝐢꯭𝐬꯭𝐭꯭𝐞꯭𝐫꯭𝐢꯭𝐚 𝐑꯭𝐞꯭𝐬꯭𝐭</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"🦋 The butterflies are still gathering nectar.\n\n"
                f"⏳ <b>Remaining Time</b> ↬ {formatted_time}\n\n"
                f"Please return once the wisteria blooms again.\n"
                f"━━━━━━━━━━━━━━━━━━\n\n"
                f"💜 <b>Shinobu Kocho</b>",
                parse_mode=enums.ParseMode.HTML
            )

        # Fetch a unique character for the user
        unique_characters = await get_unique_characters(user_id)
        if not unique_characters:
            return await message.reply_text(
                "🌸 <i>Oh my~</i> The garden seems empty today. Please try again tomorrow for a new spirit to arrive.",
                parse_mode=enums.ParseMode.HTML
            )

        # Update user data with the new character and claim time
        await user_collection.update_one(
            {'id': user_id},
            {'$push': {'characters': {'$each': unique_characters}}, '$set': {'last_daily_reward': datetime.utcnow()}}
        )

        # Send the character's image and info with Shinobu theme
        for character in unique_characters:
            # Get updated balance
            user_data = await user_collection.find_one({'id': user_id})
            balance = user_data.get('balance', 0)
            reward_amount = 5  # Daily reward amount
            
            await message.reply_photo(
                photo=character['img_url'],
                caption=(
                    f"🌸 <b>𝐖꯭𝐢꯭𝐬꯭𝐭꯭𝐞꯭𝐫꯭𝐢꯭𝐚 𝐁꯭𝐥꯭𝐞꯭𝐬꯭𝐬꯭𝐢꯭𝐧꯭𝐠</b>\n"
                    f"━━━━━━━━━━━━━━━━━━\n\n"
                    f"👤 <b>𝐇𝐚𝐬𝐡𝐢𝐫𝐚</b> ↬ {message.from_user.mention}\n"
                    f"🌸 <b>𝐏𝐞𝐭𝐚𝐥𝐬 𝐄𝐚𝐫𝐧𝐞𝐝</b> ↬ +{reward_amount}\n"
                    f"💰 <b>𝐓𝐨𝐭𝐚𝐥 𝐏𝐞𝐭𝐚𝐥𝐬</b> ↬ {balance + reward_amount}\n"
                    f"🕒 <b>𝐍𝐞𝐱𝐭 𝐁𝐥𝐞𝐬𝐬𝐢𝐧𝐠</b> ↬ 24h\n\n"
                    f"━━━━━━━━━━━━━━━━━━\n\n"
                    f"🦋\n"
                    f"<i>\"Even the gentlest butterfly\n"
                    f"returns when the wisteria blooms.\"</i>\n\n"
                    f"💜 <b>Shinobu Kocho</b>\n\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"✨ <b>New Butterfly Arrived!</b>\n"
                    f"📛 <b>Name:</b> {character['name']}\n"
                    f"🌈 <b>Rarity:</b> {character['rarity']}\n"
                    f"⛩️ <b>Anime:</b> {character['anime']}"
                ),
                parse_mode=enums.ParseMode.HTML
            )

    except Exception as e:
        print(f"Error in mclaim command: {e}")
        await message.reply_text(
            "🌸 <i>Ara ara~</i> An unexpected breeze disturbed the garden. Please try again later.",
            parse_mode=enums.ParseMode.HTML
        )

    finally:
        # Remove the user from claim lock to allow future claims
        claim_lock.pop(user_id, None)
