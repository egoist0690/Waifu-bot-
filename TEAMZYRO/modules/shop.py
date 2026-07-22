
# ==========================================

import random
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bson import ObjectId
from pyrogram import filters
from pyrogram.enums import ParseMode
from TEAMZYRO import *

user_shop_state = {}
DEFAULT_DISCOUNT = 9

# ==========================================
# RARITY PRICE STRUCTURE (Shinobu Themed)
# ==========================================

RARITY_PRICE = {
    "⚪️ Common": 1_000,           # 1K - Common garden spirits
    "🟣 Rare": 5_000,              # 5K - Rare butterflies
    "🟢 Medium": 15_000,           # 15K - Medium-rank spirits
    "🟡 Legendary": 30_000,        # 30K - Legendary souls
    "💮 Special Edition": 50_000,  # 50K - Special blooms
    "🔮 Limited Edition": 75_000,  # 75K - Limited treasures
    "💸 Premium": 200_000,         # 120K - Premium garden guests 🌸
    "🌤 Summer": 80_000,           # 25K - Summer spirits
    "🎐 Enchanted": 75_000,        # 45K - Enchanted beings
    "❄️ Frozen": 80_000,          # 40K - Frozen souls
    "💝 Romantic": 85_000,         # 35K - Romantic spirits
    "🎃 Haunted": 75_000,          # 55K - Haunted entities
    "🎄 Christmas": 70_000,        # 60K - Christmas spirits
    "🧧 Festive": 100_000,          # 45K - Festive guests
    "🍑 Naughty": 100_000,          # 65K - Naughty spirits
    "🎗️ AMV": 200_000,             # 20K - AMV edition
    "🌧 Cloudy": 80_000,           # 30K - Cloudy spirits
    "🦠 Mythgard": 500_000,        # 100K - Mythical beings
}

RARITY_EMOJIS = {
    "⚪️ Common": "⚪️",
    "🟣 Rare": "🟣",
    "🟢 Medium": "🟢",
    "🟡 Legendary": "🟡",
    "💮 Special Edition": "💮",
    "🔮 Limited Edition": "🔮",
    "💸 Premium": "💸",
    "🌤 Summer": "🌤",
    "🎐 Enchanted": "🎐",
    "❄️ Frozen": "❄️",
    "💝 Romantic": "💝",
    "🎃 Haunted": "🎃",
    "🎄 Christmas": "🎄",
    "🧧 Festive": "🧧",
    "🍑 Naughty": "🍑",
    "🎗️ AMV": "🎗️",
    "🌧 Cloudy": "🌧",
    "🦠 Mythgard": "🦠",
}

# Elegant rarity descriptions
RARITY_DESCRIPTIONS = {
    "⚪️ Common": "A gentle spirit that blooms in every garden—simple, yet charming.",
    "🟣 Rare": "A butterfly with a delicate hue—not easily found, but worth the search.",
    "🟢 Medium": "Neither common nor rare—a balanced spirit with quiet strength.",
    "🟡 Legendary": "A soul that echoes through time—legendary tales are woven around them.",
    "💮 Special Edition": "A rare bloom that appears only during special seasons—cherish it.",
    "🔮 Limited Edition": "A treasure from beyond the veil—once it's gone, it's gone forever.",
    "💸 Premium": "The crown jewel of the garden—only the most dedicated collectors may obtain this spirit.",
    "🌤 Summer": "A radiant spirit born from the summer sun's warm embrace.",
    "🎐 Enchanted": "A mystical being touched by ancient magic and wonder.",
    "❄️ Frozen": "A spirit preserved in eternal winter's icy beauty.",
    "💝 Romantic": "A soul filled with love and passion—perfect for Valentine's Day.",
    "🎃 Haunted": "A mysterious entity from the shadowy realm of Halloween.",
    "🎄 Christmas": "A festive spirit spreading joy and holiday cheer.",
    "🧧 Festive": "A celebration spirit that brings good fortune and happiness.",
    "🍑 Naughty": "A cheeky spirit with a mischievous glint in their eye.",
    "🎗️ AMV": "A dynamic spirit full of energy and rhythm.",
    "🌧 Cloudy": "A melancholic spirit that brings gentle rain and reflection.",
    "🦠 Mythgard": "A legendary being from the mythical realms of old.",
}

