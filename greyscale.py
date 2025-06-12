import yaml
import os
import cv2

# Load configs
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Get src and target paths for images
src_imgs_path = os.path.expanduser(config["inference"]["test_folder"])
trgt_imgs_path = os.path.expanduser(config["inference"]["test_folder_greyscale"])

# Make sure target folder exists
os.makedirs(trgt_imgs_path, exist_ok=True)

# Loop over images
for (_, _, img_list) in os.walk(src_imgs_path):
    for img in img_list:
        if img.endswith(".jpg") or img.endswith(".png"):
            img_path = os.path.join(src_imgs_path, img)
            image = cv2.imread(img_path)

            if image is None:
                print(f"Failed to read image: {img_path}")
                continue

            gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Save greyscale image to target path
            save_path = os.path.join(trgt_imgs_path, img)
            cv2.imwrite(save_path, gray_img)
            print(f"Saved: {save_path}")
