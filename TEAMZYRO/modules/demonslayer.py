

from TEAMZYRO import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from pyrogram import enums
import random
import time
import math
from datetime import datetime, timedelta
import asyncio
from bson import ObjectId
import html

# ==========================================
# DATABASE COLLECTIONS
# ==========================================

ds_users = db['ds_users']  # Player data
ds_achievements = db['ds_achievements']  # Achievement tracking
ds_season = db['ds_season']  # Season data
ds_rewards = db['ds_rewards']  # Milestone rewards
ds_battles = db['ds_battles']  # Active battle states

# ==========================================
# CONSTANTS
# ==========================================

HASHIRAS = {
    "Shinobu": {
        "emoji": "🦋",
        "passive": "Poison Master",
        "description": "Increases critical damage by 25%",
        "bonus": {"critical_damage": 1.25},
        "difficulty": "Medium"
    },
    "Giyu": {
        "emoji": "🌊",
        "passive": "Water Breathing",
        "description": "Increases defense by 20%",
        "bonus": {"defense_multiplier": 1.20},
        "difficulty": "Easy"
    },
    "Rengoku": {
        "emoji": "🔥",
        "passive": "Flame Breathing",
        "description": "Increases attack by 25%",
        "bonus": {"attack_multiplier": 1.25},
        "difficulty": "Easy"
    },
    "Muichiro": {
        "emoji": "🌫️",
        "passive": "Mist Breathing",
        "description": "Increases dodge chance by 15%",
        "bonus": {"dodge_chance": 0.15},
        "difficulty": "Medium"
    },
    "Mitsuri": {
        "emoji": "💕",
        "passive": "Love Breathing",
        "description": "Increases HP regeneration by 10% each turn",
        "bonus": {"hp_regen": 0.10},
        "difficulty": "Easy"
    },
    "Sanemi": {
        "emoji": "🌪️",
        "passive": "Wind Breathing",
        "description": "Increases critical chance by 15%",
        "bonus": {"critical_chance": 0.15},
        "difficulty": "Hard"
    },
    "Obanai": {
        "emoji": "🐍",
        "passive": "Serpent Breathing",
        "description": "Increases attack speed (extra turn chance)",
        "bonus": {"extra_turn_chance": 0.10},
        "difficulty": "Hard"
    },
    "Gyomei": {
        "emoji": "⛰️",
        "passive": "Stone Breathing",
        "description": "Increases HP by 30%",
        "bonus": {"hp_multiplier": 1.30},
        "difficulty": "Hard"
    },
    "Tengen": {
        "emoji": "💎",
        "passive": "Sound Breathing",
        "description": "Increases all stats by 10%",
        "bonus": {"all_stat_multiplier": 1.10},
        "difficulty": "Medium"
    }
}

RANKS = [
    {"name": "Mizunoto", "level": 1},
    {"name": "Mizunoe", "level": 5},
    {"name": "Kanoto", "level": 10},
    {"name": "Kanoe", "level": 15},
    {"name": "Tsuchinoto", "level": 20},
    {"name": "Tsuchinoe", "level": 25},
    {"name": "Hinoto", "level": 30},
    {"name": "Hinoe", "level": 35},
    {"name": "Kinoto", "level": 40},
    {"name": "Kinoe", "level": 45},
    {"name": "Hashira", "level": 50}
]

DEMONS = {
    "Weak Demon": {
        "hp_base": 50,
        "attack_base": 10,
        "defense_base": 5,
        "xp_reward": 50,
        "trophy_reward": 5,
        "coin_reward": 100,
        "emoji": "👹"
    },
    "Strong Demon": {
        "hp_base": 100,
        "attack_base": 20,
        "defense_base": 10,
        "xp_reward": 100,
        "trophy_reward": 10,
        "coin_reward": 200,
        "emoji": "👹"
    },
    "Lower Moon": {
        "hp_base": 200,
        "attack_base": 35,
        "defense_base": 15,
        "xp_reward": 200,
        "trophy_reward": 20,
        "coin_reward": 400,
        "emoji": "🌙"
    },
    "Upper Moon": {
        "hp_base": 350,
        "attack_base": 55,
        "defense_base": 25,
        "xp_reward": 400,
        "trophy_reward": 40,
        "coin_reward": 800,
        "emoji": "🌕"
    },
    "Muzan": {
        "hp_base": 600,
        "attack_base": 80,
        "defense_base": 40,
        "xp_reward": 800,
        "trophy_reward": 80,
        "coin_reward": 1500,
        "emoji": "💀"
    }
}