# RARITY ORDER FOR DISPLAY
RARITY_ORDER = [
    "⚪️ Common",
    "🟣 Rare",
    "🟢 Medium",
    "🟡 Legendary",
    "💮 Special Edition",
    "🔮 Limited Edition",
    "💸 Premium",
    "🌤 Summer",
    "🎐 Enchanted",
    "❄️ Frozen",
    "💝 Romantic",
    "🎃 Haunted",
    "🎄 Christmas",
    "🧧 Festive",
    "🍑 Naughty",
    "🎗️ AMV",
    "🌧 Cloudy",
    "🦠 Mythgard",
]

# ... rest of shop.py remains the same ...,

# Premium rarity only for shop
PREMIUM_RARITY = "💸 Premium Edition"

# Safe split
def safe_split(data, sep="_", expected=2):
    parts = data.split(sep)
    if len(parts) < expected:
        parts += [None] * (expected - len(parts))
    return parts[:expected]


async def get_active_discount():
    discount = await discounts_collection.find_one({})
    if discount and discount["expires_at"] > datetime.utcnow():
        return discount["percent"]
    return DEFAULT_DISCOUNT


def is_video(url):
    return any(url.lower().endswith(ext) for ext in [".mp4", ".mov", ".webm"])


# ==========================================
# SHOP STOCK MANAGEMENT COLLECTION
# ==========================================

shop_stock_collection = db['shop_stock']  # Collection for shop inventory


# ==========================================
# COMMAND: /ashop (Owner Only - Add Stock with Custom Price)
# ==========================================

