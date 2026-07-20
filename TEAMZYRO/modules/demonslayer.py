# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

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

ds_users = db['ds_users']
ds_achievements = db['ds_achievements']
ds_season = db['ds_season']
ds_rewards = db['ds_rewards']
ds_battles = db['ds_battles']

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
    
    hp = int(base_hp * bonus.get('hp_multiplier', 1.0) * bonus.get('all_stat_multiplier', 1.0))
    attack = int(base_attack * bonus.get('attack_multiplier', 1.0) * bonus.get('all_stat_multiplier', 1.0))
    defense = int(base_defense * bonus.get('defense_multiplier', 1.0) * bonus.get('all_stat_multiplier', 1.0))
    critical = base_critical + bonus.get('critical_chance', 0) * 100
    
    return {
        'hp': hp,
        'attack': attack,
        'defense': defense,
        'critical': min(critical, 50),
        'dodge': 5 + bonus.get('dodge_chance', 0) * 100
    }

def generate_demon(player_level):
    """Generate a demon based on player level"""
    level = player_level
    
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
    
    player = await ds_users.find_one({"user_id": user_id})
    
    if not player:
        await show_hashira_selection(client, message, user_id)
        return
    
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
        photo="https://files.catbox.moe/sf2wm1.png",
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
    
    existing = await ds_users.find_one({"user_id": user_id})
    if existing:
        await callback_query.answer("You already have a Hashira!", show_alert=True)
        return
    
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
    
    player = await ds_users.find_one({"user_id": user_id})
    if not player:
        await message.reply_text(
            "🌸 *Ara ara~* You haven't joined the Demon Slayer Corps yet!\n"
            "Use /demonslayer to begin your journey."
        )
        return
    
    last_hunt = player.get('last_hunt')
    if last_hunt:
        elapsed = time.time() - last_hunt
        if elapsed < 90:
            remaining = int(90 - elapsed)
            await message.reply_text(
                f"⏳ *Rest, slayer.* You need to wait {remaining} seconds before your next hunt."
            )
            return
    
    active_battle = await ds_battles.find_one({"user_id": user_id})
    if active_battle:
        await message.reply_text(
            "⚔️ *You're already in a battle!* Complete it first."
        )
        return
    
    demon = generate_demon(player['level'])
    stats = calculate_player_stats(player)
    
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
        "status": "preview"
    }
    await ds_battles.insert_one(battle_data)
    
    await show_battle_preview(client, message, user_id)

async def show_battle_preview(client, message, user_id):
    """Show battle preview with fight/flee options"""
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle:
        return
    
    demon = battle['demon']
    player = await ds_users.find_one({"user_id": user_id})
    
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
    
    await ds_battles.delete_one({"user_id": user_id})
    
    await callback_query.message.edit_caption(
        caption="🏃 **You successfully escaped!**\n\n*Live to fight another day, slayer.*",
        reply_markup=None,
        parse_mode=enums.ParseMode.HTML
    )
    await callback_query.answer("You fled the battle!")

@app.on_callback_query(filters.regex(r"^ds_battle_fight_(\d+)$"))
async def battle_fight_callback(client, callback_query):
    """Start the battle"""
    user_id = int(callback_query.matches[0].group(1))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("This isn't your battle!", show_alert=True)
        return
    
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle or battle['status'] == 'ended':
        await callback_query.answer("Battle already ended!", show_alert=True)
        return
    
    await ds_battles.update_one(
        {"user_id": user_id},
        {"$set": {"status": "fighting"}}
    )
    
    await process_battle_turn(client, callback_query.message, user_id)
    await callback_query.answer()

