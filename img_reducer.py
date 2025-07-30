from PIL import Image
import os

def resize_image(input_path, output_path, size=(660, 295), max_size_kb=45):
    # Open the image file
    with Image.open(input_path) as img:
        # Resize the image
        img = img.resize(size, Image.ANTIALIAS)

        # Save the image with quality settings to control the file size
        quality = 95  # Start with a high quality
        while True:
            img.save(output_path, format='JPEG', quality=quality)
            # Check the file size
            if os.path.getsize(output_path) <= max_size_kb * 1024 or quality < 10:
                break
            quality -= 5  # Decrease quality in steps until desired file size is reached

path = 'img.jpg'
base_dir = os.path.dirname(path)
prefix = 'resized_'
output_path = os.path.join(base_dir, prefix + os.path.basename(path))
resize_image(path, output_path)