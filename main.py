import re
import os
import time
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message

# Replace these with your actual credentials
API_ID = "18618422"
API_HASH = "f165b1caec3cfa4df943fe1cbe82d22a" 
BOT_TOKEN = "7557391528:AAEx0LyZGEDr2JoBEka6FrT7cPqAKSFU0IU"

# Initialize the bot
app = Client("cc_tools_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user states and files
user_data = {}

# Function to split a large file into smaller chunks
def split_file(file_path, chunk_size=300 * 1024 * 1024):  # 300 MB chunks
    chunk_files = []
    with open(file_path, "rb") as f:
        chunk_number = 0
        while True:
            chunk_data = f.read(chunk_size)
            if not chunk_data:
                break
            chunk_file = f"{file_path}_chunk_{chunk_number}.txt"
            with open(chunk_file, "wb") as chunk_f:
                chunk_f.write(chunk_data)
            chunk_files.append(chunk_file)
            chunk_number += 1
    return chunk_files

# Keyboard builders
def main_menu_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚡️ ꜰɪʟᴛᴇʀ ʙʏ ʙɪɴ", callback_data="filter_bin"),
            InlineKeyboardButton("🧹 ᴄʟᴇᴀɴ ᴄᴀʀᴅꜱ", callback_data="clean_cards")
        ],
        [
            InlineKeyboardButton("📚 ᴍᴇʀɢᴇ ꜰɪʟᴇꜱ", callback_data="merge_files"),
            InlineKeyboardButton("🎯 ʙɪɴ ꜱʜᴏʀᴛ", callback_data="bin_short")
        ],
        [
            InlineKeyboardButton("📊 ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ", callback_data="statistics"),
            InlineKeyboardButton("❓ ʜᴇʟᴘ", callback_data="help")
        ],
        [
            InlineKeyboardButton("🧼 ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ", callback_data="remove_duplicates")
        ]
    ])

def back_button_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🔙 ʙᴀᴄᴋ ᴛᴏ ᴍᴀɪɴ ᴍᴇɴᴜ", callback_data="back_to_main")
    ]])

# Start command handler
@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    user_name = message.from_user.first_name
    welcome_text = (
        f"🌟 **ᴡᴇʟᴄᴏᴍᴇ {user_name.upper()}!** 🌟\n\n"
        "🚀 **ᴄʜᴏᴏꜱᴇ ꜰʀᴏᴍ ᴛʜᴇꜱᴇ ᴘᴏᴡᴇʀꜰᴜʟ ᴏᴘᴛɪᴏɴꜱ:**\n\n"
        "⚡️ **ꜰɪʟᴛᴇʀ ʙʏ ʙɪɴ**: ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴀʀᴅ ꜰɪʟᴛᴇʀɪɴɢ\n"
        "🧹 **ᴄʟᴇᴀɴ ᴄᴀʀᴅꜱ**: ᴠᴀʟɪᴅᴀᴛᴇ ᴀɴᴅ ꜰᴏʀᴍᴀᴛ ᴄᴀʀᴅꜱ\n"
        "📚 **ᴍᴇʀɢᴇ ꜰɪʟᴇꜱ**: ᴄᴏᴍʙɪɴᴇ ᴍᴜʟᴛɪᴘʟᴇ ꜰɪʟᴇꜱ\n"
        "🎯 **ʙɪɴ ꜱʜᴏʀᴛ**: ᴇxᴛʀᴀᴄᴛ ᴜɴɪQᴜᴇ ʙɪɴꜱ\n"
        "📊 **ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ**: ᴠɪᴇᴡ ᴄᴀʀᴅ ᴀɴᴀʟʏᴛɪᴄꜱ\n"
        "❓ **ʜᴇʟᴘ**: ɢᴇᴛ ᴜꜱᴀɢᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ\n"
        "🧼 **ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ**: ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴄᴄꜱ\n\n"
        "_ᴍᴀᴅᴇ ᴡɪᴛʜ ❤️ ʙʏ @everyonefake_"
    )
    await message.reply_text(welcome_text, reply_markup=main_menu_keyboard())

