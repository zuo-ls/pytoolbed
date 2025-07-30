from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math
import random
import numpy as np
import hashlib
import time
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secret key, use default value if environment variable doesn't exist
# DEFAULT_SECRET_KEY = "your-secret-key"  # Only as a backup option
SECRET_KEY = os.getenv('KEY','Your-Secret-Key')
print('>>>>> SECRET_KEY loaded:',SECRET_KEY)

def generate_key(password, salt=None):
    """
    Generate encryption key
    :param password: Password string
    :param salt: Salt value, if not provided, generate new one
    :return: (key, salt)
    """
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_text(text, key):
    """
    Encrypt text
    :param text: Text to encrypt
    :param key: Encryption key
    :return: Encrypted text
    """
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt_text(encrypted_text, key):
    """
    Decrypt text
    :param encrypted_text: Encrypted text
    :param key: Encryption key
    :return: Decrypted text
    """
    f = Fernet(key)
    return f.decrypt(encrypted_text.encode()).decode()

def encode_signature(signature, timestamp=None, password=SECRET_KEY):
    """
    Encode signature information into a special format and encrypt it
    :param signature: Signature text
    :param timestamp: Timestamp, if not provided, use current time
    :param password: Password used to generate encryption key
    :return: Encoded signature
    """
    if timestamp is None:
        timestamp = int(time.time())
    
    # Combine signature and timestamp
    combined = f"{signature}|{timestamp}"
    
    # Generate hash
    hash_obj = hashlib.sha256(combined.encode())
    hash_str = hash_obj.hexdigest()[:12]  # Take first 12 characters as a short code, including time information
    
    # Generate encryption key
    key, salt = generate_key(password)
    
    # Encrypt signature
    encrypted_signature = encrypt_text(signature, key)
    
    # Combine encoding: use "|" as a separator, as it does not appear in Base64 and encrypted text
    salt_b64 = base64.urlsafe_b64encode(salt).decode()
    encoded = f"{hash_str}|{encrypted_signature}|{salt_b64}"
    return encoded, timestamp

def verify_signature(encoded_str, password=SECRET_KEY):
    """
    Verify and decrypt signature
    :param encoded_str: Encoded signature string
    :param password: Password used to generate decryption key
    :return: Decrypted signature
    """
    try:
        # Decompose encoded string
        parts = encoded_str.split('|')
        if len(parts) != 3:
            return "Verification failed: Invalid encoding format"
            
        hash_str, encrypted_sig, salt_b64 = parts
        
        # Restore salt value
        salt = base64.urlsafe_b64decode(salt_b64.encode())
        
        # Regenerate key
        key, _ = generate_key(password, salt)
        
        # Decrypt signature
        decrypted_signature = decrypt_text(encrypted_sig, key)
        return decrypted_signature
    except Exception as e:
        return f"Verification failed: {str(e)}"

def add_noise(image, intensity=10):
    """Add random noise"""
    img_array = np.array(image)
    noise = np.random.normal(0, intensity, img_array.shape)
    noisy_img = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy_img)

def apply_subtle_distortion(image, magnitude=4):
    """Add subtle distortion"""
    width, height = image.size
    x_shift = int(magnitude * math.sin(2 * math.pi * random.random()))
    y_shift = int(magnitude * math.sin(2 * math.pi * random.random()))
    return image.transform(image.size, Image.AFFINE, 
                         (1, 0, x_shift, 0, 1, y_shift))

def get_loc(img,loc,text_width,text_height):
    if loc == "bottom_right":
        x = img.width - text_width - 20
        y = img.height - text_height - 20
        return x, y, 0
    elif loc == "top_left":
        x = 20
        y = 20
        return x, y, 0
    elif loc == "top_right":
        x = img.width - text_width - 20
        y = 20
        return x, y, 0
    elif loc == "bottom_left":
        x = 20
        y = img.height - text_height - 20
        return x, y, 0
    elif loc == "cover":
        # Calculate diagonal angle
        angle = math.degrees(math.atan2(img.height, img.width))
        # Place text in the center of the image
        x = (img.width - text_width) // 2
        y = (img.height - text_height) // 2
        return x, y, angle

