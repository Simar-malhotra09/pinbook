import os
import yaml
import pandas as pd 

# Load config to get the path to the groud_truths dir
with open("../config.yaml", 'r') as f:
    config = yaml.safe_load(f)

csv_path = os.path.expanduser(config["test"]["ground_truths"])
ground_truths_df = pd.read_csv(csv_path)

# The csv has an individual row for each object, we want to first collect all objects for each image, 
# and then write to a file
file_names = ground_truths_df["image_name"].unique()

output_dir = os.path.dirname(csv_path)

for file in file_names:
    objects = ground_truths_df[ground_truths_df["image_name"] == file]

    with open(os.path.join(output_dir, f"{file.replace('.png', '').replace('.jpg', '')}.txt"), 'w') as f:
        for _, row in objects.iterrows():
            line = f"{float(row['bbox_x'])} {float(row['bbox_y'])} {float(row['bbox_width'])} {float(row['bbox_height'])}\n"
            f.write(line)
