from TEAMZYRO import *
from pyrogram import Client, filters
from pyrogram.types import Message
import html
import time
from datetime import datetime, timedelta

# Lock system to prevent spam
lock = {}

async def get_balance(user_id):
    user_data = await user_collection.find_one({'id': user_id}, {'balance': 1, 'tokens': 1})
    if user_data:
        return user_data.get('balance', 0), user_data.get('tokens', 0)
    return 0, 0

# Daily gift system
@app.on_message(filters.command("daily"))
async def daily_gift(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is in lock (cooldown)
    if user_id in lock and time.time() - lock[user_id] < 5:  # 5 second cooldown
        await message.reply_text("⏰ ᴀʀᴀ ᴀʀᴀ~ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀɢᴀɪɴ.")
        return

    lock[user_id] = time.time()

    # Check if user already claimed daily gift
    user_data = await user_collection.find_one({'id': user_id}, {'last_daily': 1, 'balance': 1})

    today = datetime.now().date()

    if user_data and 'last_daily' in user_data:
        last_daily = user_data['last_daily']
        if isinstance(last_daily, datetime):
            last_daily = last_daily.date()
        elif isinstance(last_daily, str):
            last_daily = datetime.fromisoformat(last_daily).date()

        if last_daily == today:
            await message.reply_text("🌸 ᴀʀᴀ ᴀʀᴀ~ ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ ᴅᴀɪʟʏ ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs ᴛᴏᴅᴀʏ! ᴄᴏᴍᴇ ʙᴀᴄᴋ ᴛᴏᴍᴏʀʀᴏᴡ.")
            return

    # Give daily gift of 100 wisteria petals
    daily_amount = 100
    await user_collection.update_one(
        {'id': user_id}, 
        {
            '$inc': {'balance': daily_amount},
            '$set': {'last_daily': datetime.now()}
        },
        upsert=True
    )

    new_balance, _ = await get_balance(user_id)
    user_name = html.escape(message.from_user.first_name)

    await message.reply_text(
        f"🦋 <b>ᴅᴀɪʟʏ ᴡɪsᴛᴇʀɪᴀ ʀᴇᴡᴀʀᴅ</b> 🌸\n\n"
        f"<blockquote>ғᴜғᴜғᴜ~ {user_name}, ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ ʏᴏᴜʀ ᴅᴀɪʟʏ ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs!\n\n"
        f"🌸 <b>ʀᴇᴡᴀʀᴅ:</b> +{daily_amount} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs\n"
        f"💳 <b>ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ:</b> {new_balance} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs</blockquote>"
    )

# Weekly gift system
@app.on_message(filters.command("weekly"))
async def weekly_gift(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is in lock (cooldown)
    if user_id in lock and time.time() - lock[user_id] < 5:  # 5 second cooldown
        await message.reply_text("⏰ ᴀʀᴀ ᴀʀᴀ~ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀɢᴀɪɴ.")
        return

    lock[user_id] = time.time()

    # Check if user already claimed weekly gift
    user_data = await user_collection.find_one({'id': user_id}, {'last_weekly': 1, 'balance': 1})

    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())  # Monday of current week
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)

    if user_data and 'last_weekly' in user_data:
        last_weekly = user_data['last_weekly']
        if isinstance(last_weekly, str):
            last_weekly = datetime.fromisoformat(last_weekly)

        if last_weekly >= week_start:
            next_week = week_start + timedelta(days=7)
            days_left = (next_week - now).days
            await message.reply_text(f"🌸 ᴀʀᴀ ᴀʀᴀ~ ʏᴏᴜ ʜᴀᴠᴇ ᴀʟʀᴇᴀᴅʏ ᴄʟᴀɪᴍᴇᴅ ʏᴏᴜʀ ᴡᴇᴇᴋʟʏ ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs! ɴᴇxᴛ ɢɪғᴛ ᴀᴠᴀɪʟᴀʙʟᴇ ɪɴ {days_left} ᴅᴀʏs.")
            return

    # Give weekly gift of 2000 wisteria petals
    weekly_amount = 2000
    await user_collection.update_one(
        {'id': user_id}, 
        {
            '$inc': {'balance': weekly_amount},
            '$set': {'last_weekly': datetime.now()}
        },
        upsert=True
    )

    new_balance, _ = await get_balance(user_id)
    user_name = html.escape(message.from_user.first_name)

    await message.reply_text(
        f"🦋 <b>ᴡᴇᴇᴋʟʏ ᴡɪsᴛᴇʀɪᴀ ʀᴇᴡᴀʀᴅ</b> 🎉\n\n"
        f"<blockquote>ғᴜғᴜғᴜ~ {user_name}, ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ ʏᴏᴜʀ ᴡᴇᴇᴋʟʏ ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs!\n\n"
        f"🌸 <b>ʀᴇᴡᴀʀᴅ:</b> +{weekly_amount} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs\n"
        f"💳 <b>ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ:</b> {new_balance} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs</blockquote>"
    )

