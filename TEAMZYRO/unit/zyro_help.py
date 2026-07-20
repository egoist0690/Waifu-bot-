# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

# TEAMZYRO/unit/zyro_help.py

HELP_DATA = {
    "balance": {
        "HELP_NAME": "💰 Balance & Pay",
        "HELP": """
💰 **Balance Commands**:
- `/balance` → Check your balance.
- `/balance @username` → Check another user's balance.
- `/balance user_id` → Check balance using user ID.

💳 **Payment Commands**:
- `/pay amount @username` → Send coins to a user.
- `/pay amount user_id` → Send coins using user ID.
- `/pay amount` (reply to a user) → Send coins to the replied user.

⚠️ **Note**:
- You must have enough balance to send coins.
- Payments are final and cannot be reversed.
"""
    },
    "check": {
        "HELP_NAME": "🔍 Check",
        "HELP": """
Use `/check <character_id>` to view details of a character.

- Displays character ID, name, anime, and rarity.
- Shows an image or video if available.
- Use the 'Who Have It' button to see the top 10 owners.
"""
    },
    "guess": {
        "HELP_NAME": "🎯 Guess",
        "HELP": """
Use `/guess <character_name>` to guess the mystery character.

- Earn 40 coins for a correct guess.
- The first correct guess captures the character.
- If incorrect, you can try again.
- A 'See Harem' button lets you view your collected characters.
"""
    },
    "harem": {
        "HELP_NAME": "🌸 Harem",
        "HELP": """
Use `/harem` or `/collection` to view your collected characters.

- Navigate pages using the buttons.
- Filter by rarity using the filter button.
- Use "Collection" button for detailed inline view.
- "💜 AMV" button shows a video-only collection.

Characters are grouped by anime and show the count you own.
"""
    },
    "inline": {
        "HELP_NAME": "🔎 Inline",
        "HELP": """
Use inline queries to search for characters or view collections.

- `@shorekeeper_RoBot query` → Search for characters.
- `@shorekeeper_RoBot collection.<user_id>` → View a user's character collection.
- `@shorekeeper_RoBot collection.<user_id> <name>` → Search within a user's collection.
- `@shorekeeper_RoBot <query>.AMV` → Show characters with video clips.

Results include character name, anime, rarity, and image/video.
"""
    },
    "favorites": {
        "HELP_NAME": "⭐ Favorites",
        "HELP": """
Add your favorite characters to your collection.

- `/fav <character_id>` → Add a character to your favorites.
- Click "✅ Yes" to confirm or "❎ No" to cancel.
- Your favorite characters will be saved for quick access.

Note: You can only favorite characters that are in your collection.
"""
    },
    "claim": {
        "HELP_NAME": "🎁 Claim",
        "HELP": """
Claim a free character every day! 🌟

- `/hclaim` or `/claim` → Claim your daily character.
- You must be in the required channel to claim.
- If you've already claimed today, you'll see the time remaining for the next claim.
- Characters are unique and not repeated from your collection.
- Return tomorrow for another claim! 🌸
"""
    },
    "gift": {
        "HELP_NAME": "🎁 Gift",
        "HELP": """
🎁 **Gift System**  
Send characters to other users using the `/gift` command.

**Commands:**
- `/gift <character_id>` (Reply to a user's message)  
  → Gift a character to another user.

**How it works:**
1. Reply to a user's message.
2. Use `/gift <character_id>` to send a character.
3. The receiver gets a confirmation message.
4. The gift is auto-canceled if not confirmed within 1 hour.
"""
    },
    "jackpot": {
        "HELP_NAME": "🎰 Jackpot",
        "HELP": """
🎰 **Jackpot Game**  
Try your luck with the jackpot and win coins!

**Commands:**
- `/jackpot`  
  → Roll the slot machine and earn coins.

**How it works:**
1. You can play twice per day.
2. The bot rolls a 🎰 dice.
3. Your winnings depend on the score:
   - 64 → 2000 coins 🎉
   - Other scores → 5 × score coins.
4. Your balance updates automatically.
"""
    },
    "rankings": {
        "HELP_NAME": "🏆 Rankings",
        "HELP": """
🏆 **Rankings & Leaderboards**  
Check out the top users and groups in different categories!

**Commands:**
- `/rank`  
  → View the Top 10 Users with the most characters.

**Categories:**
1. **Top Users** → Users with the highest number of characters.
2. **Top Groups** → Groups that have guessed the most characters.
3. **MTOP** → Users ranked by the highest coin balance.

**How it works:**
- `/rank` will display the top 10 users based on character count.
- You can switch between Top Users, Top Groups, and MTOP using the buttons.
- Rankings update dynamically as users collect characters or earn coins.
"""
    },
    "sips": {
        "HELP_NAME": "🔍 Sips",
        "HELP": """
Use this command to search for characters by name.

Commands:
- /sips <character_name> → Search for a character by name.
- Pagination buttons will appear if multiple results are found.

Each result includes:
- Character name
- Anime name
- Character ID
- Rarity indicator
"""
    },
    "shop": {
        "HELP_NAME": "🛒 Shop",
        "HELP": """
🛒 Shop Commands:
- /shop - Open the shop menu.
- /hshopmenu - Alternative command to open the shop.
- /hshop - Another way to access the shop.
- /addshop <id> <price> - Add a character to the shop (Admin only).

🛍️ How It Works:
1. Use /shop to browse characters.
2. Click "Buy" to purchase a character.
3. Click "Next" to view more characters.
4. Make sure you have enough balance!

🔹 Enjoy shopping!
"""
    },
    "coinflip": {
        "HELP_NAME": "🪙 Coinflip",
        "HELP": """
🪙 **Coinflip Betting Game** 🪙

🎮 **How to Play:**
- Use `/coinflip <amount> <heads/tails>` (or `/toss <amount> <h/t>`).
- If your guess is correct, you win **2x your bet**!
- If your guess is incorrect, you lose your bet.

📝 **Limits:**
- Minimum bet: 100 coins.
- Maximum bet: 50,000 coins.
"""
    },
    "slots": {
        "HELP_NAME": "🎰 Slots",
        "HELP": """
🎰 **Slot Machine Game** 🎰

🎮 **How to Play:**
- Spin the slots using `/slot <amount>` (or `/slots <amount>`).
- The reels spin and generate 3 random emojis.

🏆 **Payouts:**
- 3 matching emojis → **5x payout**! (e.g. [ 💎 | 💎 | 💎 ])
- 2 matching emojis → **1.5x payout**! (e.g. [ 🍒 | 🍋 | 🍒 ])
- 0 matching emojis → Bet is lost.

📝 **Limits:**
- Minimum bet: 100 coins.
- Maximum bet: 50,000 coins.
"""
    },
    "hl": {
        "HELP_NAME": "🃏 High Low",
        "HELP": """
🃏 **Higher or Lower Card Game** 🃏

🎮 **How to Play:**
- Start using `/hl <amount>` (or `/highlow <amount>`).
- Guess if the next card drawn will be **Higher** or **Lower** than the current card.
- Correct guesses increase your streak and current winnings.
- You can click the **Cashout** button at any point to claim your winnings!
- If you guess wrong, you bust and lose the bet.

🏆 **Streak Payouts:**
- Streak 1: **1.4x**
- Streak 2: **1.8x**
- Streak 3: **2.2x**
- Streak 4: **2.6x** (+0.4x per correct guess!)

📝 **Limits:**
- Minimum bet: 100 coins.
- Maximum bet: 50,000 coins.
"""
    },
    "blackjack": {
        "HELP_NAME": "🃏 Blackjack",
        "HELP": """
🃏 **Blackjack Table Game** 🃏

🎮 **How to Play:**
- Start using `/bj <amount>` (or `/blackjack <amount>`).
- You and the dealer are dealt 2 cards. Draw cards to get as close to 21 as possible.
- Use **Hit 🟢** to draw a card, or **Stand 🔴** to end your turn.
- If your hand exceeds 21, you bust (lose).

🏆 **Payouts:**
- Standard Win: **2.0x payout**
- Natural Blackjack (21): **2.5x payout**
- Push (Tie): Bet Refunded

📝 **Limits:**
- Minimum bet: 100 coins.
- Maximum bet: 50,000 coins.
"""
    },
    "wheel": {
        "HELP_NAME": "🎡 Wheel",
        "HELP": """
🎡 **Wheel of Fortune Spin** 🎡

🎮 **How to Play:**
- Spin the lucky wheel using `/spin <amount>` (or `/wheel <amount>`).

🏆 **Wheel Sectors:**
- ❌ Bust: 0.0x payout (35% chance)
- 📉 Half Loss: 0.5x payout (20% chance)
- ⚖️ Push: 1.0x payout (15% chance)
- 📈 Win: 1.5x payout (15% chance)
- 🔥 Double: 2.0x payout (10% chance)
- 🚀 Jackpot: 5.0x payout (4% chance)
- 🌟 **Waifu Drop**: Win a random Legendary/Celestial character! (1% chance)

📝 **Limits:**
- Minimum bet: 100 coins.
- Maximum bet: 50,000 coins.
"""
    },
    "new_char": {
        "HELP_NAME": "📝 New Character",
        "HELP": """
➤ /addchar character-name anime-name - Upload a character request with an image.
➤ /upload (or /gupload) character-name anime-name rarity-number - Upload and add a character directly (Admins only).
➤ /server - Change the upload server (ImgBB or Catbox) for your uploads.

Admins can approve or reject the request using the provided buttons.

➤ Rarity options:
- ⚪️ Common
- 🟣 Rare
- 🟡 Legendary
- 🟢 Medium
- 💮 Special Edition
- 🔮 Limited Edition
- 💸 Premium Edition
- 🌤 Summer
- 🎐 Celestial
- ❄️ Winter
- 💝 Valentine
- 🎃 Halloween
- 🎄 Christmas Special
- 🧧 Events
- 🍑 Echhi
- 🎗️ AMV Edition
- 🌧 Rainy
- 🫧 Aquatic

➤ Admin Commands:
- Approve a pending character request.
- Cancel an upload request.

Make sure to reply with an image when using /addchar or /upload!
"""
    },
    "transfer": {
        "HELP_NAME": "📦 Transfer",
        "HELP": """
📦 **Character Transfer System** (VIP Only)

**Commands:**
- `/transfer <user_id> <owner_id>` 
  → Start a secure character transfer from a user to a receiver owner.
- `/backtransfer <transfer_id>` (or `/untransfer` / `/trback`)
  → Rollback and revert a completed transfer (valid for up to 1 hour).

**How it works:**
1. A VIP user initiates the transfer with `/transfer <user_id> <owner_id>`.
2. A confirmation prompt with Confirm/Cancel buttons is displayed.
3. The requester clicks Confirm to execute, or Cancel to abort.
4. If confirmed, all characters are transferred, and a dynamic Transfer ID is generated.
5. You can undo this action within 1 hour using `/backtransfer <transfer_id>`.
"""
    },
    "bounty": {
        "HELP_NAME": "🏴‍☠️ Bounty",
        "HELP": """
🏴‍☠️ **Wanted Bounty Poster Generator**

**Commands:**
- `/bounty` 
  → Generate your custom One Piece-style Wanted Poster showing your balance as your bounty!
- `/bounty @username` (or reply / user_id)
  → View the wanted poster and bounty details of another user.

**How it works:**
1. Your Telegram profile picture is cropped and framed inside the poster.
2. Your name and balance are drawn with custom distressed typography.
3. The custom Berry symbol (฿) is drawn natively.
"""
    },
    "mines": {
        "HELP_NAME": "💣 Mines",
        "HELP": """
💣 **Minesweeper Casino** 💣

**Commands:**
- `/mines [bet_amount] [mine_count]` 
  → Start a new Minesweeper game with custom bet and mine risk.

**Limits:**
- Bet amount: 500 to 100,000 coins (Default: 1000)
- Mine count: 3 to 5 mines (Default: 3)

**How it works:**
1. A 4x4 grid is created with your choice of hidden mines.
2. Sweep the board clicking cells to find 💎 Diamonds.
3. A single mine explosion will instantly trigger Game Over and result in losing your bet.
4. Cashout your winnings at any time using the Claim button.

🏆 **Rewards:**
- Mathematically calculated multipliers based on the number of safe cells opened and mines hidden (with 95% RTP).
- Hitting 4+ safe cells gives a chance to win a bonus Character drop!
"""
    },
    "ox": {
        "HELP_NAME": "⭕ Tic Tac Toe",
        "HELP": """
⭕ **Tic Tac Toe (O/X) Betting** ⭕

**Commands:**
- `/ox <bet>` 
  → Host a new game lobby with the specified bet.
- `/oxstats` 
  → Check your Tic Tac Toe statistics.
- `/oxstats @username` (or user_id)
  → Check another player's statistics.
- `/oxtop` 
  → View the leaderboard of top players.
- `/oxactive` 
  → See the number of active games in progress.

**Game Rules:**
1. **Lobby & Join**: Host sets a bet (100 to 100,000 coins). Another player clicks **Join Game** to match the bet.
2. **Setup**: Symbols (❌/⭕) and first turn are assigned randomly.
3. **Turn Rules**: You have **2 minutes** to make a move on the 3x3 board. Clicking empty cells updates the grid and switches turns.
4. **Win Condition**: Form a line of 3 symbols horizontally, vertically, or diagonally to win the entire prize pool (2x bet).
5. **Draw Condition**: If all cells are filled with no winner, both players are fully refunded.
6. **AFK Protection**: Exceeding the 2-minute timer on your turn triggers an automatic loss, awarding the win to your opponent.
7. **Auto-Cancellation**: If a lobby remains empty for **5 minutes**, it is cancelled automatically and the host is refunded.
"""
    },
    "demonslayer": {
        "HELP_NAME": "⚔️ Demon Slayer",
        "HELP": """
🌸 **DEMON SLAYER RPG** 🌸

**Commands:**
/ **demonslayer** - Start or view your RPG journey
/ **hunt** - Hunt demons for XP and trophies
/ **dprofile** - View your detailed profile
/ **inv** - Check your inventory and progress
/ **challenge** - Challenge another player to PvP
/ **dtop** - View monthly leaderboard
/ **missions** - View your active missions
/ **achievements** - Track your achievements
/ **dailyhunt** - Claim daily rewards

━━━━━━━━━━━━━━━━━━━━━━

**🦋 Hashira Selection**
Choose your mentor from 9 Hashiras:
Shinobu, Giyu, Rengoku, Muichiro, Mitsuri,
Sanemi, Obanai, Gyomei, Tengen

Each Hashira grants unique passive abilities!

━━━━━━━━━━━━━━━━━━━━━━

**⚔️ Battle System**
- Fight demons with interactive combat
- Attack, defend, and use critical hits
- Earn XP, Trophies, and Petals
- Level up and increase your stats
- Progress through 11 ranks to become Hashira

━━━━━━━━━━━━━━━━━━━━━━

**🏆 Features**
- PvP battles with other slayers
- Daily rewards and missions
- Achievement tracking
- Monthly seasons with leaderboard
- Reward milestones at 100/250/500/1000 trophies
"""
    }
}
