import os
import yaml
import pandas as pd

# Load config and ground truths
with open("../config.yaml", "r") as f:
    config = yaml.safe_load(f)

csv_path = os.path.expanduser(config["test"]["ground_truths"])
ground_truths = pd.read_csv(csv_path)

# Path to YOLO result txt files
yolo_results_path = os.path.expanduser(config["results"]["yolo"])

# Iterate over YOLO .txt files
for file in os.listdir(yolo_results_path):
    if file.endswith(".txt"):
        txt_path = os.path.join(yolo_results_path, file)

        # Match ground truth rows based on image_name
        image_name = file.replace(".txt", ".jpg")  # or .png, adjust as needed
        matched_gt = ground_truths[ground_truths["image_name"] == image_name]

        # Read YOLO bbox (assuming single line, format: class x_center y_center width height normalized)
        with open(txt_path) as f:
            for line in f:
                yolo_parts = line.strip().split()
                if len(yolo_parts) != 5:
                    continue
                _, x_c, y_c, w, h = map(float, yolo_parts)

                # Optional: convert to corner format if needed
                # Then compare to ground truth
                print(f"\nYOLO result for {image_name}:")
                print(f"Center-based (normalized): x={x_c}, y={y_c}, w={w}, h={h}")
                print("Ground Truth(s):")
                print(matched_gt[["bbox_x", "bbox_y", "bbox_width", "bbox_height"]])