@app.on_message(filters.command("balance"))
async def balance(client: Client, message: Message):
    user_id = message.from_user.id

    if user_id in lock and time.time() - lock[user_id] < 2:  # 2 second cooldown
        return

    lock[user_id] = time.time()

    user_balance, user_tokens = await get_balance(user_id)
    user_name = html.escape(message.from_user.first_name)
    
    response = (
        f"🦋 <b>{user_name}'s ᴍᴀɴsɪᴏɴ ᴠᴀᴜʟᴛ</b> 🌸\n\n"
        f"<blockquote>━━━━━━━▧▣▧━━━━━━━\n"
        f"🌸 <b>ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs:</b> {user_balance}\n"
        f"🎫 <b>ᴛᴏᴋᴇɴs:</b> {user_tokens}\n"
        f"━━━━━━━▧▣▧━━━━━━━</blockquote>"
    )
    await message.reply_text(response, reply_to_message_id=False)

@app.on_message(filters.command("pay"))
async def pay(client: Client, message: Message):
    sender_id = message.from_user.id

    if sender_id in lock and time.time() - lock[sender_id] < 3:  # 3 second cooldown
        await message.reply_text("⏰ ᴀʀᴀ ᴀʀᴀ~ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ʙᴇғᴏʀᴇ sᴇɴᴅɪɴɢ ᴀɴᴏᴛʜᴇʀ ᴘᴀʏᴍᴇɴᴛ.")
        return

    lock[sender_id] = time.time()

    args = message.command

    if len(args) < 2:
        await message.reply_text("🦋 <b>ᴜsᴀɢᴇ:</b> /pay <amount> [@username/user_id] ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.")
        return

    try:
        amount = int(args[1])
        if amount <= 0:
            raise ValueError
    except ValueError:
        await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ. ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ᴘᴏsɪᴛɪᴠᴇ ɴᴜᴍʙᴇʀ.")
        return

    recipient_id = None
    recipient_name = None

    if message.reply_to_message:
        recipient_id = message.reply_to_message.from_user.id
        recipient_name = message.reply_to_message.from_user.first_name
    elif len(args) > 2:
        try:
            recipient_id = int(args[2])
        except ValueError:
            recipient_username = args[2].lstrip('@')  # Remove @ from username
            user_data = await user_collection.find_one({'username': recipient_username}, {'id': 1, 'first_name': 1})
            if user_data:
                recipient_id = user_data['id']
                recipient_name = user_data.get('first_name', recipient_username)
            else:
                await message.reply_text("❌ ʀᴇᴄɪᴘɪᴇɴᴛ ɴᴏᴛ ғᴏᴜɴᴅ. ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ᴛʜᴇ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ.")
                return

    if not recipient_id:
        await message.reply_text("❌ ʀᴇᴄɪᴘɪᴇɴᴛ ɴᴏᴛ ғᴏᴜɴᴅ. ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ᴜsᴇʀ ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ.")
        return

    sender_balance, _ = await get_balance(sender_id)
    if sender_balance < amount:
        await message.reply_text("❌ ɪɴsᴜғғɪᴄɪᴇɴᴛ ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs.")
        return

    await user_collection.update_one({'id': sender_id}, {'$inc': {'balance': -amount}})
    await user_collection.update_one({'id': recipient_id}, {'$inc': {'balance': amount}})

    updated_sender_balance, _ = await get_balance(sender_id)
    updated_recipient_balance, _ = await get_balance(recipient_id)

    # Use first name or ID for recipient in the response
    recipient_display = html.escape(recipient_name or str(recipient_id))
    sender_display = html.escape(message.from_user.first_name or str(sender_id))

    await message.reply_text(
        f"🦋 <b>ᴘᴀʏᴍᴇɴᴛ sᴜᴄᴄᴇssғᴜʟ</b> 🌸\n\n"
        f"<blockquote>✅ ʏᴏᴜ ᴘᴀɪᴅ {amount} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs ᴛᴏ {recipient_display}\n\n"
        f"💳 <b>ʏᴏᴜʀ ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ:</b> {updated_sender_balance} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs</blockquote>"
    )

    await client.send_message(
        chat_id=recipient_id,
        text=f"🦋 <b>ᴘᴀʏᴍᴇɴᴛ ʀᴇᴄᴇɪᴠᴇᴅ</b> 🎉\n\n"
        f"<blockquote>🌸 ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ {amount} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs ғʀᴏᴍ {sender_display}!\n\n"
        f"💳 <b>ʏᴏᴜʀ ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ:</b> {updated_recipient_balance} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs</blockquote>"
    )