ACHIEVEMENTS = [
    {"id": "first_win", "name": "First Victory", "description": "Win your first battle", "requirement": 1},
    {"id": "100_wins", "name": "Demon Slayer", "description": "Win 100 battles", "requirement": 100},
    {"id": "500_wins", "name": "Hashira Candidate", "description": "Win 500 battles", "requirement": 500},
    {"id": "1000_wins", "name": "Legendary Slayer", "description": "Win 1000 battles", "requirement": 1000},
    {"id": "level_50", "name": "Master Slayer", "description": "Reach Level 50", "requirement": 50},
    {"id": "level_100", "name": "Ultimate Slayer", "description": "Reach Level 100", "requirement": 100}
]

BATTLE_MESSAGES = [
    "You strike with precision!",
    "A devastating blow!",
    "Your blade cuts deep!",
    "The enemy staggers back!",
    "You land a clean hit!",
    "Your attack connects!",
    "The demon roars in pain!",
    "You unleash a powerful strike!",
    "Your technique is flawless!",
    "The demon's guard breaks!"
]

ENEMY_MESSAGES = [
    "The demon counterattacks!",
    "A clawed swipe comes at you!",
    "The demon lunges forward!",
    "A vicious attack from the shadows!",
    "The demon unleashes its fury!",
    "You're caught off guard!",
    "A powerful blow sends you back!",
    "The demon's attack is relentless!",
    "You barely dodge the strike!",
    "The demon's power overwhelms you!"
]

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_rank(level):
    """Get rank name based on level"""
    rank = RANKS[0]["name"]
    for r in RANKS:
        if level >= r["level"]:
            rank = r["name"]
    return rank

def calculate_player_stats(player):
    """Calculate player stats based on level and Hashira"""
    level = player.get('level', 1)
    hashira = player.get('hashira', 'Shinobu')
    bonus = HASHIRAS.get(hashira, {}).get('bonus', {})
    
    base_hp = 100 + (level * 20)
    base_attack = 15 + (level * 3)
    base_defense = 10 + (level * 2)
    base_critical = 5 + (level * 0.5)
    
    # Apply hashira bonuses
    hp = int(base_hp * bonus.get('hp_multiplier', 1.0) * bonus.get('all_stat_multiplier', 1.0))
    attack = int(base_attack * bonus.get('attack_multiplier', 1.0) * bonus.get('all_stat_multiplier', 1.0))
    defense = int(base_defense * bonus.get('defense_multiplier', 1.0) * bonus.get('all_stat_multiplier', 1.0))
    critical = base_critical + bonus.get('critical_chance', 0) * 100
    
    return {
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'critical': min(critical, 50),  # Cap at 50%
        'dodge': 5 + bonus.get('dodge_chance', 0) * 100
    }

def generate_demon(player_level):
    """Generate a demon based on player level"""
    level = player_level
    
    # Determine demon tier based on level
    if level < 5:
        tier = random.choices(
            ['Weak Demon', 'Strong Demon'],
            weights=[70, 30]
        )[0]
    elif level < 15:
        tier = random.choices(
            ['Weak Demon', 'Strong Demon', 'Lower Moon'],
            weights=[20, 50, 30]
        )[0]
    elif level < 30:
        tier = random.choices(
            ['Strong Demon', 'Lower Moon', 'Upper Moon'],
            weights=[20, 40, 40]
        )[0]
    elif level < 50:
        tier = random.choices(
            ['Lower Moon', 'Upper Moon', 'Muzan'],
            weights=[20, 50, 30]
        )[0]
    else:
        tier = random.choices(
            ['Upper Moon', 'Muzan'],
            weights=[40, 60]
        )[0]
    
    demon_data = DEMONS[tier]
    level_multiplier = 1 + (level / 100)
    
    return {
        'name': tier,
        'emoji': demon_data['emoji'],
        'hp': int(demon_data['hp_base'] * level_multiplier),
        'max_hp': int(demon_data['hp_base'] * level_multiplier),
        'attack': int(demon_data['attack_base'] * level_multiplier),
        'defense': int(demon_data['defense_base'] * level_multiplier),
        'xp_reward': int(demon_data['xp_reward'] * level_multiplier),
        'trophy_reward': int(demon_data['trophy_reward'] * level_multiplier),
        'coin_reward': int(demon_data['coin_reward'] * level_multiplier),
        'critical': 5 + (level * 0.2)
    }

def calculate_xp_needed(level):
    """Calculate XP needed for next level"""
    return 100 + (level * 25)

def create_progress_bar(current, total, length=10):
    """Create a progress bar"""
    if total <= 0:
        return "█" * length
    filled = int((current / total) * length)
    return "█" * filled + "░" * (length - filled)

# ==========================================
# HASHIRA SELECTION
# ==========================================