@app.on_message(filters.command("ashop"))
async def add_shop_stock(client, message):
    """
    Add a character to the shop with specified stock and custom price.
    Usage: /ashop <character_id> <price> <amount>
    Example: /ashop 12345 150000 4
    
    Sets character ID 12345 with price 150,000 petals and 4 stock.
    """
    # Owner-only check
    if message.from_user.id != OWNER_ID:
        await message.reply_text("🌸 *Ara ara~* Only the garden keeper can manage the shop inventory!")
        return
    
    args = message.text.split()
    
    if len(args) != 4:
        await message.reply_text(
            "🌸 **Usage:** `/ashop <character_id> <price> <amount>`\n\n"
            "**Example:** `/ashop 12345 150000 4`\n"
            "Sets character ID 12345 with price 150,000 petals and 4 stock.\n\n"
            "**Minimum Price:** 100 petals\n"
            "**Maximum Price:** 9,999,999 petals"
        )
        return
    
    character_id = args[1]
    
    try:
        price = int(args[2])
        if price < 100:
            await message.reply_text("🌸 *Fufufu~* Minimum price is 100 petals!")
            return
        if price > 9999999:
            await message.reply_text("🌸 *Ara~* Maximum price is 9,999,999 petals!")
            return
    except ValueError:
        await message.reply_text("🌸 *Ara ara~* Please enter a valid number for the price!")
        return
    
    try:
        amount = int(args[3])
        if amount <= 0:
            await message.reply_text("🌸 *Fufufu~* Amount must be a positive number!")
            return
        if amount > 999:
            await message.reply_text("🌸 *Ara~* Maximum stock per character is 999!")
            return
    except ValueError:
        await message.reply_text("🌸 *Ara ara~* Please enter a valid number for the amount!")
        return
    
    # Check if character exists in main collection
    character = await collection.find_one({'id': character_id})
    if not character:
        await message.reply_text(f"🌸 *Ara ara~* Character with ID `{character_id}` not found in the garden!")
        return
    
    # Check if character is Premium rarity (shop requirement)
    if character.get('rarity') != PREMIUM_RARITY:
        await message.reply_text(
            f"🌸 *Fufufu~* Character `{character['name']}` has rarity `{character.get('rarity', 'Unknown')}`.\n"
            f"The shop only accepts Premium Edition spirits!"
        )
        return
    
    # Check if character already exists in shop stock
    existing_stock = await shop_stock_collection.find_one({'character_id': character_id})
    
    if existing_stock:
        # Update existing stock and price
        new_amount = existing_stock['stock'] + amount
        old_price = existing_stock.get('price', RARITY_PRICE.get(PREMIUM_RARITY, 120000))
        await shop_stock_collection.update_one(
            {'character_id': character_id},
            {
                '$set': {
                    'stock': new_amount,
                    'price': price,
                    'last_updated': datetime.utcnow()
                }
            }
        )
        await message.reply_text(
            f"🌸 **Stock & Price Updated!**\n\n"
            f"✨ **Character:** {character['name']}\n"
            f"🆔 **ID:** `{character_id}`\n"
            f"🌸 **Old Price:** `{old_price:,}` → **New Price:** `{price:,}` petals\n"
            f"📦 **Previous Stock:** {existing_stock['stock']}\n"
            f"➕ **Added:** +{amount}\n"
            f"📊 **New Stock:** {new_amount}\n\n"
            f"*Fufufu~* The spirit's value has been updated in the bazaar!"
        )
    else:
        # Create new stock entry with custom price
        await shop_stock_collection.insert_one({
            'character_id': character_id,
            'character_data': character,  # Store full character data
            'stock': amount,
            'price': price,  # Custom price for this character
            'added_by': message.from_user.id,
            'added_at': datetime.utcnow(),
            'last_updated': datetime.utcnow()
        })
        await message.reply_text(
            f"🌸 **Character Added to Shop!**\n\n"
            f"✨ **Character:** {character['name']}\n"
            f"⛩️ **Anime:** {character.get('anime', 'Unknown')}\n"
            f"🌟 **Rarity:** {character.get('rarity', 'Premium')}\n"
            f"🆔 **ID:** `{character_id}`\n"
            f"🌸 **Price:** `{price:,}` wisteria petals\n"
            f"📦 **Stock:** {amount}\n\n"
            f"*Fufufu~* A new spirit has arrived in the bazaar with a custom price!*"
        )
    
    # Log the addition
    await PLOG(
        f"🌸 **[SHOP STOCK ADDED]**\n"
        f"👤 **Owner:** {message.from_user.first_name} (`{message.from_user.id}`)\n"
        f"🆔 **Character ID:** `{character_id}`\n"
        f"🌸 **Price Set:** {price:,} petals\n"
        f"📦 **Amount Added:** +{amount}\n"
        f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )


# ==========================================
# COMMAND: /rshop (Owner Only - Remove Stock)
# ==========================================