@app.on_message(filters.command("kill"))
@require_power("VIP")
async def kill_handler(client, message):
    # Get the user_id from the reply message
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        await message.reply_text("🦋 ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴛᴏ ᴜsᴇ ᴛʜᴇ /kill ᴄᴏᴍᴍᴀɴᴅ.")
        return

    command_args = message.text.split()

    if len(command_args) < 2:
        await message.reply_text(
            "🧪 <b>ᴋɪʟʟ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ:</b>\n\n"
            "<blockquote>• `c` ➜ ᴅᴇʟᴇᴛᴇ ᴄʜᴀʀᴀᴄᴛᴇʀ\n"
            "• `f` ➜ ᴅᴇʟᴇᴛᴇ ғᴜʟʟ ᴅᴀᴛᴀ\n"
            "• `b` ➜ ᴅᴇʟᴇᴛᴇ ʙᴀʟᴀɴᴄᴇ</blockquote>"
        )
        return

    option = command_args[1]

    try:
        if option == 'f':
            # Delete full user data
            await user_collection.delete_one({"id": user_id})
            await message.reply_text("🦋 <b>ᴅᴀᴛᴀ ᴇʀᴀsᴇᴅ</b>\n\n<blockquote>ᴛʜᴇ ғᴜʟʟ ᴅᴀᴛᴀ ᴏғ ᴛʜᴇ ᴜsᴇʀ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴍᴀɴsɪᴏɴ ʀᴇᴄᴏʀᴅs.</blockquote>")

        elif option == 'c':
            # Delete specific character from the user's collection
            if len(command_args) < 3:
                await message.reply_text("🦋 ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀ ᴄʜᴀʀᴀᴄᴛᴇʀ ɪᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ.")
                return

            char_id = command_args[2]
            user = await user_collection.find_one({"id": user_id})

            if user and 'characters' in user:
                characters = user['characters']
                updated_characters = [c for c in characters if c.get('id') != char_id]

                if len(updated_characters) == len(characters):
                    await message.reply_text(f"❌ ɴᴏ ᴄʜᴀʀᴀᴄᴛᴇʀ ᴡɪᴛʜ ɪᴅ {char_id} ғᴏᴜɴᴅ ɪɴ ᴛʜᴇ ᴜsᴇʀ's ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")
                    return

                # Update user collection
                await user_collection.update_one({"id": user_id}, {"$set": {"characters": updated_characters}})
                await message.reply_text(f"🦋 <b>ᴄʜᴀʀᴀᴄᴛᴇʀ ʀᴇᴍᴏᴠᴇᴅ</b>\n\n<blockquote>ᴄʜᴀʀᴀᴄᴛᴇʀ ᴡɪᴛʜ ɪᴅ {char_id} ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴄᴏʟʟᴇᴄᴛɪᴏɴ.</blockquote>")
            else:
                await message.reply_text(f"❌ ɴᴏ ᴄʜᴀʀᴀᴄᴛᴇʀs ғᴏᴜɴᴅ ɪɴ ᴛʜᴇ ᴜsᴇʀ's ᴄᴏʟʟᴇᴄᴛɪᴏɴ.")

        elif option == 'b':
            # Check if amount is provided
            if len(command_args) < 3:
                await message.reply_text("🦋 ᴘʟᴇᴀsᴇ sᴘᴇᴄɪғʏ ᴀɴ ᴀᴍᴏᴜɴᴛ ᴛᴏ ᴅᴇᴅᴜᴄᴛ ғʀᴏᴍ ʙᴀʟᴀɴᴄᴇ.")
                return

            try:
                amount = int(command_args[2])
            except ValueError:
                await message.reply_text("❌ ɪɴᴠᴀʟɪᴅ ᴀᴍᴏᴜɴᴛ. ᴘʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ɴᴜᴍʙᴇʀ.")
                return

            # Fetch user balance
            user_data = await user_collection.find_one({"id": user_id}, {"balance": 1})
            if user_data and "balance" in user_data:
                current_balance = user_data["balance"]
                new_balance = max(0, current_balance - amount)  # Ensure balance doesn't go negative

                await user_collection.update_one({"id": user_id}, {"$set": {"balance": new_balance}})
                await message.reply_text(
                    f"🦋 <b>ʙᴀʟᴀɴᴄᴇ ᴅᴇᴅᴜᴄᴛᴇᴅ</b>\n\n"
                    f"<blockquote>{amount} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs ʜᴀᴠᴇ ʙᴇᴇɴ ᴅᴇᴅᴜᴄᴛᴇᴅ.\n\n"
                    f"💳 <b>ɴᴇᴡ ʙᴀʟᴀɴᴄᴇ:</b> {new_balance} ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs</blockquote>"
                )
            else:
                await message.reply_text("❌ ᴛʜᴇ ᴜsᴇʀ ʜᴀs ɴᴏ ᴡɪsᴛᴇʀɪᴀ ᴘᴇᴛᴀʟs ᴛᴏ ᴅᴇᴅᴜᴄᴛ ғʀᴏᴍ.")

        else:
            await message.reply_text(
                "❌ <b>ɪɴᴠᴀʟɪᴅ ᴏᴘᴛɪᴏɴ</b>\n\n"
                "<blockquote>ᴜsᴇ `c` ғᴏʀ ᴄʜᴀʀᴀᴄᴛᴇʀ, `f` ғᴏʀ ғᴜʟʟ ᴅᴀᴛᴀ, ᴏʀ `b {amount}` ᴛᴏ ᴅᴇᴅᴜᴄᴛ ʙᴀʟᴀɴᴄᴇ.</blockquote>"
            )

    except Exception as e:
        print(f"Error in /kill command: {e}")
        await message.reply_text("❌ ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")