import os
from PIL import Image
import json

img_dir = "./"
metadata = {}

for fname in os.listdir(img_dir):
    if fname.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(img_dir, fname)
        with Image.open(path) as img:
            width, height = img.size
        metadata[fname] = {"width": width, "height": height}

with open("metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