@app.on_message(filters.command("demonslayer"))
async def demonslayer_start(client: Client, message: Message):
    """Start or continue Demon Slayer RPG"""
    user_id = message.from_user.id
    
    # Check if user has a character
    player = await ds_users.find_one({"user_id": user_id})
    
    if not player:
        # First time - show hashira selection
        await show_hashira_selection(client, message, user_id)
        return
    
    # Show main menu
    await show_main_menu(client, message, user_id)

async def show_hashira_selection(client, message, user_id):
    """Display hashira selection menu"""
    keyboard = []
    row = []
    for i, (name, data) in enumerate(HASHIRAS.items()):
        row.append(InlineKeyboardButton(
            f"{data['emoji']} {name}",
            callback_data=f"ds_hashira_preview_{name}"
        ))
        if len(row) == 3:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    caption = (
        "🌸 **DEMON SLAYER CORPS** 🌸\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "*Ara ara~ A new slayer has arrived!*\n\n"
        "Choose your Hashira mentor wisely.\n"
        "Each Hashira grants a unique passive ability.\n"
        "*This choice is permanent for the season!*\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "🦋 **Select your Hashira:**"
    )
    
    await message.reply_photo(
        photo="https://files.catbox.moe/demonslayer_banner.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.HTML
    )

@app.on_callback_query(filters.regex(r"^ds_hashira_preview_(.+)$"))
async def hashira_preview_callback(client, callback_query):
    """Show hashira preview"""
    hashira_name = callback_query.matches[0].group(1)
    hashira_data = HASHIRAS[hashira_name]
    
    caption = (
        f"🌸 **{hashira_data['emoji']} {hashira_name}**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"**Passive:** {hashira_data['passive']}\n"
        f"**Description:** {hashira_data['description']}\n"
        f"**Difficulty:** {hashira_data['difficulty']}\n\n"
        "*Choose this Hashira to begin your journey!*"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Choose", callback_data=f"ds_hashira_choose_{hashira_name}"),
            InlineKeyboardButton("🔙 Back", callback_data="ds_hashira_back")
        ]
    ]
    
    await callback_query.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.HTML
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_hashira_choose_(.+)$"))
async def hashira_choose_callback(client, callback_query):
    """Confirm hashira selection"""
    hashira_name = callback_query.matches[0].group(1)
    user_id = callback_query.from_user.id
    
    # Check if already has hashira
    existing = await ds_users.find_one({"user_id": user_id})
    if existing:
        await callback_query.answer("You already have a Hashira!", show_alert=True)
        return
    
    # Create player
    player_data = {
        "user_id": user_id,
        "hashira": hashira_name,
        "level": 1,
        "xp": 0,
        "trophies": 0,
        "season_trophies": 0,
        "wins": 0,
        "losses": 0,
        "demons_defeated": 0,
        "pvp_wins": 0,
        "total_hunts": 0,
        "created_at": datetime.utcnow(),
        "last_hunt": None,
        "last_daily": None,
        "missions": [],
        "achievements": []
    }
    
    await ds_users.insert_one(player_data)
    
    caption = (
        f"🌸 **Welcome to the Demon Slayer Corps!**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🦋 You have chosen **{hashira_name}** as your Hashira!\n\n"
        f"**Passive:** {HASHIRAS[hashira_name]['passive']}\n"
        f"**Effect:** {HASHIRAS[hashira_name]['description']}\n\n"
        "⚔️ Your journey begins now!\n"
        "Use /hunt to start your first mission."
    )
    
    keyboard = [
        [InlineKeyboardButton("⚔️ Start Hunting", callback_data="ds_hunt_start")]
    ]
    
    await callback_query.message.edit_caption(
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.HTML
    )
    await callback_query.answer("Hashira chosen successfully!")

@app.on_callback_query(filters.regex(r"^ds_hashira_back$"))
async def hashira_back_callback(client, callback_query):
    """Go back to hashira selection"""
    user_id = callback_query.from_user.id
    await show_hashira_selection(client, callback_query.message, user_id)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_hunt_start$"))
async def hunt_start_from_selection(client, callback_query):
    """Start hunt from selection screen"""
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    await hunt_command(client, callback_query.message)
    await callback_query.answer()

# ==========================================
# MAIN MENU
# ==========================================