# Callback query handler
@app.on_callback_query()
async def callback_query(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data

    if data == "filter_bin":
        user_data[user_id] = {"awaiting_file": True, "action": "filter_bin"}
        await callback_query.message.edit_text(
            "⚡️ **ʙɪɴ ꜰɪʟᴛᴇʀ ᴍᴏᴅᴇ** ⚡️\n\n"
            "📤 **ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ʏᴏᴜʀ `.ᴛxᴛ` ꜰɪʟᴇ ᴄᴏɴᴛᴀɪɴɪɴɢ ᴄᴀʀᴅ ᴅᴇᴛᴀɪʟꜱ.**\n"
            "_ɪ'ʟʟ ʜᴇʟᴘ ʏᴏᴜ ꜰɪʟᴛᴇʀ ꜱᴘᴇᴄɪꜰɪᴄ ʙɪɴꜱ!_ 🎯",
            reply_markup=back_button_keyboard()
        )
    
    elif data == "remove_duplicates":
        user_data[user_id] = {"awaiting_file": True, "action": "remove_duplicates"}
        await callback_query.message.edit_text(
            "🧼 **ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ ᴍᴏᴅᴇ** 🧼\n\n"
            "📤 **ꜱᴇɴᴅ ʏᴏᴜʀ `.ᴛxᴛ` ꜰɪʟᴇ ᴡɪᴛʜ ᴄᴀʀᴅ ᴅᴇᴛᴀɪʟꜱ.**\n"
            "_ɪ'ʟʟ ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴄᴀʀᴅꜱ!_ ✨",
            reply_markup=back_button_keyboard()
        )

    elif data == "clean_cards":
        user_data[user_id] = {"awaiting_file": True, "action": "clean_cards"}
        await callback_query.message.edit_text(
            "🧹 **ᴄᴀʀᴅ ᴄʟᴇᴀɴɪɴɢ ᴍᴏᴅᴇ** 🧹\n\n"
            "📤 **ꜱᴇɴᴅ ʏᴏᴜʀ `.ᴛxᴛ` ꜰɪʟᴇ ᴡɪᴛʜ ᴄᴀʀᴅ ᴅᴇᴛᴀɪʟꜱ.**\n"
            "_ɪ'ʟʟ ᴄʟᴇᴀɴ ᴀɴᴅ ᴠᴀʟɪᴅᴀᴛᴇ ᴛʜᴇᴍ!_ ✨",
            reply_markup=back_button_keyboard()
        )

    elif data == "merge_files":
        user_data[user_id] = {"awaiting_files": True, "files": [], "start_time": time.time()}
        await callback_query.message.edit_text(
            "📚 **ꜰɪʟᴇ ᴍᴇʀɢᴇʀ ᴍᴏᴅᴇ** 📚\n\n"
            "📤 **ꜱᴇɴᴅ ʏᴏᴜʀ `.ᴛxᴛ` ꜰɪʟᴇꜱ.**\n"
            "✅ **ᴜꜱᴇ `/ᴅᴏɴᴇ` ᴡʜᴇɴ ꜰɪɴɪꜱʜᴇᴅ!**\n\n"
            "_ᴘʀᴏ ᴛɪᴘ: ꜰɪʟᴇꜱ ᴀʀᴇ ᴘʀᴏᴄᴇꜱꜱᴇᴅ ɪɴ ᴏʀᴅᴇʀ_ 📝",
            reply_markup=back_button_keyboard()
        )

    elif data == "bin_short":
        user_data[user_id] = {"awaiting_file": True, "action": "bin_short"}
        await callback_query.message.edit_text(
            "🎯 **ʙɪɴ ꜱʜᴏʀᴛᴇɴᴇʀ ᴍᴏᴅᴇ** 🎯\n\n"
            "📤 **ꜱᴇɴᴅ ʏᴏᴜʀ `.ᴛxᴛ` ꜰɪʟᴇ ᴡɪᴛʜ ᴄᴀʀᴅ ᴅᴇᴛᴀɪʟꜱ.**\n"
            "_ɪ'ʟʟ ᴇxᴛʀᴀᴄᴛ ᴜɴɪQᴜᴇ ʙɪɴꜱ!_ 🎲",
            reply_markup=back_button_keyboard()
        )

    elif data == "statistics":
        await callback_query.message.edit_text(
            "📊 **ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ** 📊\n\n"
            "• ꜱᴛᴀᴛᴜꜱ: ᴏɴʟɪɴᴇ 🌟\n"
            "• ᴘʀᴏᴄᴇꜱꜱɪɴɢ ꜱᴘᴇᴇᴅ: ᴜʟᴛʀᴀ ꜰᴀꜱᴛ ⚡️\n"
            "• ᴜᴘᴛɪᴍᴇ: ᴀᴄᴛɪᴠᴇ 🟢\n\n"
            "_ʙᴏᴛ ɪꜱ ʀᴜɴɴɪɴɢ ꜱᴍᴏᴏᴛʜʟʏ!_ 🚀",
            reply_markup=back_button_keyboard()
        )

    elif data == "help":
        help_text = (
            "❓ **ʜᴇʟᴘ ɢᴜɪᴅᴇ** ❓\n\n"
            "1️⃣ **ꜰɪʟᴛᴇʀ ʙʏ ʙɪɴ:**\n"
            "📤 ꜱᴇɴᴅ ꜰɪʟᴇ → ᴇɴᴛᴇʀ ʙɪɴ → ɢᴇᴛ ꜰɪʟᴛᴇʀᴇᴅ ᴄᴀʀᴅꜱ\n\n"
            "2️⃣ **ᴄʟᴇᴀɴ ᴄᴀʀᴅꜱ:**\n"
            "📤 ꜱᴇɴᴅ ꜰɪʟᴇ → ɢᴇᴛ ᴄʟᴇᴀɴᴇᴅ ᴄᴀʀᴅꜱ ɪɴꜱᴛᴀɴᴛʟʏ\n\n"
            "3️⃣ **ᴍᴇʀɢᴇ ꜰɪʟᴇꜱ:**\n"
            "📤 ꜱᴇɴᴅ ᴍᴜʟᴛɪᴘʟᴇ ꜰɪʟᴇꜱ → ᴛʏᴘᴇ `/ᴅᴏɴᴇ` → ɢᴇᴛ ᴍᴇʀɢᴇᴅ ꜰɪʟᴇ\n\n"
            "4️⃣ **ʙɪɴ ꜱʜᴏʀᴛ:**\n"
            "📤 ꜱᴇɴᴅ ꜰɪʟᴇ → ᴇɴᴛᴇʀ ᴅɪɢɪᴛꜱ → ɢᴇᴛ ᴜɴɪQᴜᴇ ʙɪɴꜱ\n\n"
            "5️⃣ **ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ:**\n"
            "📤 ꜱᴇɴᴅ ꜰɪʟᴇ → ɢᴇᴛ ᴜɴɪQᴜᴇ ᴄᴀʀᴅꜱ\n\n"
            "_ɴᴇᴇᴅ ᴍᴏʀᴇ ʜᴇʟᴘ? ᴄᴏɴᴛᴀᴄᴛ @everyonefake_ 🤝"
        )
        await callback_query.message.edit_text(help_text, reply_markup=back_button_keyboard())

    elif data == "back_to_main":
        user_name = callback_query.from_user.first_name
        welcome_text = (
            f"🌟 **ᴡᴇʟᴄᴏᴍᴇ {user_name.upper()}!** 🌟\n\n"
            "🚀 **ᴄʜᴏᴏꜱᴇ ꜰʀᴏᴍ ᴛʜᴇꜱᴇ ᴘᴏᴡᴇʀꜰᴜʟ ᴏᴘᴛɪᴏɴꜱ:**\n\n"
            "⚡️ **ꜰɪʟᴛᴇʀ ʙʏ ʙɪɴ**: ᴀᴅᴠᴀɴᴄᴇᴅ ᴄᴀʀᴅ ꜰɪʟᴛᴇʀɪɴɢ\n"
            "🧹 **ᴄʟᴇᴀɴ ᴄᴀʀᴅꜱ**: ᴠᴀʟɪᴅᴀᴛᴇ ᴀɴᴅ ꜰᴏʀᴍᴀᴛ ᴄᴀʀᴅꜱ\n"
            "📚 **ᴍᴇʀɢᴇ ꜰɪʟᴇꜱ**: ᴄᴏᴍʙɪɴᴇ ᴍᴜʟᴛɪᴘʟᴇ ꜰɪʟᴇꜱ\n"
            "🎯 **ʙɪɴ ꜱʜᴏʀᴛ**: ᴇxᴛʀᴀᴄᴛ ᴜɴɪQᴜᴇ ʙɪɴꜱ\n"
            "📊 **ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ**: ᴠɪᴇᴡ ᴄᴀʀᴅ ᴀɴᴀʟʏᴛɪᴄꜱ\n"
            "❓ **ʜᴇʟᴘ**: ɢᴇᴛ ᴜꜱᴀɢᴇ ɪɴꜱᴛʀᴜᴄᴛɪᴏɴꜱ\n"
            "🧼 **ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ**: ʀᴇᴍᴏᴠᴇ ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴄᴄꜱ\n\n"
            "_ᴍᴀᴅᴇ ᴡɪᴛʜ ❤️ ʙʏ @everyonefake_"
        )
        await callback_query.message.edit_text(welcome_text, reply_markup=main_menu_keyboard())

# Document handler
@app.on_message(filters.document)
async def handle_document(client, message: Message):
    user_id = message.from_user.id

    if user_id in user_data and user_data[user_id].get("awaiting_files"):
        if not message.document.file_name.endswith(".txt"):
            await message.reply_text("❌ **ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴏɴʟʏ `.ᴛxᴛ` ꜰɪʟᴇꜱ!**")
            return

        file_path = f"file_{user_id}_{int(time.time())}.txt"
        await message.download(file_path)

        user_data[user_id]["files"].append(f'downloads/{file_path}')
        files_count = len(user_data[user_id]["files"])

        await message.reply_text(
            f"📥 **ꜰɪʟᴇ #{files_count} ʀᴇᴄᴇɪᴠᴇᴅ!**\n"
            "_ꜱᴇɴᴅ ᴍᴏʀᴇ ᴏʀ ᴜꜱᴇ_ `/ᴅᴏɴᴇ` _ᴛᴏ ꜰɪɴɪꜱʜ!_ ✨",
            reply_markup=back_button_keyboard()
        )

    elif user_id in user_data and user_data[user_id].get("awaiting_file"):
        if not message.document.file_name.endswith(".txt"):
            await message.reply_text("❌ **ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴏɴʟʏ `.ᴛxᴛ` ꜰɪʟᴇꜱ!**")
            return

        try:
            file_path = f"file_{user_id}_{time.time()}.txt"
            await message.download(file_path)

            file_path = f"downloads/{file_path}"
            # Check file size
            #file_size = os.path.getsize(file_path)
            #if file_size > 300 * 1024 * 1024:  # 300 MB limit
            #    await message.reply_text("❌ **ꜰɪʟᴇ ɪꜱ ᴛᴏᴏ ʟᴀʀɢᴇ! ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴀ ꜰɪʟᴇ ꜱᴍᴀʟʟᴇʀ ᴛʜᴀɴ 50 ᴍʙ.**")
            #    Path(file_path).unlink(missing_ok=True)
            #    return

            with open(file_path, "r", encoding="utf-8") as f:
                cards = f.read().splitlines()

            action = user_data[user_id].get("action")

            if action == "filter_bin":
                await message.reply_text(
                    "🎯 **ᴇɴᴛᴇʀ ʙɪɴ ɴᴜᴍʙᴇʀ(ꜱ)** 🎯\n\n"
                    "• ꜰᴏʀ ꜱɪɴɢʟᴇ ʙɪɴ: ᴇɴᴛᴇʀ 6-8 ᴅɪɢɪᴛꜱ (ᴇ.ɢ., 123456)\n"
                    "• ꜰᴏʀ ᴍᴜʟᴛɪᴘʟᴇ ʙɪɴꜱ: ꜱᴇᴘᴀʀᴀᴛᴇ ᴡɪᴛʜ ᴄᴏᴍᴍᴀꜱ (ᴇ.ɢ., 123456,654321)\n\n"
                    "_ɪ'ʟʟ ꜰɪʟᴛᴇʀ ᴄᴀʀᴅꜱ ᴍᴀᴛᴄʜɪɴɢ ᴛʜᴇ ʙɪɴ(ꜱ)!_",
                    reply_markup=back_button_keyboard()
                )
                user_data[user_id]["file_path"] = file_path
                user_data[user_id]["awaiting_bin"] = True

            elif action == "remove_duplicates":
                start_time = time.time()
                unique_cards = list(set(cards))
                
                output_file = f"unique_cards_{user_id}_{time.time()}.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(unique_cards))

                # Split the file if it's too large
                chunk_files = split_file(output_file)
                for chunk_file in chunk_files:
                    await message.reply_document(
                        document=chunk_file,
                        caption=(
                            "🧼 **ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ ʀᴇᴍᴏᴠᴇᴅ!** 🧼\n\n"
                            f"• ᴏʀɪɢɪɴᴀʟ ᴄᴀʀᴅꜱ: {len(cards)}\n"
                            f"• ᴜɴɪQᴜᴇ ᴄᴀʀᴅꜱ: {len(unique_cards)}\n"
                            f"• ᴅᴜᴘʟɪᴄᴀᴛᴇꜱ ʀᴇᴍᴏᴠᴇᴅ: {len(cards) - len(unique_cards)}\n"
                            f"• ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛɪᴍᴇ: {time.time() - start_time:.2f}ꜱ ⚡️\n\n"
                            "_ᴄʟᴇᴀɴᴇᴅ ᴡɪᴛʜ ❤️ ʙʏ @everyonefake_"
                        ),
                        reply_markup=back_button_keyboard()
                    )
                    Path(chunk_file).unlink(missing_ok=True)

                Path(file_path).unlink(missing_ok=True)
                Path(output_file).unlink(missing_ok=True)

                if user_id in user_data:
                    del user_data[user_id]

            elif action == "clean_cards":
                start_time = time.time()
                cleaned_cards = []
                card_pattern = re.compile(r"(\d{15,16})[\|/:](\d{2})[\|/:](\d{2,4})[\|/:](\d{3,4})")

                for card in cards:
                    card = card.replace(" ", "")
                    match = card_pattern.search(card)
                    if match:
                        formatted_card = f"{match.group(1)}|{match.group(2)}|{match.group(3)}|{match.group(4)}"
                        cleaned_cards.append(formatted_card)

                output_file = f"cleaned_cards_{user_id}_{time.time()}.txt"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(cleaned_cards))

                # Split the file if it's too large
                chunk_files = split_file(output_file)
                for chunk_file in chunk_files:
                    await message.reply_document(
                        document=chunk_file,
                        caption=(
                            "✨ **ᴄʟᴇᴀɴɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ!** ✨\n\n"
                            f"• ᴄᴀʀᴅꜱ ᴘʀᴏ ᴄᴇꜱꜱᴇᴅ: {len(cards)}\n"
                            f"• ᴠᴀʟɪᴅ ᴄᴀʀᴅꜱ: {len(cleaned_cards)}\n"
                            f"• ꜱᴜᴄᴄᴇꜱꜱ ʀᴀᴛᴇ: {(len(cleaned_cards)/len(cards)*100):.1f}%\n"
                            f"• ᴘʀᴏᴄᴇꜱꜱɪɴɢ ᴛɪᴍᴇ: {time.time() - start_time:.2f}ꜱ ⚡️\n\n"
                            "_ᴄʟᴇᴀɴᴇᴅ ᴡɪᴛʜ ❤️ ʙʏ @everyonefake_"
                        ),
                        reply_markup=back_button_keyboard()
                    )
                    Path(chunk_file).unlink(missing_ok=True)

                Path(file_path).unlink(missing_ok=True)
                Path(output_file).unlink(missing_ok=True)

                if user_id in user_data:
                    del user_data[user_id]

            elif action == "bin_short":
                user_data[user_id]["file_path"] = file_path
                await message.reply_text(
                    "🎯 **ᴇɴᴛᴇʀ ʙɪɴ ʟᴇɴɢᴛʜ** 🎯\n\n"
                    "• ʀᴀɴɢᴇ: 6-12 ᴅɪɢɪᴛꜱ\n"
                    "• ꜰᴏʀᴍᴀᴛ: ɴᴜᴍʙᴇʀꜱ ᴏɴʟʏ\n\n"
                    "_ᴇxᴀᴍᴘʟᴇ: 6 ꜰᴏʀ 6-ᴅɪɢɪᴛ ʙɪɴꜱ_",
                    reply_markup=back_button_keyboard()
                )
                user_data[user_id]["awaiting_digits"] = True

        except Exception as e:
            print(f"❌ ᴇʀʀᴏʀ ɪɴ ʜᴀɴᴅʟᴇ_ᴅᴏᴄᴜᴍᴇɴᴛ: {str(e)}")
            await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}\n_ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ!_")

