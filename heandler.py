from connaction import *
from config import OWNER_ID
from database import *
from qrcode_feature import get_qrcode_maker

def is_owner(chat_id):
    return chat_id == OWNER_ID

def get_command(chat_id, first_name, last_name, username, message_text):
    # Ignore messages from banned users
    if is_user_banned(chat_id):
        return

    if message_text == '/start':
        get_start_message(chat_id, first_name, last_name, username)
    elif message_text == '/help':
        get_help_message(chat_id)
    elif message_text.startswith('/qr'):
        get_qrcode_maker(chat_id, message_text)
    elif message_text.startswith('/broadcast') and is_owner(chat_id):
        get_broadcast_message(chat_id, message_text)
    elif message_text.startswith('/users') and is_owner(chat_id):
        get_users_message(chat_id)


def get_start_message(chat_id, first_name, last_name, username):
    welcome_message = f"<b>Welcome 🙋{first_name} {last_name}!\nI`m a QRMakerProBot.</b>\n\n" \
                    f"<i>To get help, type /help</i>"
    inline_keyboard = {
        "inline_keyboard": [
            [
                {"text": "Join Channel", "url": "https://t.me/devx_coder"}
            ],
            [
                {"text": "GitHub", "url": "https://github.com/priyanshusingh999"},
                {"text": "Developer", "url": "https://t.me/priyanshusingh999"}
            ]
        ]
    }
    send_message(chat_id, welcome_message, reply_markup=inline_keyboard)

def get_help_message(chat_id):
    help_message = "<b>Available Commands\n\n/qr - use this command to make qrcode\n/users - this command use only owner🔒\n/broadcast - this command use only owner🔒</b>\n\n" \
                  "<i>To get started, type /start</i>"
    send_message(chat_id, help_message)

def get_broadcast_message(chat_id, message_text):
    # Extract actual broadcast message (after /broadcast)
    message_parts = message_text.split(maxsplit=1)
    if len(message_parts) < 2:
        send_message(chat_id, "❌ Please provide a message to broadcast.")
        return

    broadcast_text = message_parts[1].strip()

    # Connect to DB and fetch all chat_ids
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM users")
        user_ids = cursor.fetchall()

    success, failed = 0, 0
    for user in user_ids:
        try:
            send_message(user[0], broadcast_text)
            success += 1
            time.sleep(0.05)  # Safe rate limit for Telegram
        except Exception as e:
            print(f"❌ Failed to send message to {user[0]}: {e}")
            failed += 1

    # Send summary to the sender (owner/admin)
    summary = f"✅ Broadcast completed!\n\nTotal Users: {len(user_ids)}\n✅ Sent: {success}\n❌ Failed: {failed}"
    send_message(chat_id, summary)

def get_users_message(chat_id, db_path='database.db'):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        total_users = len(users)
        send_message(chat_id, f"Total users: {total_users}")