@app.on_message(filters.command("rshop"))
async def remove_shop_stock(client, message):
    """
    Remove stock from a character in the shop.
    Usage: /rshop <character_id> <amount>
    Example: /rshop 12345 2
    """
    # Owner-only check
    if message.from_user.id != OWNER_ID:
        await message.reply_text("🌸 *Ara ara~* Only the garden keeper can manage the shop inventory!")
        return
    
    args = message.text.split()
    
    if len(args) != 3:
        await message.reply_text(
            "🌸 **Usage:** `/rshop <character_id> <amount>`\n\n"
            "**Example:** `/rshop 12345 2`\n"
            "Removes 2 stock from character ID 12345."
        )
        return
    
    character_id = args[1]
    
    try:
        amount = int(args[2])
        if amount <= 0:
            await message.reply_text("🌸 *Fufufu~* Amount must be a positive number!")
            return
    except ValueError:
        await message.reply_text("🌸 *Ara ara~* Please enter a valid number for the amount!")
        return
    
    # Check if character exists in shop stock
    existing_stock = await shop_stock_collection.find_one({'character_id': character_id})
    
    if not existing_stock:
        await message.reply_text(
            f"🌸 *Ara ara~* Character with ID `{character_id}` is not in the shop inventory!"
        )
        return
    
    current_stock = existing_stock['stock']
    character_name = existing_stock.get('character_data', {}).get('name', 'Unknown')
    current_price = existing_stock.get('price', RARITY_PRICE.get(PREMIUM_RARITY, 120000))
    new_stock = current_stock - amount
    
    if new_stock < 0:
        await message.reply_text(
            f"🌸 *Ara ara~* Cannot remove {amount} stock!\n\n"
            f"✨ **Character:** {character_name}\n"
            f"🌸 **Price:** {current_price:,} petals\n"
            f"📦 **Current Stock:** {current_stock}\n"
            f"❌ **Requested Removal:** {amount}\n\n"
            f"*Fufufu~* You can only remove up to {current_stock} stock!"
        )
        return
    
    if new_stock == 0:
        # Remove character completely from shop
        await shop_stock_collection.delete_one({'character_id': character_id})
        await message.reply_text(
            f"🌸 **Character Removed from Shop!**\n\n"
            f"✨ **Character:** {character_name}\n"
            f"🆔 **ID:** `{character_id}`\n"
            f"🌸 **Price was:** {current_price:,} petals\n"
            f"📦 **Stock Removed:** {amount}\n"
            f"📊 **Remaining Stock:** 0\n\n"
            f"*Fufufu~* The spirit has been withdrawn from the bazaar."
        )
    else:
        # Update stock
        await shop_stock_collection.update_one(
            {'character_id': character_id},
            {'$set': {'stock': new_stock, 'last_updated': datetime.utcnow()}}
        )
        await message.reply_text(
            f"🌸 **Stock Updated!**\n\n"
            f"✨ **Character:** {character_name}\n"
            f"🆔 **ID:** `{character_id}`\n"
            f"🌸 **Price:** {current_price:,} petals\n"
            f"📦 **Previous Stock:** {current_stock}\n"
            f"➖ **Removed:** -{amount}\n"
            f"📊 **New Stock:** {new_stock}\n\n"
            f"*Fufufu~* The spirit's presence has been reduced in the bazaar."
        )
    
    # Log the removal
    await PLOG(
        f"🌸 **[SHOP STOCK REMOVED]**\n"
        f"👤 **Owner:** {message.from_user.first_name} (`{message.from_user.id}`)\n"
        f"🆔 **Character ID:** `{character_id}`\n"
        f"📦 **Amount Removed:** -{amount}\n"
        f"📊 **New Stock:** {new_stock if new_stock > 0 else 'Removed from shop'}\n"
        f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )


# ==========================================
# COMMAND: /shop - Premium Only Direct Display
# ==========================================

@app.on_message(filters.command(["shop", "hshop", "hshopmenu"]))
async def shop_menu(client, message):
    """
    Display shop with only Premium characters.
    Shows character image, info, and buy button.
    """
    user_id = message.from_user.id
    
    # Get all Premium characters with stock
    all_premium = await collection.find({"rarity": PREMIUM_RARITY}).to_list(None)
    
    if not all_premium:
        await message.reply_text(
            "🌸 *Ara ara~* No Premium spirits available in the garden!\n\n"
            "*Fufufu~* Please check back later for new arrivals."
        )
        return
    
    # Get shop stock for Premium characters
    character_ids = [char['id'] for char in all_premium]
    stock_entries = await shop_stock_collection.find(
        {'character_id': {'$in': character_ids}, 'stock': {'$gt': 0}}
    ).to_list(None)
    
    # Create a dict of character_id -> stock and price
    stock_dict = {entry['character_id']: entry['stock'] for entry in stock_entries}
    price_dict = {entry['character_id']: entry.get('price', RARITY_PRICE.get(PREMIUM_RARITY, 120000)) for entry in stock_entries}
    
    # Filter characters to only those in stock
    characters = [char for char in all_premium if char['id'] in stock_dict]
    
    if not characters:
        await message.reply_text(
            "🌸 *Ara ara~* No Premium spirits are currently in stock!\n\n"
            "*Fufufu~* The bazaar will be restocked soon. Please check back later."
        )
        return
    
    random.shuffle(characters)
    
    # Get user's balance
    user = await user_collection.find_one({"id": user_id})
    balance = user.get("balance", 0) if user else 0
    
    # Store shop state
    user_shop_state[user_id] = {
        "index": 0,
        "characters": characters,
        "stock_dict": stock_dict,
        "price_dict": price_dict,
        "balance": balance,
        "message_id": None,
        "chat_id": message.chat.id
    }
    
    # Display first character
    await display_shop_character(client, message, user_id, is_initial=True)