# Done command handler
@app.on_message(filters.command("done"))
async def merge_files(client, message: Message):
    user_id = message.from_user.id

    if user_id in user_data and user_data[user_id].get("awaiting_files"):
        files = user_data[user_id].get("files", [])
        start_time = user_data[user_id].get("start_time", time.time())

        if len(files) == 0:
            await message.reply_text("❌ **ɴᴏ ꜰɪʟᴇꜱ ʀᴇᴄᴇɪᴠᴇᴅ! ᴘʟᴇᴀꜱᴇ ꜱᴇɴᴅ ᴀᴛ ʟᴇᴀꜱᴛ ᴏɴᴇ `.ᴛxᴛ` ꜰɪʟᴇ.**")
            return

        try:
            merged_content = []
            total_lines = 0

            for file_path in files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.read().splitlines()
                        total_lines += len(lines)
                        merged_content.extend(lines)
                except Exception as e:
                    print(f"❌ ᴇʀʀᴏʀ ʀᴇᴀᴅɪɴɢ ꜰɪʟᴇ {file_path}: {str(e)}")
                    await message.reply_text(f"❌ **ᴇʀʀᴏʀ ʀᴇᴀᴅɪɴɢ ꜰɪʟᴇ:** {str(e)}")
                    continue

            output_file = f"merged_files_{user_id}_{time.time()}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(merged_content))

            process_time = time.time() - start_time

            # Split the file if it's too large
            chunk_files = split_file(output_file)
            for chunk_file in chunk_files:
                await message.reply_document(
                    document=chunk_file,
                    caption=(
                        "📚 **ᴍᴇʀɢᴇ ᴄᴏᴍᴘʟᴇᴛᴇ!** 📚\n\n"
                        f"• ꜰɪʟᴇꜱ ᴍᴇʀɢᴇᴅ: {len(files)}\n"
                        f"• ᴛᴏᴛᴀʟ ʟɪɴᴇꜱ: {total_lines:,}\n"
                        f"• ᴘʀᴏᴄᴇꜱꜱ ᴛɪᴍᴇ: {process_time:.2f}ꜱ\n"
                        f"• ꜱᴘᴇᴇᴅ: {int(total_lines/process_time):,} ʟɪɴᴇꜱ/ꜱ\n\n"
                        "_ᴍᴇʀɢᴇᴅ ᴡɪᴛʜ ❤️ ʙʏ @everyonefake_"
                    ),
                    reply_markup=back_button_keyboard()
                )
                Path(chunk_file).unlink(missing_ok=True)

            for file_path in files:
                Path(file_path).unlink(missing_ok=True)
            Path(output_file).unlink(missing_ok=True)

            if user_id in user_data:
                del user_data[user_id]

        except Exception as e:
            print(f"❌ ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ ɪɴ ᴍᴇʀɢᴇ_ꜰɪʟᴇꜱ: {str(e)}")
            await message.reply_text(f"❌ **ᴜɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ:** {str(e)}\n_ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ!_")