async def process_battle_turn(client, message, user_id):
    """Process one turn of battle"""
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle or battle['status'] == 'ended':
        return
    
    player = await ds_users.find_one({"user_id": user_id})
    stats = calculate_player_stats(player)
    demon = battle['demon']
    hashira = HASHIRAS.get(player['hashira'], {})
    bonus = hashira.get('bonus', {})
    
    turn_message = ""
    player_attack = stats['attack']
    demon_defense = demon['defense']
    
    critical_chance = stats['critical'] / 100
    is_critical = random.random() < critical_chance
    
    miss_chance = 0.10
    is_miss = random.random() < miss_chance
    
    dodge_chance = stats['dodge'] / 100
    is_dodged = random.random() < dodge_chance
    
    if is_dodged:
        damage = 0
        turn_message = f"💨 *The demon dodged your attack!*"
    elif is_miss:
        damage = 0
        turn_message = f"💨 *Your attack missed!*"
    else:
        damage = max(1, player_attack - demon_defense // 2)
        if is_critical:
            damage = int(damage * 1.5 * bonus.get('critical_damage', 1.0))
            turn_message = f"⚡ **CRITICAL HIT!** {damage} damage!"
        else:
            turn_message = random.choice(BATTLE_MESSAGES) + f" (-{damage} HP)"
    
    battle['demon_hp'] = max(0, battle['demon_hp'] - damage)
    await ds_battles.update_one(
        {"user_id": user_id},
        {"$set": {"demon_hp": battle['demon_hp']}}
    )
    
    if battle['demon_hp'] <= 0:
        await end_battle(client, message, user_id, True)
        return
    
    demon_attack = demon['attack']
    player_defense = stats['defense']
    
    demon_miss = random.random() < 0.10
    
    if demon_miss:
        demon_damage = 0
        turn_message += "\n\n💨 *The demon's attack missed!*"
    else:
        demon_damage = max(1, demon_attack - player_defense // 2)
        if random.random() < bonus.get('dodge_chance', 0):
            demon_damage = int(demon_damage * 0.5)
            turn_message += f"\n\n🦋 *Your Hashira's blessing reduced the damage!*"
        turn_message += f"\n\n{random.choice(ENEMY_MESSAGES)} (-{demon_damage} HP)"
    
    battle['player_hp'] = max(0, battle['player_hp'] - demon_damage)
    await ds_battles.update_one(
        {"user_id": user_id},
        {"$set": {"player_hp": battle['player_hp']}}
    )
    
    if battle['player_hp'] <= 0:
        await end_battle(client, message, user_id, False)
        return
    
    await ds_battles.update_one(
        {"user_id": user_id},
        {"$inc": {"turn": 1}}
    )
    
    await update_battle_display(client, message, user_id, turn_message)

async def update_battle_display(client, message, user_id, turn_message):
    """Update battle message with current state"""
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle:
        return
    
    demon = battle['demon']
    player = await ds_users.find_one({"user_id": user_id})
    stats = calculate_player_stats(player)
    
    demon_hp_bar = create_progress_bar(battle['demon_hp'], battle['demon_max_hp'])
    player_hp_bar = create_progress_bar(battle['player_hp'], stats['hp'])
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚔️ **BATTLE IN PROGRESS**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**Turn {battle['turn'] + 1}**\n\n"
        f"{demon['emoji']} **{demon['name']}**\n"
        f"❤️ `{demon_hp_bar}` {battle['demon_hp']}/{battle['demon_max_hp']}\n\n"
        f"👤 **You**\n"
        f"❤️ `{player_hp_bar}` {battle['player_hp']}/{stats['hp']}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{turn_message}\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("⚔️ Attack", callback_data=f"ds_battle_attack_{user_id}"),
            InlineKeyboardButton("🛡️ Defend", callback_data=f"ds_battle_defend_{user_id}")
        ]
    ]
    
    try:
        await message.edit_caption(
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=enums.ParseMode.HTML
        )
    except Exception:
        pass

@app.on_callback_query(filters.regex(r"^ds_battle_attack_(\d+)$"))
async def battle_attack_callback(client, callback_query):
    """Handle attack action"""
    user_id = int(callback_query.matches[0].group(1))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("This isn't your battle!", show_alert=True)
        return
    
    await process_battle_turn(client, callback_query.message, user_id)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_battle_defend_(\d+)$"))
