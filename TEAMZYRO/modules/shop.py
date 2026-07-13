# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

import random
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bson import ObjectId
from pyrogram import filters
from pyrogram.enums import ParseMode
from TEAMZYRO import *

user_shop_state = {}
DEFAULT_DISCOUNT = 12

# ==========================================
# RARITY PRICE STRUCTURE (Shinobu Themed)
# ==========================================

RARITY_PRICE = {
    "⚪️ Common": 1_000,           # 1K - Common garden spirits
    "🟣 Rare": 5_000,              # 5K - Rare butterflies
    "🟡 Legendary": 15_000,        # 15K - Legendary souls
    "🟢 Medium": 30_000,           # 30K - Medium-rank spirits
    "💮 Special Edition": 50_000,  # 50K - Special blooms
    "🔮 Limited Edition": 75_000,  # 75K - Limited treasures
    "💸 Premium Edition": 120_000, # 120K - Premium garden guests 🌸
}

RARITY_EMOJIS = {
    "⚪️ Common": "⚪️",
    "🟣 Rare": "🟣",
    "🟡 Legendary": "🟡",
    "🟢 Medium": "🟢",
    "💮 Special Edition": "💮",
    "🔮 Limited Edition": "🔮",
    "💸 Premium Edition": "💸",
}

# Shinobu's elegant rarity descriptions
RARITY_DESCRIPTIONS = {
    "⚪️ Common": "A gentle spirit that blooms in every garden—simple, yet charming.",
    "🟣 Rare": "A butterfly with a delicate hue—not easily found, but worth the search.",
    "🟡 Legendary": "A soul that echoes through time—legendary tales are woven around them.",
    "🟢 Medium": "Neither common nor rare—a balanced spirit with quiet strength.",
    "💮 Special Edition": "A rare bloom that appears only during special seasons—cherish it.",
    "🔮 Limited Edition": "A treasure from beyond the veil—once it's gone, it's gone forever.",
    "💸 Premium Edition": "The crown jewel of the garden—only the most dedicated collectors may obtain this spirit.",
}

# ---------------- RARITY ORDER FOR DISPLAY ---------------- #

RARITY_ORDER = [
    "⚪️ Common",
    "🟣 Rare",
    "🟢 Medium",
    "🟡 Legendary",
    "💮 Special Edition",
    "🔮 Limited Edition",
    "💸 Premium Edition",
]


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


# ---------------- DISCOUNT SYSTEM ---------------- #

@app.on_message(filters.command("discount"))
async def set_discount(client, message):
    if message.from_user.id != OWNER_ID:
        return await message.reply("🌸 *Ara ara~* Only the garden keeper can set discounts, dear.")

    args = message.text.split()

    if len(args) < 3:
        return await message.reply(
            "🌸 **Usage:**\n"
            "`/discount <percent> <duration>`\n\n"
            "**Examples:**\n"
            "`/discount 30 1d` - 30% off for 1 day\n"
            "`/discount 25 12h` - 25% off for 12 hours"
        )

    try:
        percent = int(args[1])
    except ValueError:
        return await message.reply("🌸 *Fufufu~* Please enter a valid percentage!")

    duration = args[2].lower()

    if duration.endswith("h"):
        hours = int(duration[:-1])
        expires = datetime.utcnow() + timedelta(hours=hours)

    elif duration.endswith("d"):
        days = int(duration[:-1])
        expires = datetime.utcnow() + timedelta(days=days)

    else:
        return await message.reply("🌸 *Ara~* Duration must end with 'h' (hours) or 'd' (days).")

    await discounts_collection.delete_many({})
    await discounts_collection.insert_one({
        "percent": percent,
        "expires_at": expires
    })

    await message.reply(
        f"🌸 *Wonderful!* A {percent}% discount has been applied for {duration}.\n"
        f"*Fufufu~* The garden spirits will be delighted!"
    )
    

def is_video(url):
    return any(url.lower().endswith(ext) for ext in [".mp4", ".mov", ".webm"])


# ---------------- SHOP MENU ---------------- #

