import os
from pyrogram import Client, filters
from pyrogram.types import Message

# Environment Variables (Set these in Zeabur)
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
BOT_TOKEN = os.environ["BOT_TOKEN"]

# Chat IDs
SOURCE_CHAT_ID = -1002312779748  # Source group for media forward
DESTINATION_CHAT_ID = -1002740358553  # Destination group (also used for Force Add)
REQUIRED_ADDS = 5  # Members to be added to unlock
GROUP_ID = DESTINATION_CHAT_ID  # Group where force-add is applied

# Create bot client
app = Client("multi_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to track users' added members
user_data = {}

# 📌 Media Forwarding Without Captions
@app.on_message(filters.chat(SOURCE_CHAT_ID))
def forward_media_only(client, message: Message):
    try:
        if message.media:
            message.copy(DESTINATION_CHAT_ID, caption="")  # Remove caption
            print(f"✅ Forwarded media message {message.message_id}")
    except Exception as e:
        print(f"❌ Error forwarding message {message.message_id}: {e}")

# 👤 When New User Joins the Group
@app.on_message(filters.new_chat_members & filters.chat(GROUP_ID))
def handle_new_members(client, message: Message):
    for new_member in message.new_chat_members:
        if new_member.is_bot:
            continue
        user_id = new_member.id
        user_data[user_id] = {"added": set()}
        # Mute user until they add REQUIRED_ADDS members
        client.restrict_chat_member(GROUP_ID, user_id, permissions=None)
        client.send_message(
            GROUP_ID,
            f"🕉️ Ahem... Brahmāsmi.\n\nWelcome, [{new_member.first_name}](tg://user?id={user_id})!\n"
            f"🔒 To unlock the chat, add {REQUIRED_ADDS} members.\n"
            f"📿 This is your path to moksha. 🌌",
            parse_mode="markdown"
        )

# 🔍 Monitor If Member is Adding Others
@app.on_message(filters.chat(GROUP_ID))
def check_adds(client, message: Message):
    if message.new_chat_members:
        inviter = message.from_user
        if inviter and inviter.id in user_data:
            for m in message.new_chat_members:
                user_data[inviter.id]["added"].add(m.id)
            count = len(user_data[inviter.id]["added"])
            if count >= REQUIRED_ADDS:
                client.restrict_chat_member(GROUP_ID, inviter.id, permissions={
                    "can_send_messages": True,
                    "can_send_media_messages": True,
                    "can_send_other_messages": True,
                    "can_add_web_page_previews": True,
                })
                client.send_message(
                    GROUP_ID,
                    f"🔓 [{inviter.first_name}](tg://user?id={inviter.id}) ka bandhan toot gaya hai.\n"
                    f"Chat ab khula hai! 🕊️",
                    parse_mode="markdown"
                )
            else:
                remaining = REQUIRED_ADDS - count
                client.send_message(
                    GROUP_ID,
                    f"⏳ Tumne {count} yogi bulaye.\n"
                    f"Aur {remaining} aur chahiye moksha ke liye... ⚡",
                    reply_to_message_id=message.message_id
                )

# ✅ Start bot
app.run()