async def display_shop_character(client, message, user_id, is_initial=False, callback_query=None):
    """
    Display a single character with image, info, and buy button.
    Properly updates image when navigating.
    """
    state = user_shop_state.get(user_id)
    if not state:
        return
    
    index = state["index"]
    characters = state["characters"]
    stock_dict = state["stock_dict"]
    price_dict = state.get("price_dict", {})
    
    # Check if index is valid
    if index >= len(characters):
        index = 0
        state["index"] = 0
    
    char = characters[index]
    char_id = char.get('id')
    stock_count = stock_dict.get(char_id, 0)
    
    # Get custom price or fallback to default
    price = price_dict.get(char_id, RARITY_PRICE.get(PREMIUM_RARITY, 120000))
    discount = await get_active_discount()
    discounted_price = int(price * (100 - discount) / 100)
    original_price_display = f"~~{price:,}~~" if discount > 0 else ""
    
    # Get user's balance
    user = await user_collection.find_one({"id": user_id})
    balance = user.get("balance", 0) if user else 0
    state["balance"] = balance
    
    # Determine if user can afford
    can_afford = balance >= discounted_price and stock_count > 0
    
    # Build caption
    caption = (
        f"🌸 **Wisteria Bazaar** 🌸\n\n"
        f"✨ **Name:** {char['name']}\n"
        f"⛩️ **Anime:** {char.get('anime', 'Unknown')}\n"
        f"🌟 **Rarity:** {char.get('rarity', 'Premium')}\n"
        f"🌸 **Price:** {original_price_display} `{discounted_price:,}` wisteria petals"
        f"{f' ({discount}% off!)' if discount > 0 else ''}\n"
        f"📦 **Stock:** `{stock_count}`\n"
        f"💳 **Your Petals:** `{balance:,}`\n\n"
        f"*{RARITY_DESCRIPTIONS.get(char.get('rarity', ''), 'A beautiful Premium spirit awaits you~')}*"
    )
    
    # Build navigation and buy buttons (NO REFRESH BUTTON)
    keyboard = []
    
    # Navigation row with counter
    nav_buttons = []
    if index > 0:
        nav_buttons.append(InlineKeyboardButton("◀️ Prev", callback_data=f"shop_prev_{user_id}"))
    
    # Show current position
    nav_buttons.append(InlineKeyboardButton(f"{index + 1}/{len(characters)}", callback_data="shop_noop"))
    
    if index < len(characters) - 1:
        nav_buttons.append(InlineKeyboardButton("Next ▶️", callback_data=f"shop_next_{user_id}"))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    # Buy button
    if can_afford:
        keyboard.append([
            InlineKeyboardButton(f"🌸 Buy ({discounted_price:,} petals)", callback_data=f"shop_buy_{user_id}_{index}")
        ])
    else:
        if stock_count == 0:
            keyboard.append([
                InlineKeyboardButton("🔒 Out of Stock", callback_data="shop_noop")
            ])
        else:
            keyboard.append([
                InlineKeyboardButton(f"🔒 Need {discounted_price - balance:,} more petals", callback_data="shop_noop")
            ])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Get the image URL
    img_url = char.get("img_url", "")
    is_video_file = is_video(img_url)
    
    # Send or edit message with proper media
    if is_initial:
        # Send new message with character image
        if is_video_file:
            sent_msg = await message.reply_video(
                video=img_url,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            sent_msg = await message.reply_photo(
                photo=img_url,
                caption=caption,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        # Store message ID for later editing
        state["message_id"] = sent_msg.id
        state["chat_id"] = sent_msg.chat.id
    else:
        # Edit existing message - properly update image
        try:
            if is_video_file:
                await callback_query.message.edit_media(
                    InputMediaVideo(media=img_url, caption=caption, parse_mode=ParseMode.MARKDOWN),
                    reply_markup=reply_markup
                )
            else:
                await callback_query.message.edit_media(
                    InputMediaPhoto(media=img_url, caption=caption, parse_mode=ParseMode.MARKDOWN),
                    reply_markup=reply_markup
                )
        except Exception as e:
            # If media edit fails (e.g., same media type), try editing text
            try:
                await callback_query.message.edit_caption(
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception:
                # Fallback: edit text only
                await callback_query.message.edit_text(
                    caption,
                    reply_markup=reply_markup,
                    parse_mode=ParseMode.MARKDOWN
                )


# ==========================================
# SHOP NAVIGATION CALLBACKS
# ==========================================

@app.on_callback_query(filters.regex(r"^shop_next_(\d+)$"))
async def shop_next_character(client, callback_query):
    user_id = int(callback_query.matches[0].group(1))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("🌸 *Ara~* This isn't your shop session!", show_alert=True)
        return
    
    state = user_shop_state.get(user_id)
    if not state:
        await callback_query.answer("🌸 *Ara~* Your session has expired. Please start from /shop again!", show_alert=True)
        return
    
    if state["index"] >= len(state["characters"]) - 1:
        await callback_query.answer("🌸 *Fufufu~* You're at the last spirit!", show_alert=True)
        return
    
    state["index"] += 1
    await display_shop_character(client, callback_query.message, user_id, is_initial=False, callback_query=callback_query)
    await callback_query.answer()


@app.on_callback_query(filters.regex(r"^shop_prev_(\d+)$"))
async def shop_prev_character(client, callback_query):
    user_id = int(callback_query.matches[0].group(1))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("🌸 *Ara~* This isn't your shop session!", show_alert=True)
        return
    
    state = user_shop_state.get(user_id)
    if not state:
        await callback_query.answer("🌸 *Ara~* Your session has expired. Please start from /shop again!", show_alert=True)
        return
    
    if state["index"] <= 0:
        await callback_query.answer("🌸 *Fufufu~* You're at the first spirit!", show_alert=True)
        return
    
    state["index"] -= 1
    await display_shop_character(client, callback_query.message, user_id, is_initial=False, callback_query=callback_query)
    await callback_query.answer()


# ==========================================
# SHOP BUY CALLBACK
# ==========================================

@app.on_callback_query(filters.regex(r"^shop_buy_(\d+)_(\d+)$"))
async def shop_buy_character(client, callback_query):
    user_id = int(callback_query.matches[0].group(1))
    index = int(callback_query.matches[0].group(2))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("🌸 *Ara~* This isn't your shop session!", show_alert=True)
        return
    
    state = user_shop_state.get(user_id)
    if not state:
        await callback_query.answer("🌸 *Ara~* Your session has expired. Please start from /shop again!", show_alert=True)
        return
    
    if index != state["index"]:
        await callback_query.answer("🌸 *Ara~* This spirit has changed! Please refresh.", show_alert=True)
        return
    
    char = state["characters"][index]
    char_id = char.get('id')
    
    # Check stock
    stock_entry = await shop_stock_collection.find_one({'character_id': char_id})
    if not stock_entry or stock_entry.get('stock', 0) <= 0:
        await callback_query.answer("🌸 *Ara ara~* This spirit is out of stock!", show_alert=True)
        return
    
    # Check user
    user = await user_collection.find_one({"id": user_id})
    if not user:
        await callback_query.answer("🌸 *Oh my~* I don't recognize you!", show_alert=True)
        return
    
    # Get custom price from stock entry
    price = stock_entry.get('price', RARITY_PRICE.get(PREMIUM_RARITY, 120000))
    discount = await get_active_discount()
    discounted_price = int(price * (100 - discount) / 100)
    
    # Check balance
    if user.get("balance", 0) < discounted_price:
        needed = discounted_price - user.get("balance", 0)
        await callback_query.answer(
            f"🌸 *Ara ara~* You need {needed:,} more wisteria petals!",
            show_alert=True
        )
        return
    
    # Check if user already has this character
    existing_chars = user.get("characters", [])
    for existing in existing_chars:
        if existing.get("id") == char_id:
            await callback_query.answer(
                "🌸 *Fufufu~* This spirit already resides in your garden!",
                show_alert=True
            )
            return
    
    # Decrease stock
    new_stock = stock_entry['stock'] - 1
    if new_stock == 0:
        await shop_stock_collection.delete_one({'character_id': char_id})
        # Update stock dict in state
        state["stock_dict"][char_id] = 0
    else:
        await shop_stock_collection.update_one(
            {'character_id': char_id},
            {'$set': {'stock': new_stock}}
        )
        state["stock_dict"][char_id] = new_stock
    
    # Deduct petals and add character to user's collection
    await user_collection.update_one(
        {"id": user_id},
        {
            "$inc": {"balance": -discounted_price},
            "$push": {"characters": {
                "_id": ObjectId(),
                "img_url": char.get("img_url", ""),
                "name": char.get("name", "Unknown"),
                "anime": char.get("anime", "Unknown"),
                "rarity": char.get("rarity", "Premium"),
                "id": char_id
            }}
        }
    )
    
    # Get updated balance
    updated_user = await user_collection.find_one({"id": user_id})
    new_balance = updated_user.get("balance", 0) if updated_user else 0
    
    # Update state balance
    state["balance"] = new_balance
    
    # Remove the character from the list if stock is 0
    if new_stock == 0:
        # Remove from characters list
        state["characters"].pop(index)
        # If we removed the last character, go to previous
        if state["index"] >= len(state["characters"]):
            state["index"] = len(state["characters"]) - 1
        
        # If no characters left, close shop
        if not state["characters"]:
            await callback_query.message.edit_text(
                "🌸 *Ara ara~* All spirits have found new homes!\n\n"
                "*Fufufu~* The bazaar is empty for now. Please check back later for new arrivals."
            )
            await callback_query.answer(
                f"🌸 *Wonderful!* {char.get('name', 'Unknown')} has joined your garden! 🦋",
                show_alert=True
            )
            return
    
    # Success message
    await callback_query.answer(
        f"🌸 *Wonderful!* {char.get('name', 'Unknown')} has joined your garden! 🦋",
        show_alert=True
    )
    
    # Update the displayed character with new balance
    await display_shop_character(client, callback_query.message, user_id, is_initial=False, callback_query=callback_query)
    
    # Log the purchase
    await PLOG(
        f"🌸 **[SHOP PURCHASE]**\n"
        f"👤 **User:** {callback_query.from_user.first_name} (`{user_id}`)\n"
        f"🆔 **Character:** {char.get('name', 'Unknown')} (`{char_id}`)\n"
        f"🌸 **Price:** {discounted_price:,} petals\n"
        f"📦 **Remaining Stock:** {new_stock}\n"
        f"📅 **Time:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )


# ==========================================
# NOOP CALLBACK (for disabled buttons)
# ==========================================

@app.on_callback_query(filters.regex(r"^shop_noop$"))
async def shop_noop_callback(client, callback_query):
    await callback_query.answer()
