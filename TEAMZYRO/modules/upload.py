from TEAMZYRO import app, collection, rarity_map
from pyrogram import filters


@app.on_message(filters.command("rarity"))
async def rarity_count(client, message):

    try:
        text = "❀ ᴄʜᴀʀᴀᴄᴛᴇʀ ʀᴀʀɪᴛʏ ᴄᴏᴜɴᴛ ❀\n"
        text += "─" * 24 + "\n\n"

        total = 0

        for rarity_no in sorted(rarity_map.keys()):
            rarity_name = rarity_map[rarity_no]

            count = await collection.count_documents(
                {"rarity_number": rarity_no}
            )

            total += count

            text += (
                f"❀ {rarity_name}\n"
                f"   ⤷ {count} ᴄʜᴀʀᴀᴄᴛᴇʀꜱ\n\n"
            )

        text += "─" * 24 + "\n"
        text += f"❀ ᴛᴏᴛᴀʟ ᴄʜᴀʀᴀᴄᴛᴇʀꜱ : {total}\n"
        text += "❀ ꜱʜɪɴᴏʙᴜ ᴋᴏᴄʜᴏᴜ ɪꜱ ᴡᴀᴛᴄʜɪɴɢ ʏᴏᴜ 🌸"

        await message.reply_text(text)

    except Exception as e:
        await message.reply_text(
            f"❀ ᴇʀʀᴏʀ : `{e}`"
        )