async def show_main_menu(client, message, user_id):
    """Show main RPG menu"""
    player = await ds_users.find_one({"user_id": user_id})
    if not player:
        await demonslayer_start(client, message)
        return
    
    stats = calculate_player_stats(player)
    rank = get_rank(player['level'])
    
    caption = (
        f"🌸 **DEMON SLAYER CORPS** 🌸\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🦋 **Hashira:** {player['hashira']}\n"
        f"⭐ **Rank:** {rank}\n"
        f"📊 **Level:** {player['level']}\n"
        f"🏆 **Trophies:** {player['trophies']}\n"
        f"📈 **Season Trophies:** {player.get('season_trophies', 0)}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "*What would you like to do, slayer?*"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("⚔️ Hunt", callback_data="ds_hunt"),
            InlineKeyboardButton("👤 Profile", callback_data="ds_profile")
        ],
        [
            InlineKeyboardButton("📦 Inventory", callback_data="ds_inventory"),
            InlineKeyboardButton("📋 Missions", callback_data="ds_missions")
        ],
        [
            InlineKeyboardButton("🏆 Achievements", callback_data="ds_achievements"),
            InlineKeyboardButton("📊 Leaderboard", callback_data="ds_leaderboard")
        ],
        [
            InlineKeyboardButton("☀️ Daily Hunt", callback_data="ds_daily"),
            InlineKeyboardButton("⚔️ Challenge", callback_data="ds_challenge_menu")
        ]
    ]
    
    await message.reply_photo(
        photo="https://files.catbox.moe/demonslayer_main.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# HUNT COMMAND
# ==========================================

@app.on_message(filters.command("hunt"))
async def hunt_command(client: Client, message: Message):
    """Start a demon hunt"""
    user_id = message.from_user.id
    
    # Check if player exists
    player = await ds_users.find_one({"user_id": user_id})
    if not player:
        await message.reply_text(
            "🌸 *Ara ara~* You haven't joined the Demon Slayer Corps yet!\n"
            "Use /demonslayer to begin your journey."
        )
        return
    
    # Check cooldown
    last_hunt = player.get('last_hunt')
    if last_hunt:
        elapsed = time.time() - last_hunt
        if elapsed < 90:
            remaining = int(90 - elapsed)
            await message.reply_text(
                f"⏳ *Rest, slayer.* You need to wait {remaining} seconds before your next hunt."
            )
            return
    
    # Check for active battle
    active_battle = await ds_battles.find_one({"user_id": user_id})
    if active_battle:
        await message.reply_text(
            "⚔️ *You're already in a battle!* Complete it first."
        )
        return
    
    # Generate demon
    demon = generate_demon(player['level'])
    stats = calculate_player_stats(player)
    
    # Store battle state
    battle_data = {
        "user_id": user_id,
        "type": "hunt",
        "demon": demon,
        "player_hp": stats['hp'],
        "player_max_hp": stats['hp'],
        "demon_hp": demon['hp'],
        "demon_max_hp": demon['max_hp'],
        "turn": 0,
        "started_at": time.time(),
        "status": "preview"  # preview, fighting, ended
    }
    await ds_battles.insert_one(battle_data)
    
    # Show battle preview
    await show_battle_preview(client, message, user_id)

async def show_battle_preview(client, message, user_id):
    """Show battle preview with fight/flee options"""
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle:
        return
    
    demon = battle['demon']
    player = await ds_users.find_one({"user_id": user_id})
    
    # Create progress bars
    hp_bar = create_progress_bar(demon['hp'], demon['max_hp'])
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚔️ **DEMON ENCOUNTER**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{demon['emoji']} **Enemy:** {demon['name']}\n\n"
        "❤️ **HP**\n"
        f"{hp_bar} {demon['hp']}/{demon['max_hp']}\n\n"
        f"⚔️ **Attack:** {demon['attack']}\n"
        f"🛡️ **Defense:** {demon['defense']}\n"
        f"🎯 **Critical:** {demon['critical']:.1f}%\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏆 **Reward**\n\n"
        f"+{demon['trophy_reward']} Trophies\n"
        f"+{demon['xp_reward']} XP\n"
        f"+{demon['coin_reward']} Petals\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "*What will you do?*"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("⚔️ Fight", callback_data=f"ds_battle_fight_{user_id}"),
            InlineKeyboardButton("🏃 Flee", callback_data=f"ds_battle_flee_{user_id}")
        ]
    ]
    
    await message.reply_photo(
        photo="https://files.catbox.moe/demon_encounter.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# BATTLE SYSTEM
# ==========================================

@app.on_callback_query(filters.regex(r"^ds_battle_flee_(\d+)$"))
async def battle_flee_callback(client, callback_query):
    """Handle flee action"""
    user_id = int(callback_query.matches[0].group(1))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("This isn't your battle!", show_alert=True)
        return
    
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle or battle['status'] == 'ended':
        await callback_query.answer("Battle already ended!", show_alert=True)
        return
    
    # Delete battle
    await ds_battles.delete_one({"user_id": user_id})
    
    a