@app.on_message(filters.command(["shop", "hshop", "hshopmenu"]))
async def shop_menu(client, message):
    keyboard = []
    
    # Display rarities in proper order with prices
    for rarity in RARITY_ORDER:
        price = RARITY_PRICE.get(rarity, 1000)
        emoji = RARITY_EMOJIS.get(rarity, "🌸")
        
        # Format price with commas
        price_str = f"{price:,}"
        
        # Add different visual indicators for high value rarities
        if price >= 100_000:
            label = f"👑 {emoji} {rarity} — {price_str} petals"
        elif price >= 50_000:
            label = f"💎 {emoji} {rarity} — {price_str} petals"
        elif price >= 25_000:
            label = f"🌟 {emoji} {rarity} — {price_str} petals"
        else:
            label = f"{emoji} {rarity} — {price_str} petals"
            
        keyboard.append([InlineKeyboardButton(label, callback_data=f"xeno_{RARITY_ORDER.index(rarity)}")])

    await message.reply_photo(
        photo="https://files.catbox.moe/ohi1vs.jpg",
        caption=(
            "🌸 **Welcome to the Wisteria Bazaar!** 🌸\n\n"
            "*Fufufu~* Here, you may acquire beautiful spirits to adorn your garden.\n"
            "Browse by rarity, and remember—each spirit is unique!\n\n"
            "🌸 **Rarity Guide:**\n"
            "╔═══════════════════════════════╗\n"
            "║ ⚪️ Common     →    1,000     ║\n"
            "║ 🟣 Rare       →    5,000     ║\n"
            "║ 🟢 Medium     →   30,000     ║\n"
            "║ 🟡 Legendary  →   15,000     ║\n"
            "║ 💮 Special    →   50,000     ║\n"
            "║ 🔮 Limited    →   75,000     ║\n"
            "║ 💸 Premium    →  120,000 👑  ║\n"
            "╚═══════════════════════════════╝\n\n"
            "✨ *Happy collecting, dear butterfly!*"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# ---------------- SHOW RARITY ---------------- #

@app.on_callback_query(filters.regex(r"^xeno_\d+$"))
async def show_rarity_list(client, callback_query):
    _, index_str = safe_split(callback_query.data, "_", 2)

    rarity = RARITY_ORDER[int(index_str)]
    user_id = callback_query.from_user.id

    # Get characters of this rarity
    characters = await collection.find({"rarity": rarity}).to_list(None)
    if not characters:
        return await callback_query.answer("🌸 *Ara~* No spirits of this rarity are available right now!", show_alert=True)

    random.shuffle(characters)

    # Get user's current balance
    user = await user_collection.find_one({"id": user_id})
    balance = user.get("balance", 0) if user else 0

    user_shop_state[user_id] = {
        "rarity": rarity,
        "index": 0,
        "characters": characters[:5],
        "balance": balance
    }

    await show_character(client, callback_query.message, user_id)
    await callback_query.answer()


# ---------------- SHOW CHARACTER ---------------- #

async def show_character(client, msg, user_id):
    data = user_shop_state[user_id]
    char = data["characters"][data["index"]]

    price = RARITY_PRICE.get(char["rarity"], 1000)
    discount = await get_active_discount()
    discounted_price = int(price * (100 - discount) / 100)
    original_price_display = f"~~{price:,}~~" if discount > 0 else ""

    emoji = RARITY_EMOJIS.get(char["rarity"], "🌸")
    description = RARITY_DESCRIPTIONS.get(char["rarity"], "A beautiful spirit awaits you~")
    
    # Get user's balance
    user = await user_collection.find_one({"id": user_id})
    balance = user.get("balance", 0) if user else 0
    data["balance"] = balance
    
    # Determine if user can afford
    can_afford = balance >= discounted_price
    afford_status = "✅ You can afford this spirit!" if can_afford else f"❌ You need {discounted_price - balance:,} more petals"

    # Price tier indicator
    if price >= 100_000:
        tier_icon = "👑 **Premium Tier** — The rarest of rare!"
    elif price >= 50_000:
        tier_icon = "💎 **Luxury Tier** — A true treasure!"
    elif price >= 25_000:
        tier_icon = "🌟 **Elite Tier** — Exceptional beauty!"
    else:
        tier_icon = "🌸 **Standard Tier** — Lovely in every way!"

    caption = (
        f"🌸 *A beautiful spirit awaits!* 🦋\n\n"
        f"✨ **Name:** {char['name']}\n"
        f"⛩️ **Anime:** {char['anime']}\n"
        f"{emoji} **Rarity:** {char['rarity']}\n"
        f"🌸 **Price:** {original_price_display} `{discounted_price:,}` wisteria petals"
        f"{f' ({discount}% off!)' if discount > 0 else ''}\n"
        f"💳 **Your Petals:** `{balance:,}`\n"
        f"📊 **Status:** {afford_status}\n"
        f"🏷️ **Tier:** {tier_icon}\n\n"
        f"*{description}*\n\n"
        f"🆔 **ID:** `{char['id']}`\n"
        f"*Fufufu~* Will you bring this spirit into your garden?"
    )

    # Build keyboard with different colors/indicators
    claim_button_text = f"🌸 Claim ({discounted_price:,})" if can_afford else f"🔒 Locked ({discounted_price:,})"
    
    keyboard = [
        [
            InlineKeyboardButton("⬅️ Prev", callback_data="prev_char"),
            InlineKeyboardButton(claim_button_text, callback_data=f"claim_{data['index']}"),
            InlineKeyboardButton("Next ➡️", callback_data="next_char"),
        ],
        [
            InlineKeyboardButton("🔄 Refresh (5,000 petals)", callback_data="refresh_chars"),
            InlineKeyboardButton("🏠 Back to Bazaar", callback_data="back_to_shop")
        ]
    ]

    await msg.delete()

    if is_video(char.get("img_url", "")):
        await msg.reply_video(
            video=char["img_url"],
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await msg.reply_photo(
            photo=char.get("img_url", ""),
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.MARKDOWN
        )


# ---------------- NAVIGATION ---------------- #

@app.on_callback_query(filters.regex("^next_char$"))
async def next_character(client, callback_query):
    user_id = callback_query.from_user.id
    state = user_shop_state.get(user_id)

    if not state:
        return await callback_query.answer("🌸 *Ara~* Your session has expired. Please start from /shop again!", True)

    if state["index"] >= len(state["characters"]) - 1:
        return await callback_query.answer("🌸 *Fufufu~* That's the last spirit in this rarity!", True)

    state["index"] += 1
    await show_character(client, callback_query.message, user_id)
    await callback_query.answer()


@app.on_callback_query(filters.regex("^prev_char$"))
async def prev_character(client, callback_query):
    user_id = callback_query.from_user.id
    state = user_shop_state.get(user_id)

    if not state:
        return await callback_query.answer("🌸 *Ara~* Your session has expired. Please start from /shop again!", True)

    if state["index"] <= 0:
        return await callback_query.answer("🌸 *Fufufu~* You're already at the first spirit!", True)

    state["index"] -= 1
    await show_character(client, callback_query.message, user_id)
    await callback_query.answer()


# ---------------- BACK TO SHOP ---------------- #

@app.on_callback_query(filters.regex("^back_to_shop$"))
async def back_to_shop(client, callback_query):
    user_id = callback_query.from_user.id
    user_shop_state.pop(user_id, None)
    
    await callback_query.message.delete()
    await shop_menu(client, callback_query.message)


# ---------------- REFRESH ---------------- #

@app.on_callback_query(filters.regex("^refresh_chars$"))
async def refresh_characters(client, callback_query):
    user_id = callback_query.from_user.id
    state = user_shop_state.get(user_id)

    if not state:
        return await callback_query.answer("🌸 *Ara~* Your session has expired. Please start from /shop again!", True)

    # Check if user has enough petals (5000)
    user = await user_collection.find_one({"id": user_id})
    if not user or user.get("balance", 0) < 5000:
        return await callback_query.answer("🌸 *Ara ara~* You need 5,000 wisteria petals to refresh the spirits!", True)

    # Deduct 5000 petals
    await user_collection.update_one({"id": user_id}, {"$inc": {"balance": -5000}})

    # Fetch new characters
    rarity = state["rarity"]
    characters = await collection.find({"rarity": rarity}).to_list(None)
    random.shuffle(characters)
    state["characters"] = characters[:5]
    state["index"] = 0

    await callback_query.answer("🌸 *Fufufu~* New spirits have arrived! Enjoy~", True)
    await show_character(client, callback_query.message, user_id)


# ---------------- CLAIM ---------------- #

@app.on_callback_query(filters.regex(r"^claim_\d+$"))
async def claim_character(client, callback_query):
    _, index_str = safe_split(callback_query.data, "_", 2)

    user_id = callback_query.from_user.id
    state = user_shop_state.get(user_id)

    if not state:
        return await callback_query.answer("🌸 *Ara~* Your session has expired. Please start from /shop again!", True)

    char = state["characters"][int(index_str)]
    user = await user_collection.find_one({"id": user_id})

    if not user:
        return await callback_query.answer("🌸 *Oh my~* I don't recognize you! Please interact with the bot first.", True)

    price = RARITY_PRICE.get(char["rarity"], 1000)
    discount = await get_active_discount()
    discounted_price = int(price * (100 - discount) / 100)

    # Check if user can afford
    if user.get("balance", 0) < discounted_price:
        needed = discounted_price - user.get("balance", 0)
        return await callback_query.answer(
            f"🌸 *Ara ara~* You need {needed:,} more wisteria petals! "
            f"Try /daily, /guess, or /jackpot to earn more!",
            True
        )

    # Check if user already has this character
    existing_chars = user.get("characters", [])
    for existing in existing_chars:
        if existing.get("id") == char["id"]:
            return await callback_query.answer(
                "🌸 *Fufufu~* This spirit already resides in your garden! "
                "Would you like to gift it to a friend instead?",
                True
            )

    # Deduct petals and add character
    await user_collection.update_one(
        {"id": user_id},
        {
            "$inc": {"balance": -discounted_price},
            "$push": {"characters": {
                "_id": ObjectId(),
                "img_url": char["img_url"],
                "name": char["name"],
                "anime": char["anime"],
                "rarity": char["rarity"],
                "id": char["id"]
            }}
        }
    )

    # Get updated balance
    updated_user = await user_collection.find_one({"id": user_id})
    new_balance = updated_user.get("balance", 0) if updated_user else 0

    # Rarity-specific celebration message
    if price >= 100_000:
        celebration = "👑 **A PREMIUM SPIRIT JOINS YOUR GARDEN!** 👑\n*Truly extraordinary! The garden is blessed!*"
    elif price >= 50_000:
        celebration = "💎 **A LUXURIOUS SPIRIT HAS ARRIVED!** 💎\n*Such elegance! The garden shines brighter today!*"
    elif price >= 25_000:
        celebration = "🌟 **AN EXQUISITE SPIRIT JOINS YOU!** 🌟\n*What a beautiful addition to your collection!*"
    else:
        celebration = "🌸 **A LOVELY SPIRIT HAS ARRIVED!** 🌸\n*Welcome to the garden, dear butterfly!*"

    await callback_query.answer(
        f"🌸 *Wonderful!* {char['name']} has joined your garden! 🦋",
        True
    )
    
    # Update the character display to show "Claimed" status
    emoji = RARITY_EMOJIS.get(char["rarity"], "🌸")
    await callback_query.message.edit_caption(
        caption=(
            f"🌸 *Spirit Claimed!* 🦋\n\n"
            f"{celebration}\n\n"
            f"✨ **Name:** {char['name']}\n"
            f"⛩️ **Anime:** {char['anime']}\n"
            f"{emoji} **Rarity:** {char['rarity']}\n"
            f"🌸 **Paid:** {discounted_price:,} wisteria petals\n"
            f"💳 **New Balance:** {new_balance:,} petals\n\n"
            f"*Fufufu~* This beautiful spirit is now yours! Treat them well~\n"
            f"Use /harem to admire your growing collection! 🌸"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Bazaar", callback_data="back_to_shop")],
            [InlineKeyboardButton("🌸 View Your Garden", switch_inline_query_current_chat=f"collection.{user_id}")]
        ])
    )
