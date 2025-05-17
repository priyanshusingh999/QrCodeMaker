import time, sqlite3, json
from connaction import get_updates, send_message, send_photo, get_chat_member
from heandler import *
from config import OWNER_ID, FORCE_JOIN_CHANNEL
from database import insert_user
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is Running!'

def run_flask():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run_flask).start()



def main(FORCE_JOIN_CHANNEL): # Main loop to check for new messages
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            if 'message' in update and 'chat' in update['message'] and 'id' in update['message']['chat'] and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                message_text = update['message']['text']
                print(f"Received message from chat_id {chat_id}: {message_text}")

                # Safely extract user details with default values
                first_name = update.get('message', {}).get('from', {}).get('first_name', ' ')
                last_name = update.get('message', {}).get('from', {}).get('last_name', ' ')
                username = update.get('message', {}).get('from', {}).get('username')
                print(f"first_name: {first_name}, last_name: {last_name}, username: {username}")
                insert_user(chat_id, first_name, last_name, username) # Insert or update user details in the database

                # Check if user is member of the required channel for force join

                chat_member_info = get_chat_member(FORCE_JOIN_CHANNEL, chat_id)
                if chat_member_info is None or chat_member_info.get('result', {}).get('status') in ['left', 'kicked']:
                    inline_keyboard = {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "🔗 Join Channel", "url": f"https://t.me/{FORCE_JOIN_CHANNEL.strip('@')}"
                                }
                            ]
                        ]
                    }
                    join_message = f"<b>🔒Please hamare channel ko join karo tabhi aap bot ko use kar sakte ho.</b>"
                    send_message(chat_id, join_message, reply_markup=inline_keyboard)
                    continue  # Skip processing this message further

            if message_text.startswith('/'):
                get_command(chat_id, first_name, last_name, username, message_text)
            # Respond to the message
            else:
                send_message(chat_id, f'You said: {message_text}')

        # Update the offset to the last update's ID
        if updates.get('result'):
            offset = updates['result'][-1]['update_id'] + 1

        # Sleep for a while before checking for new updates
        time.sleep(1)

if __name__ == '__main__':
    main(FORCE_JOIN_CHANNEL)
