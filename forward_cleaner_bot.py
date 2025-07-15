from pyrogram import Client, filters

api_id = 24264746
api_hash = "d32b45046f15b9ab89367a2f4cb31d3d"
bot_token = "8006692160:AAFRcTXu5hpnYwe8QV_y69PhbVF04xR2v6g"

app = Client("forward_cleaner_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

source_chat_id = -1002312779748
destination_chat_id = -1002740358553

@app.on_message(filters.chat(source_chat_id))
def forward_cleaned(client, message):
    message.copy(destination_chat_id)

app.run()
