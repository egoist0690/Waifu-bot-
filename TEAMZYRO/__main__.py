# ==========================================
# Creator: MrZyro
# Telegram: @MrZyro_dev
# GitHub: https://github.com/MrZyro
# ==========================================

from TEAMZYRO import *
import importlib
import logging
import asyncio
import sys
from TEAMZYRO.modules import ALL_MODULES


async def initialize_bot():
    """Initialize bot and database asynchronously."""
    LOGGER("TEAMZYRO").info("🦋 Initializing WaifuBot...")
    
    # Load all modules
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("TEAMZYRO.modules." + module_name)
    LOGGER("TEAMZYRO.modules").info("𝐀𝐥𝐥 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 𝐋𝐨𝐚𝐝𝐞𝐝 𝐁𝐚𝐛𝐲🥳...")
    
    # Initialize database
    LOGGER("TEAMZYRO").info("🔄 Initializing database connections and indexes...")
    try:
        await initialize_database()
        LOGGER("TEAMZYRO").info("✅ Database initialization complete")
    except Exception as e:
        LOGGER("TEAMZYRO").error(f"❌ Database initialization failed: {e}")
        LOGGER("TEAMZYRO").warning("⚠️ Continuing with potentially slower queries...")
    
    return True


def main() -> None:
    # Create event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Initialize bot asynchronously
    try:
        loop.run_until_complete(initialize_bot())
    except Exception as e:
        LOGGER("TEAMZYRO").critical(f"❌ Bot initialization failed: {e}")
        sys.exit(1)
    
    # Start the client
    ZYRO.start()

    # Verify FORCE_JOIN admin permissions and get/generate invite link
    try:
        try:
            chat_target = int(FORCE_JOIN)
        except ValueError:
            chat_target = FORCE_JOIN
            
        chat_obj = ZYRO.get_chat(chat_target)
        invite_link = chat_obj.invite_link
        if not invite_link:
            invite = ZYRO.create_chat_invite_link(chat_target)
            invite_link = invite.invite_link
            
        FORCE_JOIN_LINK = invite_link
        LOGGER("TEAMZYRO").info(f"Successfully verified FORCE_JOIN admin rights. Link: {invite_link}")
    except Exception as e:
        LOGGER("TEAMZYRO").error(
            "\n"
            "=======================================================================\n"
            "❌ CRITICAL STARTUP ERROR:\n"
            f"Bot is NOT an admin in the FORCE_JOIN channel/chat ({FORCE_JOIN})!\n"
            "Please ensure the bot is added to the channel as an Admin and has\n"
            "permission to invite users.\n"
            f"Details: {e}\n"
            "======================================================================="
        )
        try:
            ZYRO.stop()
        except:
            pass
        sys.exit(1)

    # Verify BOT_LOGGING permissions by sending a startup message
    try:
        try:
            log_target = int(BOT_LOGGING)
        except ValueError:
            log_target = BOT_LOGGING
            
        test_msg = ZYRO.send_message(
            chat_id=log_target,
            text="⚙️ **WaifuBot Startup Notification**:\n"
                 "✅ Successfully connected & verified write permissions in the logs channel!\n"
                 "✅ Database indexes initialized successfully!\n"
                 "🦋 Bot is ready to serve!"
        )
        LOGGER("TEAMZYRO").info(f"Successfully verified BOT_LOGGING permissions. Test message sent (ID: {test_msg.id}).")
    except Exception as e:
        LOGGER("TEAMZYRO").error(
            "\n"
            "=======================================================================\n"
            "❌ CRITICAL STARTUP ERROR:\n"
            f"Bot cannot post/send messages to BOT_LOGGING chat ({BOT_LOGGING})!\n"
            "Please ensure the bot is added to the log channel/group and has permission\n"
            "to post messages.\n"
            f"Details: {e}\n"
            "======================================================================="
        )
        try:
            ZYRO.stop()
        except:
            pass
        sys.exit(1)

    # Send startup message to channel
    send_start_message()
    
    # Start polling
    application.run_polling(drop_pending_updates=True)
    
    LOGGER("TEAMZYRO").info(
        "╔═════ஜ۩۞۩ஜ════╗\n  ☠︎︎MADE BY TEAMEGOIST☠︎︎\n╚═════ஜ۩۞۩ஜ════╝"
    )
    

if __name__ == "__main__":
    main()
