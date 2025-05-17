# QR Code Maker with Telegram Bot

This project allows you to generate customized QR codes via a Telegram bot. The bot generates QR codes with enhanced features such as higher error correction, logo embedding, and watermarking, and sends the QR code images directly to Telegram chats.

## Features

- Generate QR codes from text commands sent to the Telegram bot.
- QR codes have higher error correction for better resilience.
- Customizable QR code colors.
- Optional logo embedding at the center of the QR code.
- Watermark text added to the QR code image.
- Sends QR code images directly to Telegram chats.

## Installation

1. Clone the repository.

2. Install the required Python packages:

```bash
pip install -r requirements.txt
```

3. Set up your Telegram bot token in the `connaction.py` file.

## Usage

Send a message to your Telegram bot with the command:

```
/qr your_text_here
```

The bot will generate a QR code for the provided text and send it back as an image.

## Dependencies

- qrcode
- requests
- Pillow

## License

This project is licensed under the MIT License.
