import os

# BOT_TOKEN = ''
# OWNER_ID = 
# FORCE_JOIN_CHANNEL = ''  # Add the channel username or ID here

BOT_TOKEN = os.getenv('BOT_TOKEN')
OWNER_ID = int(os.getenv("OWNER_ID", ""))  # Default to 0 if not set
FORCE_JOIN_CHANNEL = os.getenv('FORCE_JOIN_CHANNEL')