async def battle_defend_callback(client, callback_query):
    """Handle defend action"""
    user_id = int(callback_query.matches[0].group(1))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("This isn't your battle!", show_alert=True)
        return
    
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle:
        return
    
    heal_amount = int(battle['player_max_hp'] * 0.10)
    battle['player_hp'] = min(battle['player_max_hp'], battle['player_hp'] + heal_amount)
    await ds_battles.update_one(
        {"user_id": user_id},
        {"$set": {"player_hp": battle['player_hp']}}
    )
    
    turn_message = f"🛡️ *You take a defensive stance and heal {heal_amount} HP!*"
    await update_battle_display(client, callback_query.message, user_id, turn_message)
    await callback_query.answer("You defend!")

async def end_battle(client, message, user_id, victory):
    """End the battle and award rewards"""
    battle = await ds_battles.find_one({"user_id": user_id})
    if not battle:
        return
    
    player = await ds_users.find_one({"user_id": user_id})
    demon = battle['demon']
    
    await ds_battles.update_one(
        {"user_id": user_id},
        {"$set": {"status": "ended"}}
    )
    
    if victory:
        xp_gain = demon['xp_reward']
        trophy_gain = demon['trophy_reward']
        coin_gain = demon['coin_reward']
        
        old_level = player['level']
        xp_needed = calculate_xp_needed(old_level)
        
        updates = {
            "$inc": {
                "xp": xp_gain,
                "trophies": trophy_gain,
                "season_trophies": trophy_gain,
                "coins": coin_gain,
                "wins": 1,
                "demons_defeated": 1,
                "total_hunts": 1
            },
            "$set": {"last_hunt": time.time()}
        }
        
        new_xp = player.get('xp', 0) + xp_gain
        new_level = old_level
        while new_xp >= calculate_xp_needed(new_level):
            new_xp -= calculate_xp_needed(new_level)
            new_level += 1
        
        if new_level > old_level:
            updates["$set"]["level"] = new_level
            updates["$set"]["xp"] = new_xp
            level_up = True
        else:
            updates["$set"]["xp"] = new_xp
            level_up = False
        
        await ds_users.update_one({"user_id": user_id}, updates)
        
        await check_achievements(client, user_id)
        
        updated_player = await ds_users.find_one({"user_id": user_id})
        stats = calculate_player_stats(updated_player)
        
        xp_bar = create_progress_bar(updated_player['xp'], calculate_xp_needed(updated_player['level']))
        
        caption = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "🏆 **VICTORY!**\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👹 **{demon['name']} defeated!**\n\n"
            f"✨ **Rewards Earned:**\n"
            f"+{xp_gain} XP\n"
            f"+{trophy_gain} Trophies\n"
            f"+{coin_gain} Petals\n"
        )
        
        if level_up:
            caption += (
                f"\n🎉 **LEVEL UP!**\n"
                f"⭐ Level {old_level} → **{new_level}**\n"
            )
        
        caption += (
            f"\n📊 **XP Progress**\n"
            f"`{xp_bar}` {updated_player['xp']}/{calculate_xp_needed(updated_player['level'])} XP"
        )
        
        await ds_battles.delete_one({"user_id": user_id})
        
        keyboard = [
            [InlineKeyboardButton("⚔️ Hunt Again", callback_data=f"ds_hunt_again_{user_id}")],
            [InlineKeyboardButton("📊 View Profile", callback_data=f"ds_profile_view_{user_id}")]
        ]
        
        await message.edit_caption(
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=enums.ParseMode.HTML
        )
        
    else:
        trophy_loss = max(1, demon['trophy_reward'] // 2)
        await ds_users.update_one(
            {"user_id": user_id},
            {
                "$inc": {"losses": 1, "trophies": -trophy_loss},
                "$set": {"last_hunt": time.time()}
            }
        )
        
        await ds_battles.delete_one({"user_id": user_id})
        
        caption = (
            "━━━━━━━━━━━━━━━━━━━━━━\n"
            "💀 **DEFEAT**\n"
            "━━━━━━━━━━━━━━━━━━━━━━\n\n"
            f"👹 **{demon['name']}** was too strong...\n\n"
            f"💔 **Lost:** {trophy_loss} Trophies\n\n"
            "*Train harder and try again, slayer!*"
        )
        
        keyboard = [
            [InlineKeyboardButton("⚔️ Hunt Again", callback_data=f"ds_hunt_again_{user_id}")]
        ]
        
        await message.edit_caption(
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=enums.ParseMode.HTML
        )

@app.on_callback_query(filters.regex(r"^ds_hunt_again_(\d+)$"))
async def hunt_again_callback(client, callback_query):
    """Start a new hunt"""
    user_id = int(callback_query.matches[0].group(1))
    
    if callback_query.from_user.id != user_id:
        await callback_query.answer("This isn't your hunt!", show_alert=True)
        return
    
    await callback_query.message.delete()
    await hunt_command(client, callback_query.message)
    await callback_query.answer()

# ==========================================
# PROFILE COMMAND
# ==========================================

@app.on_message(filters.command("dprofile"))
async def profile_command(client: Client, message: Message):
    """Display player profile"""
    user_id = message.from_user.id
    target_user = None
    
    if message.reply_to_message:
        target_user = message.reply_to_message.from_user
    else:
        target_user = message.from_user
    
    await show_profile(client, message, target_user.id)

async def show_profile(client, message, user_id):
    """Show player profile"""
    player = await ds_users.find_one({"user_id": user_id})
    if not player:
        await message.reply_text(
            "🌸 *Ara ara~* This slayer hasn't joined the Demon Slayer Corps yet!"
        )
        return
    
    stats = calculate_player_stats(player)
    rank = get_rank(player['level'])
    hashira = HASHIRAS[player['hashira']]
    
    xp_needed = calculate_xp_needed(player['level'])
    xp_bar = create_progress_bar(player['xp'], xp_needed)
    
    season_rank = await get_season_rank(user_id)
    
    try:
        user = await client.get_users(user_id)
        user_name = user.first_name
    except:
        user_name = f"User {user_id}"
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🌸 **{user_name}'S PROFILE**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{hashira['emoji']} **Hashira:** {player['hashira']}\n"
        f"⭐ **Rank:** {rank}\n"
        f"📊 **Level:** {player['level']}\n"
        f"📈 **XP:** `{xp_bar}` {player['xp']}/{xp_needed}\n\n"
        f"❤️ **HP:** {stats['hp']}\n"
        f"⚔️ **Attack:** {stats['attack']}\n"
        f"🛡️ **Defense:** {stats['defense']}\n"
        f"🎯 **Critical:** {stats['critical']:.1f}%\n"
        f"💨 **Dodge:** {stats['dodge']:.1f}%\n\n"
        f"🏆 **Trophies:** {player['trophies']}\n"
        f"📈 **Season Rank:** #{season_rank}\n"
        f"🏅 **Season Trophies:** {player.get('season_trophies', 0)}\n\n"
        f"⚔️ **Wins:** {player.get('wins', 0)}\n"
        f"💀 **Losses:** {player.get('losses', 0)}\n"
        f"👹 **Demons Defeated:** {player.get('demons_defeated', 0)}\n"
        f"⚔️ **PvP Wins:** {player.get('pvp_wins', 0)}\n"
        "━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    keyboard = [
        [InlineKeyboardButton("⚔️ Hunt Now", callback_data=f"ds_hunt_again_{user_id}")]
    ]
    
    await message.reply_photo(
        photo="https://files.catbox.moe/profile_banner.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# INVENTORY COMMAND
# ==========================================

@app.on_message(filters.command("inv"))
async def inventory_command(client: Client, message: Message):
    """Display player inventory"""
    user_id = message.from_user.id
    player = await ds_users.find_one({"user_id": user_id})
    
    if not player:
        await message.reply_text(
            "🌸 *Ara ara~* You haven't joined the Demon Slayer Corps yet!\n"
            "Use /demonslayer to begin your journey."
        )
        return
    
    rank = get_rank(player['level'])
    hashira = HASHIRAS[player['hashira']]
    
    reward_progress = await get_reward_progress(user_id)
    next_reward = await get_next_milestone(player['trophies'])
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📦 **INVENTORY**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏆 **Trophies:** {player['trophies']}\n"
        f"📊 **XP:** {player['xp']}\n"
        f"⭐ **Level:** {player['level']}\n"
        f"🎖️ **Rank:** {rank}\n"
        f"{hashira['emoji']} **Hashira:** {player['hashira']}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 **Reward Progress**\n"
        f"Current: {player['trophies']} Trophies\n"
    )
    
    if next_reward:
        caption += (
            f"Next: {next_reward} Trophies\n"
            f"`{create_progress_bar(player['trophies'], next_reward)}`"
        )
    
    caption += "\n━━━━━━━━━━━━━━━━━━━━━━"
    
    await message.reply_text(
        caption,
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# CHALLENGE COMMAND
# ==========================================

@app.on_message(filters.command("challenge"))
async def challenge_command(client: Client, message: Message):
    """Challenge another player to PvP"""
    if not message.reply_to_message:
        await message.reply_text(
            "⚔️ *Reply to a user's message to challenge them!*"
        )
        return
    
    challenger_id = message.from_user.id
    opponent_id = message.reply_to_message.from_user.id
    
    if challenger_id == opponent_id:
        await message.reply_text("You can't challenge yourself!")
        return
    
    challenger = await ds_users.find_one({"user_id": challenger_id})
    opponent = await ds_users.find_one({"user_id": opponent_id})
    
    if not challenger:
        await message.reply_text("You need to join the Demon Slayer Corps first!")
        return
    
    if not opponent:
        await message.reply_text("Your opponent hasn't joined the Demon Slayer Corps!")
        return
    
    challenge_data = {
        "challenger_id": challenger_id,
        "opponent_id": opponent_id,
        "status": "pending",
        "created_at": time.time()
    }
    await ds_battles.insert_one(challenge_data)
    
    challenger_name = message.from_user.first_name
    opponent_name = message.reply_to_message.from_user.first_name
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "⚔️ **PvP CHALLENGE**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"👤 {challenger_name}\n"
        "   ⚔️ VS\n"
        f"👤 {opponent_name}\n\n"
        f"🏆 **Trophy Bet:** 10 Trophies\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{opponent_name}, do you accept?"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Accept", callback_data=f"ds_challenge_accept_{challenger_id}_{opponent_id}"),
            InlineKeyboardButton("❌ Decline", callback_data=f"ds_challenge_decline_{challenger_id}_{opponent_id}")
        ]
    ]
    
    await message.reply_photo(
        photo="https://files.catbox.moe/pvp_challenge.jpg",
        caption=caption,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=enums.ParseMode.HTML
    )

