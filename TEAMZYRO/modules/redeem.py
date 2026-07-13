# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

import random
import string
import time
from datetime import datetime
from pymongo import ReturnDocument
from pyrogram import Client, filters
from pyrogram import enums
from TEAMZYRO import ZYRO as app
from TEAMZYRO import collection, user_collection, db, require_power, BOT_LOGGING

# Collections
redeem_collection = db["redeem_codes"]  # Collection for redeem codes

# ==========================================
# COMMAND: /gen (VIP/Owner Only)
# ==========================================

@app.on_message(filters.command("gen"))
@require_power("VIP")
async def generate_redeem_code(client, message):
    """
    Generate redeem codes for coins or characters.
    
    Usage:
        /gen coins <amount> <limit>          - Generate code for coins
        /gen <character_id> <copies> <limit> - Generate code for character copies
        
    Examples:
        /gen coins 5000 10      - 10 people can redeem 5000 coins each
        /gen 12345 3 5          - 5 people can redeem 3 copies of character 12345
    """
    args = message.command
    user_id = message.from_user.id
    
    # Validate minimum arguments
    if len(args) < 3:
        await message.reply_text(
            "**Usage:**\n"
            "`/gen coins <amount> <limit>` - Generate coin redeem code\n"
            "`/gen <character_id> <copies> <limit>` - Generate character redeem code\n\n"
            "**Examples:**\n"
            "`/gen coins 5000 10` - 10 users can redeem 5000 coins each\n"
            "`/gen 12345 3 5` - 5 users can redeem 3 copies each",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    try:
        # Parse limit (always the last argument)
        limit = int(args[-1])
        if limit <= 0:
            raise ValueError("Limit must be positive")
        if limit > 1000:
            await message.reply_text("❌ Limit too high. Maximum: 1000 users")
            return
    except ValueError:
        await message.reply_text("❌ Invalid limit. Please enter a positive number.")
        return
    
    # Check if it's a coin generation
    if args[1].lower() == "coins":
        # Handle coin generation
        if len(args) != 4:
            await message.reply_text(
                "❌ **Invalid format!**\n"
                "Use: `/gen coins <amount> <limit>`",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return
        
        try:
            coin_amount = int(args[2])
            if coin_amount <= 0:
                raise ValueError("Amount must be positive")
            if coin_amount > 999999999:
                await message.reply_text("❌ Amount too large. Maximum: 999,999,999")
                return
        except ValueError:
            await message.reply_text("❌ Invalid coin amount. Please enter a positive number.")
            return
        
        # Generate coin redeem code
        reward_type = "coins"
        reward_data = coin_amount
        reward_description = f"{coin_amount:,} coins"
        
    else:
        # Handle character generation
        if len(args) != 4:
            await message.reply_text(
                "❌ **Invalid format!**\n"
                "Use: `/gen <character_id> <copies> <limit>`",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return
        
        character_id = args[1]
        
        try:
            copies = int(args[2])
            if copies <= 0:
                raise ValueError("Copies must be positive")
            if copies > 100:
                await message.reply_text("❌ Too many copies. Maximum: 100")
                return
        except ValueError:
            await message.reply_text("❌ Invalid copy count. Please enter a positive number.")
            return
        
        # Check if character exists in database
        character = await collection.find_one({'id': character_id})
        if not character:
            await message.reply_text(
                f"❌ Character with ID `{character_id}` not found in database.",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            return
        
        # Generate character redeem code
        reward_type = "character"
        reward_data = {
            "character_id": character_id,
            "copies": copies,
            "character_name": character.get("name", "Unknown"),
            "anime": character.get("anime", "Unknown"),
            "rarity": character.get("rarity", "Unknown"),
            "img_url": character.get("img_url", "")
        }
        reward_description = f"{copies}x {character.get('name', 'Unknown')} from {character.get('anime', 'Unknown')}"
    
    # Generate unique redeem code
    redeem_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # Ensure code is unique
    while await redeem_collection.find_one({"code": redeem_code}):
        redeem_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    # Create the redeem code document
    redeem_data = {
        "code": redeem_code,
        "reward_type": reward_type,
        "reward_data": reward_data,
        "reward_description": reward_description,
        "creator_id": user_id,
        "created_at": datetime.utcnow(),
        "timestamp": time.time(),
        "limit": limit,  # How many users can redeem
        "redeemed_count": 0,  # How many have redeemed
        "redeemed_by": [],  # List of user IDs who redeemed
        "is_active": True
    }
    
    await redeem_collection.insert_one(redeem_data)
    
    # Prepare response message
    response = (
        f"✅ **Redeem Code Generated Successfully!**\n\n"
        f"🎟 **Code:** `{redeem_code}`\n"
        f"📦 **Reward:** {reward_description}\n"
        f"👥 **Redeem Limit:** {limit} users\n"
        f"👤 **Created By:** {message.from_user.first_name or 'Unknown'}\n"
        f"📅 **Created:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n"
        f"🔄 **Status:** Active\n\n"
        f"Share this code with users. They can redeem it using `/redeem {redeem_code}`"
    )
    
    await message.reply_text(response, parse_mode=enums.ParseMode.MARKDOWN)
    
    # Log the generation
    await app.send_message(
        chat_id=BOT_LOGGING,
        text=f"🦋 **[REDEEM CODE GENERATED]**\n"
             f"👤 **Creator:** {message.from_user.first_name} (`{user_id}`)\n"
             f"🎟 **Code:** `{redeem_code}`\n"
             f"📦 **Reward:** {reward_description}\n"
             f"👥 **Limit:** {limit} users\n"
             f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        parse_mode=enums.ParseMode.MARKDOWN
    )


# ==========================================
# COMMAND: /redeem (Public - Anyone can use)
# ==========================================

@app.on_message(filters.command("redeem"))
async def redeem_code(client, message):
    """
    Redeem a code for coins or characters.
    Anyone can use this command.
    """
    args = message.command
    user_id = message.from_user.id
    
    if len(args) < 2:
        await message.reply_text(
            "**Usage:** `/redeem <code>`\n\n"
            "Redeem your code to receive coins or characters!",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    redeem_code = args[1]
    
    # Special April Fool's code
    if redeem_code == "1APRGIFT":
        await message.reply_text("🤣 Aap pagal ban chuke ho! Happy April Fool! 🎉", parse_mode=enums.ParseMode.MARKDOWN)
        return
    
    # Find the redeem code in database
    redeem_data = await redeem_collection.find_one({"code": redeem_code})
    
    if not redeem_data:
        await message.reply_text(
            "❌ **Invalid or expired redeem code.**\n\n"
            "The code you entered does not exist or has been removed.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Check if code is active
    if not redeem_data.get("is_active", True):
        await message.reply_text(
            "❌ **This code has been deactivated.**\n\n"
            "The code is no longer active.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Check if user has already redeemed this code
    redeemed_by = redeem_data.get("redeemed_by", [])
    if user_id in redeemed_by:
        await message.reply_text(
            "❌ **You have already redeemed this code!**\n\n"
            "Each code can only be redeemed once per user.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Check if code has reached its limit
    redeemed_count = redeem_data.get("redeemed_count", 0)
    limit = redeem_data.get("limit", 1)
    
    if redeemed_count >= limit:
        await message.reply_text(
            f"❌ **This code has reached its limit!**\n\n"
            f"All {limit} redemption slots have been used.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Process redemption based on reward type
    reward_type = redeem_data.get("reward_type")
    reward_data = redeem_data.get("reward_data")
    
    try:
        if reward_type == "coins":
            # Handle coin redemption
            coin_amount = int(reward_data)
            
            # Add coins to user's balance
            await user_collection.update_one(
                {'id': user_id},
                {'$inc': {'balance': coin_amount}},
                upsert=True
            )
            
            # Get updated balance
            user_balance = await user_collection.find_one({'id': user_id}, {'balance': 1})
            new_balance = user_balance.get('balance', coin_amount) if user_balance else coin_amount
            
            # Mark code as redeemed by this user
            await redeem_collection.update_one(
                {"code": redeem_code},
                {
                    "$push": {"redeemed_by": user_id},
                    "$inc": {"redeemed_count": 1}
                }
            )
            
            # Send success message
            await message.reply_text(
                f"💰 **Redeem Successful!**\n\n"
                f"🎉 You received `{coin_amount:,}` coins!\n"
                f"💳 **New Balance:** `{new_balance:,}` coins\n\n"
                f"🎟 **Code:** `{redeem_code}`\n"
                f"👥 **Remaining Slots:** {limit - (redeemed_count + 1)}",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            
            # Log the redemption
            await app.send_message(
                chat_id=BOT_LOGGING,
                text=f"💰 **[COIN REDEEMED]**\n"
                     f"👤 **User:** {message.from_user.first_name} (`{user_id}`)\n"
                     f"🎟 **Code:** `{redeem_code}`\n"
                     f"💳 **Amount:** `{coin_amount:,}` coins\n"
                     f"👥 **Remaining:** {limit - (redeemed_count + 1)} slots\n"
                     f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            
        elif reward_type == "character":
            # Handle character redemption
            character_id = reward_data.get("character_id")
            copies = reward_data.get("copies", 1)
            character_name = reward_data.get("character_name", "Unknown")
            
            # Get character from main collection
            character = await collection.find_one({'id': character_id})
            
            if not character:
                # Character might have been deleted from main collection
                await message.reply_text(
                    f"❌ **Character Not Found!**\n\n"
                    f"The character `{character_name}` is no longer available.\n"
                    f"Please contact support.",
                    parse_mode=enums.ParseMode.MARKDOWN
                )
                return
            
            # Add multiple copies to user's collection
            for _ in range(copies):
                await user_collection.update_one(
                    {'id': user_id},
                    {'$push': {'characters': character}},
                    upsert=True
                )
            
            # Mark code as redeemed by this user
            await redeem_collection.update_one(
                {"code": redeem_code},
                {
                    "$push": {"redeemed_by": user_id},
                    "$inc": {"redeemed_count": 1}
                }
            )
            
            # Get updated collection count
            user = await user_collection.find_one({'id': user_id})
            char_count = len(user.get('characters', [])) if user else 0
            
            # Prepare character info
            char_info = (
                f"🎭 **Character:** `{character.get('name', 'Unknown')}`\n"
                f"📺 **Anime:** `{character.get('anime', 'Unknown')}`\n"
                f"🌟 **Rarity:** `{character.get('rarity', 'Unknown')}`\n"
                f"📦 **Copies Received:** `{copies}`\n"
                f"🖼 **Image:** [Click Here]({character.get('img_url', '#')})\n"
            )
            
            # Send success message
            await message.reply_text(
                f"🎉 **Redeem Successful!**\n\n"
                f"{char_info}\n"
                f"📊 **Total Characters:** `{char_count}`\n\n"
                f"🎟 **Code:** `{redeem_code}`\n"
                f"👥 **Remaining Slots:** {limit - (redeemed_count + 1)}",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            
            # Log the redemption
            await app.send_message(
                chat_id=BOT_LOGGING,
                text=f"🎭 **[CHARACTER REDEEMED]**\n"
                     f"👤 **User:** {message.from_user.first_name} (`{user_id}`)\n"
                     f"🎟 **Code:** `{redeem_code}`\n"
                     f"📦 **Character:** {character.get('name', 'Unknown')} x{copies}\n"
                     f"👥 **Remaining:** {limit - (redeemed_count + 1)} slots\n"
                     f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            
        else:
            # Unknown reward type
            await message.reply_text(
                "❌ **Invalid reward type!**\n"
                "Please contact the bot administrator.",
                parse_mode=enums.ParseMode.MARKDOWN
            )
            
    except Exception as e:
        print(f"Error in redeem handler: {e}")
        await message.reply_text(
            "❌ **An error occurred while processing your redemption.**\n\n"
            "Please try again later or contact support.",
            parse_mode=enums.ParseMode.MARKDOWN
        )


# ==========================================
# COMMAND: /mycodes (VIP Only)
# ==========================================

@app.on_message(filters.command("mycodes"))
@require_power("VIP")
async def list_my_codes(client, message):
    """List all redeem codes generated by the user."""
    user_id = message.from_user.id
    
    # Find all codes created by this user
    codes = await redeem_collection.find(
        {"creator_id": user_id}
    ).sort("created_at", -1).to_list(length=50)
    
    if not codes:
        await message.reply_text(
            "📭 **No redeem codes found.**\n\n"
            "You haven't generated any codes yet. Use `/gen` to create some!",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Build response
    response = "🎟 **Your Generated Codes:**\n\n"
    for code_data in codes[:20]:  # Limit to 20 for readability
        code = code_data.get("code")
        reward_desc = code_data.get("reward_description", "Unknown")
        redeemed = code_data.get("redeemed_count", 0)
        limit = code_data.get("limit", 0)
        is_active = "🟢 ACTIVE" if code_data.get("is_active", True) else "🔴 INACTIVE"
        created = code_data.get("created_at")
        created_str = created.strftime("%Y-%m-%d") if created else "Unknown"
        
        response += f"`{code}` - {reward_desc}\n"
        response += f"   Status: {is_active} | Redeemed: {redeemed}/{limit} | Created: {created_str}\n\n"
    
    if len(codes) > 20:
        response += f"\n... and {len(codes) - 20} more codes."
    
    await message.reply_text(response, parse_mode=enums.ParseMode.MARKDOWN)


# ==========================================
# COMMAND: /checkcode (VIP Only)
# ==========================================

@app.on_message(filters.command("checkcode"))
@require_power("VIP")
async def check_code_status(client, message):
    """Check if a redeem code is valid and its status."""
    args = message.command
    
    if len(args) != 2:
        await message.reply_text(
            "**Usage:** `/checkcode <code>`\n\n"
            "Check the status of a redeem code.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    code = args[1]
    code_data = await redeem_collection.find_one({"code": code})
    
    if not code_data:
        await message.reply_text(
            f"❌ **Code Not Found:** `{code}`",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Build status message
    is_active = code_data.get("is_active", True)
    status = "🟢 **ACTIVE**" if is_active else "🔴 **INACTIVE**"
    redeemed = code_data.get("redeemed_count", 0)
    limit = code_data.get("limit", 0)
    
    reward_desc = code_data.get("reward_description", "Unknown")
    creator_id = code_data.get("creator_id", "Unknown")
    created = code_data.get("created_at")
    created_str = created.strftime("%Y-%m-%d %H:%M:%S") if created else "Unknown"
    
    # Get creator info
    creator_name = "Unknown"
    try:
        creator = await client.get_users(creator_id)
        creator_name = creator.first_name
    except:
        pass
    
    response = (
        f"🎟 **Code Status:** `{code}`\n\n"
        f"📦 **Reward:** {reward_desc}\n"
        f"🎯 **Status:** {status}\n"
        f"👥 **Redemptions:** {redeemed}/{limit}\n"
        f"👤 **Creator:** {creator_name} (`{creator_id}`)\n"
        f"📅 **Created:** {created_str} UTC\n"
    )
    
    # Show who redeemed
    if redeemed > 0:
        redeemed_by = code_data.get("redeemed_by", [])
        response += f"\n**Redeemed By:**\n"
        for i, uid in enumerate(redeemed_by[:10], 1):
            try:
                user = await client.get_users(uid)
                name = user.first_name
                response += f"{i}. {name} (`{uid}`)\n"
            except:
                response += f"{i}. `{uid}`\n"
        if len(redeemed_by) > 10:
            response += f"\n... and {len(redeemed_by) - 10} more users."
    
    await message.reply_text(response, parse_mode=enums.ParseMode.MARKDOWN)


# ==========================================
# COMMAND: /deactivatecode (VIP Only)
# ==========================================

@app.on_message(filters.command("deactivatecode"))
@require_power("VIP")
async def deactivate_code(client, message):
    """Deactivate a redeem code (Admin/VIP only)."""
    args = message.command
    
    if len(args) != 2:
        await message.reply_text(
            "**Usage:** `/deactivatecode <code>`\n\n"
            "Deactivate a redeem code. It can no longer be redeemed.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    code = args[1]
    code_data = await redeem_collection.find_one({"code": code})
    
    if not code_data:
        await message.reply_text(
            f"❌ **Code Not Found:** `{code}`",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    if not code_data.get("is_active", True):
        await message.reply_text(
            f"❌ **Code is already inactive:** `{code}`",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Deactivate the code
    await redeem_collection.update_one(
        {"code": code},
        {"$set": {"is_active": False}}
    )
    
    await message.reply_text(
        f"✅ **Code Deactivated:** `{code}`\n\n"
        f"This code can no longer be redeemed.",
        parse_mode=enums.ParseMode.MARKDOWN
    )
    
    # Log the deactivation
    await app.send_message(
        chat_id=BOT_LOGGING,
        text=f"🔴 **[CODE DEACTIVATED]**\n"
             f"👤 **Admin:** {message.from_user.first_name} (`{message.from_user.id}`)\n"
             f"🎟 **Code:** `{code}`\n"
             f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        parse_mode=enums.ParseMode.MARKDOWN
    )


# ==========================================
# COMMAND: /activatecode (VIP Only)
# ==========================================

@app.on_message(filters.command("activatecode"))
@require_power("VIP")
async def activate_code(client, message):
    """Reactivate a deactivated redeem code (Admin/VIP only)."""
    args = message.command
    
    if len(args) != 2:
        await message.reply_text(
            "**Usage:** `/activatecode <code>`\n\n"
            "Reactivate a deactivated redeem code.",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    code = args[1]
    code_data = await redeem_collection.find_one({"code": code})
    
    if not code_data:
        await message.reply_text(
            f"❌ **Code Not Found:** `{code}`",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    if code_data.get("is_active", True):
        await message.reply_text(
            f"⚠️ **Code is already active:** `{code}`",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Check if code still has remaining slots
    redeemed = code_data.get("redeemed_count", 0)
    limit = code_data.get("limit", 0)
    
    if redeemed >= limit:
        await message.reply_text(
            f"❌ **Cannot reactivate:** `{code}`\n\n"
            f"This code has already reached its redemption limit ({limit}/{limit}).",
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return
    
    # Reactivate the code
    await redeem_collection.update_one(
        {"code": code},
        {"$set": {"is_active": True}}
    )
    
    remaining = limit - redeemed
    await message.reply_text(
        f"✅ **Code Reactivated:** `{code}`\n\n"
        f"👥 **Remaining Slots:** {remaining}",
        parse_mode=enums.ParseMode.MARKDOWN
    )
    
    # Log the reactivation
    await app.send_message(
        chat_id=BOT_LOGGING,
        text=f"🟢 **[CODE REACTIVATED]**\n"
             f"👤 **Admin:** {message.from_user.first_name} (`{message.from_user.id}`)\n"
             f"🎟 **Code:** `{code}`\n"
             f"👥 **Remaining Slots:** {remaining}\n"
             f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
        parse_mode=enums.ParseMode.MARKDOWN
    )
