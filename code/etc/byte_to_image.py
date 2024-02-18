from PIL import Image
import numpy as np
import math
import os

SRC_PATH = 'APT_unzip_pe'
DST_PATH = 'APT_Image'

def to_image(file, dst_file):
    try:
        with open(file, 'rb') as f:
            byte_data = f.read()
            image_size = math.ceil(math.sqrt(len(byte_data)))

            padded_data = byte_data + b'\x00' * (image_size**2 - len(byte_data))
            image_data = np.reshape(np.frombuffer(padded_data, dtype=np.uint8), (image_size, image_size))
            
            # Gray Scale
            image = Image.fromarray(image_data, 'L')
            # RGB
            # image = Image.fromarray(image_data, 'RGB')
            image.save(dst_file, 'PNG')
    except Exception as e:
        print(f"Error processing {file}: {e}")

def start():
    for i in os.listdir(SRC_PATH):
        family_path = os.path.join(SRC_PATH, i)
        family_image_dir = os.path.join(DST_PATH, i)

        os.makedirs(family_image_dir, exist_ok=True)

        for k in os.listdir(family_path):
            sample_path = os.path.join(family_path, k)
            save_image_path = os.path.join(family_image_dir, f"{k}.png")
            to_image(sample_path, save_image_path)

# Test
if __name__ == "__main__":
    start()
