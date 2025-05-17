import qrcode
from qrcode import constants
import os
import tempfile
from connaction import BOT_TOKEN
import requests
from PIL import Image
import qrcode.image.pil
from config import FORCE_JOIN_CHANNEL

def send_photo(chat_id, photo_path, caption=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto'
    with open(photo_path, 'rb') as photo_file:
        files = {'photo': photo_file}
        data = {'chat_id': chat_id}
        if caption:
            data['caption'] = caption
        response = requests.post(url, data=data, files=files)
    return response.json()

def get_qrcode_maker(chat_id, message_text):
    # Extract text after /qr command
    parts = message_text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        from connaction import send_message
        send_message(chat_id, "❌ Please provide text to generate QR code. Usage: /qr your_text_here")
        return

    qr_text = parts[1].strip()

    # Generate QR code with higher version and error correction
    qr = qrcode.QRCode(
        version=4,
        error_correction=constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_text)
    qr.make(fit=True)

    img = qr.make_image(image_factory=qrcode.image.pil.PilImage, fill_color="darkblue", back_color="white").convert('RGB')

    # Try to add logo at the center if logo.png exists
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)

        # Calculate logo size as 25% of the QR code size
        qr_width, qr_height = img.size
        logo_size = int(qr_width * 0.25)
        logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

        # Calculate position to paste the logo
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)

        # Paste the logo into the QR code
        img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)

    # Add watermark text at bottom right corner
    from PIL import ImageDraw, ImageFont

    watermark_text = f"created by {FORCE_JOIN_CHANNEL}"
    draw = ImageDraw.Draw(img)

    # Use a basic font and size
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    margin = 10
    x = img.width - text_width - margin
    y = img.height - text_height - margin

    # Draw watermark with semi-transparent white color
    # Since image is RGB, alpha channel is not supported, so use a light gray color instead
    draw.text((x, y), watermark_text, font=font, fill=(200, 200, 200))

    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        img.save(tmp_file)
        tmp_filename = tmp_file.name

    # Send photo
    send_photo(chat_id, tmp_filename, caption=f"QR Code for: {qr_text}")

    # Remove temporary file
    os.remove(tmp_filename)