@app.on_callback_query(filters.regex(r"^ds_challenge_accept_(\d+)_(\d+)$"))
async def challenge_accept_callback(client, callback_query):
    """Accept challenge and start PvP"""
    challenger_id = int(callback_query.matches[0].group(1))
    opponent_id = int(callback_query.matches[0].group(2))
    
    if callback_query.from_user.id != opponent_id:
        await callback_query.answer("This isn't your challenge!", show_alert=True)
        return
    
    await start_pvp_battle(client, callback_query.message, challenger_id, opponent_id)
    await callback_query.answer("Challenge accepted!")

@app.on_callback_query(filters.regex(r"^ds_challenge_decline_(\d+)_(\d+)$"))
async def challenge_decline_callback(client, callback_query):
    """Decline challenge"""
    opponent_id = int(callback_query.matches[0].group(2))
    
    if callback_query.from_user.id != opponent_id:
        await callback_query.answer("This isn't your challenge!", show_alert=True)
        return
    
    await callback_query.message.edit_caption(
        caption="❌ **Challenge declined.**\n\n*The battle was called off.*",
        reply_markup=None,
        parse_mode=enums.ParseMode.HTML
    )
    await callback_query.answer("You declined the challenge!")

async def start_pvp_battle(client, message, challenger_id, opponent_id):
    """Start PvP battle"""
    challenger = await ds_users.find_one({"user_id": challenger_id})
    opponent = await ds_users.find_one({"user_id": opponent_id})
    
    challenger_stats = calculate_player_stats(challenger)
    opponent_stats = calculate_player_stats(opponent)
    
    battle_data = {
        "user_id": challenger_id,
        "type": "pvp",
        "opponent_id": opponent_id,
        "challenger_hp": challenger_stats['hp'],
        "challenger_max_hp": challenger_stats['hp'],
        "opponent_hp": opponent_stats['hp'],
        "opponent_max_hp": opponent_stats['hp'],
        "turn": 0,
        "status": "pvp_fighting",
        "started_at": time.time()
    }
    await ds_battles.insert_one(battle_data)
    
    await update_pvp_display(client, message, challenger_id, opponent_id, "⚔️ The battle begins!")