def wrap_text(text, max_width, font, draw):
    """
    Wrap long text to multiple lines
    :param text: Text to wrap
    :param max_width: Maximum width (pixels)
    :param font: Font
    :param draw: ImageDraw object
    :return: List of wrapped text lines
    """
    # Maximum characters per line (set based on empirical value)
    chars_per_line = 50
    
    # If text length is less than maximum characters per line, return directly
    if len(text) <= chars_per_line:
        return [text]
    
    # Split text into fixed lengths
    lines = []
    for i in range(0, len(text), chars_per_line):
        line = text[i:i + chars_per_line]
        lines.append(line)
    
    return lines

def save_watermark_log(input_path, output_path, watermark_text, signature, encoded_sig, timestamp, loc):
    """
    Save watermark processing log
    """
    import json
    import datetime
    
    log_file = "watermark_log.json"
    
    # Create log entry
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "input_file": input_path,
        "output_file": output_path,
        "watermark_text": watermark_text,
        "signature": signature,
        "encoded_signature": encoded_sig,
        "process_timestamp": timestamp,
        "location": loc
    }
    
    try:
        # Read existing logs
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                if not isinstance(logs, list):
                    logs = []
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
        
        # Add new log
        logs.append(log_entry)
        
        # Save log
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=4)
            
        print(f"Log saved to: {log_file}")
    except Exception as e:
        print(f"Error saving log: {str(e)}")