# Text message handler
@app.on_message(filters.text)
async def handle_text(client, message: Message):
    user_id = message.from_user.id

    if user_id in user_data and user_data[user_id].get("awaiting_bin"):
        bins_input = message.text.strip()
        bins = [b.strip() for b in bins_input.split(",")]
        bin_pattern = re.compile(r"^\d{6,8}$")  # Validate BIN number format
        
        invalid_bins = [b for b in bins if not bin_pattern.match(b)]
        if invalid_bins:
            await message.reply_text(f"❌ **ɪɴᴠᴀʟɪᴅ ʙɪɴꜱ ᴅᴇᴛᴇᴄᴛᴇᴅ:** {', '.join(invalid_bins)}\n**ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴠᴀʟɪᴅ 6-8 ᴅɪɢɪᴛ ʙɪɴꜱ ꜱᴇᴘᴀʀᴀᴛᴇᴅ ʙʏ ᴄᴏᴍᴍᴀꜱ.**")
            return

        file_path = user_data[user_id].get("file_path")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                cards = f.read().splitlines()

            filtered_cards = [card for card in cards if any(card.startswith(bin) for bin in bins)]

            if len(filtered_cards) == 0:
                await message.reply_text(f"❌ **ɴᴏ ᴄᴀʀᴅꜱ ᴍᴀᴛᴄʜᴇᴅ ᴛʜᴇ ʙɪɴꜱ:** `{', '.join(bins)}`")
                return

            output_file = f"filtered_cards_{user_id}_{time.time()}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(filtered_cards))

            # Split the file if it's too large
            chunk_files = split_file(output_file)
            for chunk_file in chunk_files:
                await message.reply_document(
                    document=chunk_file,
                    caption=(
                        "⚡️ **ꜰɪʟᴛᴇʀɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ!** ⚡️\n\n"
                        f"• ᴛᴏᴛᴀʟ ᴄᴀʀᴅꜱ: {len(cards)}\n"
                        f"• ꜰɪʟᴛᴇʀᴇᴅ ᴄᴀʀᴅꜱ: {len(filtered_cards)}\n"
                        f"• ʙɪɴꜱ ᴜꜱᴇᴅ: {', '.join(bins)}\n\n"
                        "_ꜰɪʟᴛᴇʀᴇᴅ ᴡɪᴛʜ ❤️ ʙʏ @everyonefake_"
                    ),
                    reply_markup=back_button_keyboard()
                )
                Path(chunk_file).unlink(missing_ok=True)

            Path(file_path).unlink(missing_ok=True)
            Path(output_file).unlink(missing_ok=True)

            if user_id in user_data:
                del user_data[user_id]

        except Exception as e:
            print(f"❌ ᴇʀʀᴏʀ ɪɴ ʜᴀɴᴅʟᴇ_ᴛᴇxᴛ (ʙɪɴ ꜰɪʟᴛᴇʀɪɴɢ): {str(e)}")
            await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}\n_ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ!_")

    elif user_id in user_data and user_data[user_id].get("awaiting_digits"):
        bin_length = message.text.strip()
        if not bin_length.isdigit() or int(bin_length) < 6 or int(bin_length) > 12:
            await message.reply_text("❌ **ɪɴᴠᴀʟɪᴅ ʙɪɴ ʟᴇɴɢᴛʜ! ᴘʟᴇᴀꜱᴇ ᴇɴᴛᴇʀ ᴀ ᴠᴀʟɪᴅ ʟᴇɴɢᴛʜ ʙᴇᴛᴡᴇᴇɴ 6 ᴀɴᴅ 12.**")
            return

        file_path = user_data[user_id].get("file_path")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                cards = f.read().splitlines()

            unique_bins = set()
            for card in cards:
                if len(card) >= int(bin_length):
                    unique_bins.add(card[:int(bin_length)])

            output_file = f"unique_bins_{user_id}_{time.time()}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(unique_bins))

            # Split the file if it's too large
            chunk_files = split_file(output_file)
            for chunk_file in chunk_files:
                await message.reply_document(
                    document=chunk_file,
                    caption=(
                        "🎯 **ʙɪɴ ꜱʜᴏʀᴛᴇɴɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇ!** 🎯\n\n"
                        f"• ᴛᴏᴛᴀʟ ᴄᴀʀᴅꜱ: {len(cards)}\n"
                        f"• ᴜɴɪQᴜᴇ ʙɪɴꜱ: {len(unique_bins)}\n"
                        f"• ʙɪɴ ʟᴇɴɢᴛʜ: {bin_length}\n\n"
                        "_ꜱʜᴏʀᴛᴇɴᴇᴅ ᴡɪᴛʜ ❤️ ʙʏ @everyonefake_"
                    ),
                    reply_markup=back_button_keyboard()
                )
                Path(chunk_file).unlink(missing_ok=True)

            Path(file_path).unlink(missing_ok=True)
            Path(output_file).unlink(missing_ok=True)

            if user_id in user_data:
                del user_data[user_id]

        except Exception as e:
            print(f"❌ ᴇʀʀᴏʀ ɪɴ ʜᴀɴᴅʟᴇ_ᴛᴇxᴛ (ʙɪɴ ꜱʜᴏʀᴛᴇɴɪɴɢ): {str(e)}")
            await message.reply_text(f"❌ **ᴇʀʀᴏʀ:** {str(e)}\n_ᴘʟᴇᴀꜱᴇ ᴛʀʏ ᴀɢᴀɪɴ!_")

# Run the bot
app.run()