# ==========================================
# LEADERBOARD
# ==========================================

@app.on_message(filters.command("dtop"))
async def leaderboard_command(client: Client, message: Message):
    """Display monthly leaderboard"""
    cursor = ds_users.find().sort("season_trophies", -1).limit(10)
    top_players = await cursor.to_list(length=10)
    
    if not top_players:
        await message.reply_text("No players found!")
        return
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📊 **MONTHLY LEADERBOARD**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    
    medals = ["🥇", "🥈", "🥉"]
    for i, player in enumerate(top_players):
        medal = medals[i] if i < 3 else f"#{i+1}"
        try:
            user = await client.get_users(player['user_id'])
            name = user.first_name[:20]
        except:
            name = f"User {player['user_id']}"
        
        rank = get_rank(player['level'])
        caption += (
            f"{medal} **{name}**\n"
            f"   Level {player['level']} | {rank}\n"
            f"   🏆 {player.get('season_trophies', 0)} Trophies\n"
            f"   🦋 {player['hashira']}\n\n"
        )
    
    caption += "━━━━━━━━━━━━━━━━━━━━━━"
    
    await message.reply_text(
        caption,
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# MISSIONS
# ==========================================

@app.on_message(filters.command("missions"))
async def missions_command(client: Client, message: Message):
    """Display missions"""
    user_id = message.from_user.id
    player = await ds_users.find_one({"user_id": user_id})
    
    if not player:
        await message.reply_text("You haven't joined the Demon Slayer Corps!")
        return
    
    missions = [
        {
            "name": "Demon Slayer",
            "description": f"Defeat 10 demons",
            "progress": player.get('demons_defeated', 0),
            "target": 10,
            "reward": f"+50 Trophies",
            "completed": player.get('demons_defeated', 0) >= 10
        },
        {
            "name": "Rising Star",
            "description": f"Reach Level {player['level'] + 5}",
            "progress": player['level'],
            "target": player['level'] + 5,
            "reward": f"+100 XP",
            "completed": False
        },
        {
            "name": "Trophy Collector",
            "description": f"Collect 100 Trophies",
            "progress": player['trophies'],
            "target": 100,
            "reward": f"+50 Petals",
            "completed": player['trophies'] >= 100
        }
    ]
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "📋 **MISSIONS**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    
    for mission in missions:
        progress_bar = create_progress_bar(mission['progress'], mission['target'])
        status = "✅" if mission['completed'] else "⏳"
        caption += (
            f"{status} **{mission['name']}**\n"
            f"   {mission['description']}\n"
            f"   `{progress_bar}` {mission['progress']}/{mission['target']}\n"
            f"   🎁 {mission['reward']}\n\n"
        )
    
    caption += "━━━━━━━━━━━━━━━━━━━━━━"
    
    await message.reply_text(
        caption,
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# ACHIEVEMENTS
# ==========================================

@app.on_message(filters.command("achievements"))
async def achievements_command(client: Client, message: Message):
    """Display achievements"""
    user_id = message.from_user.id
    player = await ds_users.find_one({"user_id": user_id})
    
    if not player:
        await message.reply_text("You haven't joined the Demon Slayer Corps!")
        return
    
    achievements_data = []
    for ach in ACHIEVEMENTS:
        is_completed = await check_achievement_completed(player, ach['id'])
        progress = await get_achievement_progress(player, ach['id'])
        
        achievements_data.append({
            "name": ach['name'],
            "description": ach['description'],
            "completed": is_completed,
            "progress": progress,
            "requirement": ach['requirement']
        })
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🏆 **ACHIEVEMENTS**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    
    for ach in achievements_data:
        status = "✅" if ach['completed'] else "🔒"
        progress_bar = create_progress_bar(ach['progress'], ach['requirement'])
        caption += (
            f"{status} **{ach['name']}**\n"
            f"   {ach['description']}\n"
            f"   `{progress_bar}` {ach['progress']}/{ach['requirement']}\n\n"
        )
    
    caption += "━━━━━━━━━━━━━━━━━━━━━━"
    
    await message.reply_text(
        caption,
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# DAILY HUNT
# ==========================================

@app.on_message(filters.command("dailyhunt"))
async def daily_hunt_command(client: Client, message: Message):
    """Daily hunt reward"""
    user_id = message.from_user.id
    player = await ds_users.find_one({"user_id": user_id})
    
    if not player:
        await message.reply_text("You haven't joined the Demon Slayer Corps!")
        return
    
    last_daily = player.get('last_daily')
    if last_daily:
        time_diff = datetime.utcnow() - last_daily
        if time_diff.total_seconds() < 86400:
            remaining = int(86400 - time_diff.total_seconds())
            hours = remaining // 3600
            minutes = (remaining % 3600) // 60
            await message.reply_text(
                f"☀️ *You've already claimed your daily hunt!*\n"
                f"Next reward available in {hours}h {minutes}m."
            )
            return
    
    level = player['level']
    xp_reward = 50 + (level * 10)
    coin_reward = 100 + (level * 20)
    
    await ds_users.update_one(
        {"user_id": user_id},
        {
            "$inc": {"xp": xp_reward, "balance": coin_reward},
            "$set": {"last_daily": datetime.utcnow()}
        }
    )
    
    caption = (
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "☀️ **DAILY HUNT REWARD**\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"✨ **Rewards Earned:**\n"
        f"+{xp_reward} XP\n"
        f"+{coin_reward} Petals\n\n"
        "*Come back tomorrow for more!*"
    )
    
    await message.reply_text(
        caption,
        parse_mode=enums.ParseMode.HTML
    )

# ==========================================
# HELPER FUNCTIONS - ACHIEVEMENTS
# ==========================================

async def check_achievement_completed(player, ach_id):
    """Check if achievement is completed"""
    achievements = player.get('achievements', [])
    return ach_id in achievements

async def get_achievement_progress(player, ach_id):
    """Get achievement progress"""
    if ach_id == "first_win":
        return player.get('wins', 0)
    elif ach_id == "100_wins":
        return player.get('wins', 0)
    elif ach_id == "500_wins":
        return player.get('wins', 0)
    elif ach_id == "1000_wins":
        return player.get('wins', 0)
    elif ach_id == "level_50":
        return player.get('level', 0)
    elif ach_id == "level_100":
        return player.get('level', 0)
    return 0

async def check_achievements(client, user_id):
    """Check and unlock achievements"""
    player = await ds_users.find_one({"user_id": user_id})
    if not player:
        return
    
    achievements = player.get('achievements', [])
    new_achievements = []
    
    for ach in ACHIEVEMENTS:
        if ach['id'] in achievements:
            continue
        
        progress = await get_achievement_progress(player, ach['id'])
        if progress >= ach['requirement']:
            new_achievements.append(ach['id'])
    
    if new_achievements:
        await ds_users.update_one(
            {"user_id": user_id},
            {"$push": {"achievements": {"$each": new_achievements}}}
        )

# ==========================================
# HELPER FUNCTIONS - SEASON
# ==========================================

async def get_season_rank(user_id):
    """Get player's season rank"""
    cursor = ds_users.find().sort("season_trophies", -1)
    all_players = await cursor.to_list(length=None)
    
    for i, player in enumerate(all_players, 1):
        if player['user_id'] == user_id:
            return i
    return len(all_players) + 1

# ==========================================
# HELPER FUNCTIONS - REWARDS
# ==========================================

async def get_reward_progress(user_id):
    """Get reward progress"""
    player = await ds_users.find_one({"user_id": user_id})
    if not player:
        return 0
    
    trophies = player['trophies']
    milestones = [100, 250, 500, 1000]
    
    current = 0
    for m in milestones:
        if trophies >= m:
            current = m
    
    return current

async def get_next_milestone(trophies):
    """Get next milestone"""
    milestones = [100, 250, 500, 1000]
    for m in milestones:
        if trophies < m:
            return m
    return None

# ==========================================
# REWARD COMMANDS (Owner Only)
# ==========================================

@app.on_message(filters.command("setreward"))
async def set_reward_command(client, message):
    """Set milestone reward (Owner only)"""
    if message.from_user.id != OWNER_ID:
        await message.reply_text("Only the owner can set rewards!")
        return
    
    args = message.text.split()
    if len(args) < 4:
        await message.reply_text(
            "Usage: /setreward <milestone> <type> <amount>\n\n"
            "Types: xp, coins, trophies\n"
            "Example: /setreward 100 xp 500"
        )
        return
    
    try:
        milestone = int(args[1])
        reward_type = args[2].lower()
        amount = int(args[3])
    except ValueError:
        await message.reply_text("Invalid values!")
        return
    
    if reward_type not in ["xp", "coins", "trophies"]:
        await message.reply_text("Invalid reward type! Use: xp, coins, trophies")
        return
    
    await ds_rewards.update_one(
        {"milestone": milestone},
        {"$set": {reward_type: amount}},
        upsert=True
    )
    
    await message.reply_text(
        f"✅ Reward set for {milestone} trophies:\n"
        f"+{amount} {reward_type.capitalize()}"
    )

@app.on_message(filters.command("showrewards"))
async def show_rewards_command(client, message):
    """Show all rewards (Owner only)"""
    if message.from_user.id != OWNER_ID:
        await message.reply_text("Only the owner can view rewards!")
        return
    
    rewards = await ds_rewards.find().to_list(length=None)
    
    if not rewards:
        await message.reply_text("No rewards set!")
        return
    
    text = "🎯 **Milestone Rewards**\n\n"
    for reward in rewards:
        text += f"🏆 {reward['milestone']} Trophies:\n"
        if "xp" in reward:
            text += f"   +{reward['xp']} XP\n"
        if "coins" in reward:
            text += f"   +{reward['coins']} Petals\n"
        if "trophies" in reward:
            text += f"   +{reward['trophies']} Trophies\n"
        text += "\n"
    
    await message.reply_text(text)

# ==========================================
# MAIN MENU CALLBACKS
# ==========================================

@app.on_callback_query(filters.regex(r"^ds_hunt$"))
async def menu_hunt_callback(client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.delete()
    await hunt_command(client, callback_query.message)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_profile$"))
async def menu_profile_callback(client, callback_query):
    user_id = callback_query.from_user.id
    await show_profile(client, callback_query.message, user_id)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_inventory$"))
async def menu_inventory_callback(client, callback_query):
    user_id = callback_query.from_user.id
    await inventory_command(client, callback_query.message)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_missions$"))
async def menu_missions_callback(client, callback_query):
    await missions_command(client, callback_query.message)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_achievements$"))
async def menu_achievements_callback(client, callback_query):
    await achievements_command(client, callback_query.message)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_leaderboard$"))
async def menu_leaderboard_callback(client, callback_query):
    await leaderboard_command(client, callback_query.message)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_daily$"))
async def menu_daily_callback(client, callback_query):
    await daily_hunt_command(client, callback_query.message)
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_challenge_menu$"))
async def menu_challenge_callback(client, callback_query):
    await callback_query.message.reply_text(
        "⚔️ *To challenge someone, reply to their message and use:*\n"
        "`/challenge`"
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"^ds_profile_view_(\d+)$"))
async def profile_view_callback(client, callback_query):
    user_id = int(callback_query.matches[0].group(1))
    await show_profile(client, callback_query.message, user_id)
    await callback_query.answer()