def process_id_card(input_path, output_path, watermark_text, degree=1.5, loc="bottom_right", layer_num=3, signature=None, size=0.03, alpha_range=(64, 128)):
    """
    Process ID card image: add enhanced watermark, noise, and distortion effects to make it harder for AI to modify
    :param input_path: Input image path
    :param output_path: Output image path
    :param watermark_text: Watermark text
    :param degree: Blur degree
    :param loc: Watermark position, optional values are "bottom_right", "top_left", "top_right", "bottom_left","cover"
    :param layer_num: Number of watermark layers
    :param signature: Custom signature, if provided, will be encoded into the watermark
    :param size: Watermark text size ratio
    :param alpha_range: Watermark transparency range, format is (minimum value, maximum value), value range 0-255
    """
    try:
        # Generate encoded signature
        encoded_sig = None
        timestamp = None
        if signature:
            encoded_sig, timestamp = encode_signature(signature, password=SECRET_KEY)
        
        # Open image
        img = Image.open(input_path)
        
        # Convert to RGBA mode
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Create a copy for processing
        watermarked = img.copy()
        
        # Add blur effect (moderate blur to maintain some readability)
        blurred = watermarked.filter(ImageFilter.GaussianBlur(radius=degree))
        
        # Add random noise
        blurred = add_noise(blurred, intensity=5)
        
        # Add subtle distortion
        blurred = apply_subtle_distortion(blurred)
        
        # First, add watermark text in cover mode
        txt_layers = []
        for i in range(layer_num):
            txt_layer = Image.new('RGBA', blurred.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            txt_layers.append((txt_layer, draw))
        
        # Calculate watermark text font size
        font_size = int(min(img.size) * (size*1.5))
        
        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", font_size)
            if signature:  # Signature text uses a smaller font
                sig_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", int(font_size * 0.3))
        except:
            font = ImageFont.load_default()
            sig_font = font
        
        # Get watermark text size
        bbox = ImageDraw.Draw(blurred).textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate watermark text position and angle (always use cover mode)
        x, y, angle = get_loc(img, "cover", text_width, text_height)
        
        # Add watermark text in cover mode
        for i, (txt_layer, draw) in enumerate(txt_layers):
            # Draw watermark slightly offset on each layer
            offset_x = x + random.randint(-10, 10)
            offset_y = y + random.randint(-10, 10)
            offset_angle = angle + random.randint(-5, 5)
            
            # Use different transparency
            alpha = random.randint(alpha_range[0], alpha_range[1])
            
            # Draw watermark text
            draw.text((offset_x, offset_y), watermark_text, font=font, fill=(255, 0, 0, alpha))
            
            txt_layer = txt_layer.rotate(offset_angle, expand=True)
            txt_layer = txt_layer.resize(blurred.size)
            
            if blurred.mode != 'RGBA':
                blurred = blurred.convert('RGBA')
            blurred = Image.alpha_composite(blurred, txt_layer)
        
        # If there is a signature, add encoded information (using the original method)
        if signature:
            # Create a new transparent layer for encoded information
            txt_layer = Image.new('RGBA', blurred.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(txt_layer)
            
            # Calculate maximum width of encoded text (80% of image width)
            max_encoded_width = int(img.width * 0.8)
            
            # Prepare encoded text
            encoded_text = "Signature Code:"
            encoded_lines = wrap_text(encoded_sig, max_encoded_width, sig_font, draw)
            all_lines = [encoded_text] + encoded_lines
            
            # Calculate total height and line height
            line_heights = []
            total_height = 0
            for line in all_lines:
                bbox = draw.textbbox((0, 0), line, font=sig_font)
                height = bbox[3] - bbox[1]
                line_heights.append(height)
                total_height += height
            
            # Add line spacing
            line_spacing = int(font_size * 0.2)
            total_height += line_spacing * (len(all_lines) - 1)
            
            # Calculate encoded text position (using the specified loc parameter)
            x, y, _ = get_loc(img, loc, max_encoded_width, total_height)
            
            # Draw encoded text
            current_y = y
            for i, line in enumerate(all_lines):
                alpha = random.randint(alpha_range[0], alpha_range[1])
                if i == 0:  # "Signature Code:" title
                    color = (0, 0, 255, alpha)  # Blue
                else:  # Encoded content
                    color = (0, 0, 255, int(alpha * 0.8))  # Slightly lighter blue
                
                draw.text((x, current_y), line, font=sig_font, fill=color)
                current_y += line_heights[i] + line_spacing
            
            if blurred.mode != 'RGBA':
                blurred = blurred.convert('RGBA')
            blurred = Image.alpha_composite(blurred, txt_layer)
        
        # Convert back to RGB mode and save
        blurred = blurred.convert('RGB')
        
        # Save processed image
        blurred.save(output_path, quality=95)  # Use higher quality setting
        print(f"Image processing completed, saved to: {output_path}")
        
        # Save processing log
        if signature:
            save_watermark_log(input_path, output_path, watermark_text, signature, encoded_sig, timestamp, loc)
            
        return encoded_sig, timestamp
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None, None

# Example usage
pth = "sample.jpg"
out = os.path.splitext(pth)[0] + "_output.jpeg" # Output path
blur_degree = 3.5 # Blur degree
loc = "bottom_right" # Watermark position
watermark_text = "本文件仅租房子用的" # Watermark text
signature = "Lis-Valid:250801to250831" # Add signature
size = 0.05  # Font size ratio (relative to image's minimum edge length, e.g., 0.03 means 3%)
alpha_range = (80, 120)  # Transparency range, lower value means more transparent

# Process image
process_id_card(pth, out, watermark_text, blur_degree, loc, layer_num=3, signature=signature, size=size, alpha_range=alpha_range)

# Verify signature
print("\nVerify signature:")
encoded_sig, timestamp = encode_signature(signature, password=SECRET_KEY)  # Use key from environment variable
decrypted = verify_signature(encoded_sig, SECRET_KEY)  # Use key from environment variable
print(f"Encoded: {encoded_sig}")
print(f"Decrypted signature: {decrypted}")
print(f"Timestamp: {timestamp}")


