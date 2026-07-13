# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

from TEAMZYRO import *
from TEAMZYRO import application
from html import escape
import asyncio
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram import enums
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

@app.on_message(filters.command(["guess", "protecc", "collect", "grab", "hunt"]))
async def guess(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    today = datetime.utcnow().date()

    if await check_cooldown(user_id):
        remaining_time = await get_remaining_cooldown(user_id)
        await message.reply_text(
            f"🌸 *My, my~ Such enthusiasm!* But even a butterfly needs to rest its wings. Please wait {remaining_time} seconds before your next attempt.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return

    if 'name' not in last_characters.get(chat_id, {}):
        await message.reply_text("🌸 *Ara ara~* The garden is quiet right now. No spirits have manifested in this realm yet.", parse_mode=enums.ParseMode.MARKDOWN)
        return
    
    if chat_id not in last_characters:
        await message.reply_text("🌸 *Fufufu~* It seems the wisteria has yet to bloom here. No souls to guide today.", parse_mode=enums.ParseMode.MARKDOWN)
        return

    if chat_id in first_correct_guesses:
        await message.reply_text("🌸 *Too late~* This butterfly has already been gently guided to its new home!", parse_mode=enums.ParseMode.MARKDOWN)
        return

    if last_characters[chat_id].get('ranaway', False):
        await message.reply_text("🌸 *Oh dear~* The spirit detected our wisteria perfume and vanished into the mist!", parse_mode=enums.ParseMode.MARKDOWN)
        return 

    guess = ' '.join(message.command[1:]).lower() if len(message.command) > 1 else ''
    
    if "()" in guess or "&" in guess.lower():
        await message.reply_text("🌸 *Fufufu~* Such strange characters! Let's keep our words pure and elegant, shall we?", parse_mode=enums.ParseMode.MARKDOWN)
        return

    name_parts = last_characters[chat_id]['name'].lower().split()
    
    if sorted(name_parts) == sorted(guess.split()) or any(part == guess for part in name_parts):
        first_correct_guesses[chat_id] = user_id
        for task in asyncio.all_tasks():
            if task.get_name() == f"expire_session_{chat_id}":
                task.cancel()
                break

        timestamp = last_characters[chat_id].get('timestamp')
        if timestamp:
            time_taken = time.time() - timestamp
            time_taken_str = f"{int(time_taken)} seconds"
        else:
            time_taken_str = "A fleeting moment"

        if user_id not in user_guess_progress or user_guess_progress[user_id]["date"] != today:
            user_guess_progress[user_id] = {"date": today, "count": 0}

        user_guess_progress[user_id]["count"] += 1
        
        # Fetch user from MongoDB
        user = await user_collection.find_one({'id': user_id})
        if user:
            update_fields = {}
            if message.from_user.username != user.get('username'):
                update_fields['username'] = message.from_user.username
            if message.from_user.first_name != user.get('first_name'):
                update_fields['first_name'] = message.from_user.first_name
            if update_fields:
                await user_collection.update_one({'id': user_id}, {'$set': update_fields})
            
            await user_collection.update_one({'id': user_id}, {'$push': {'characters': last_characters[chat_id]}})
      
        else:
            await user_collection.insert_one({
                'id': user_id,
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'characters': [last_characters[chat_id]],
            })

        # Update group count in top_global_groups_collection
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            group_name = message.chat.title or f"Group_{chat_id}"
            await top_global_groups_collection.update_one(
                {'chat_id': chat_id},
                {
                    '$set': {'group_name': group_name},
                    '$inc': {'count': 1}
                },
                upsert=True
            )

        await react_to_message(chat_id, message.id)

        # Fetch user to update balance
        user = await user_collection.find_one({'id': user_id})
        if user:
            current_balance = user.get('balance', 0)
            new_balance = current_balance + 40
            await user_collection.update_one({'id': user_id}, {'$set': {'balance': new_balance}})
        else:
            new_balance = 40
            await user_collection.insert_one({
                'id': user_id,
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'characters': [last_characters[chat_id]],
                'balance': 40
            })

        keyboard = [[InlineKeyboardButton("🌸 View Your Butterfly Garden", switch_inline_query_current_chat=f"collection.{user_id}")]]
        
        await message.reply_text(
            f'🌸 *My, my! What an exquisite capture~* ✨\n\n'
            f'Congratulations <b><a href="tg://user?id={user_id}">{escape(message.from_user.first_name)}</a></b>, you\'ve successfully guided a spirit home! 🦋\n\n'
            f'<blockquote>📛 <b>Name:</b> {last_characters[chat_id]["name"]}\n'
            f'🌈 <b>Anime:</b> {last_characters[chat_id]["anime"]}\n'
            f'✨ <b>Rarity:</b> {last_characters[chat_id]["rarity"]}\n\n'
            f'⏱️ <b>Time to Capture:</b> {time_taken_str}\n'
            f'🌸 <b>Wisteria Petals Earned:</b> +40\n'
            f'💳 <b>Total Petals:</b> {new_balance}\n\n'
            f'This soul has been gently placed in your garden. Use /harem to admire your collection.</blockquote>',
            parse_mode=enums.ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        message_id = last_characters[chat_id].get('message_id')
        incorrect_text = (
            "🌸 *Ara ara~ Not quite!*\n\n"
            "*Fufufu~* Your aim is a bit off today. Take a closer look at the spirit's essence before your next attempt. I believe in you~"
        )
        if message_id:
            keyboard = [
                [InlineKeyboardButton("🔍 View the Spirit Again", url=f"https://t.me/c/{str(chat_id)[4:]}/{message_id}")],
            ]
            await message.reply_text(
                incorrect_text,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                incorrect_text,
                parse_mode=enums.ParseMode.MARKDOWN
            )
