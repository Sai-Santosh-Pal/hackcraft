from PIL import Image, ImageOps
import os

# Directory containing block icons
ICON_DIR = 'block_icons'
# Output directory for processed icons
OUTPUT_DIR = 'block_icons_with_bg'
# Padding in pixels
PADDING = 8
# Background color (white)
BG_COLOR = (255, 255, 255, 255)

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(ICON_DIR):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        path = os.path.join(ICON_DIR, filename)
        img = Image.open(path).convert('RGBA')
        # Add padding
        padded_img = ImageOps.expand(img, border=PADDING, fill=BG_COLOR)
        # Save to output directory
        out_path = os.path.join(OUTPUT_DIR, filename)
        padded_img.save(out_path)
        print(f'Processed: {filename}')

print('All icons processed!')
