import requests, time, json
from config import BOT_TOKEN

# Function to get updates
def get_updates(offset=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params=params)
    return response.json()

# Function to send a message
def send_message(chat_id, text, parse_mode='HTML', reply_markup=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode,}
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    requests.post(url, data=payload)

def get_chat_member(chat_id, user_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember'
    params = {'chat_id': chat_id, 'user_id': user_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def send_photo(chat_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    payload = {'chat_id': chat_id}
    response = requests.post(url, data=payload)