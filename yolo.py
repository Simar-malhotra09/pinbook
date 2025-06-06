import os
from ultralytics import YOLO
import torch


def tensor_to_txt(tensor: torch.Tensor, filepath: str):
    with open(filepath, 'w') as f:
        for row in tensor:
            line = ' '.join([f"{v.item():.4f}" for v in row])
            f.write(line + '\n')
    
# Load pretrained model
model = YOLO("yolov8m.pt")

# Create output directory if it doesn't exist
output_dir = "yolo_results"
os.makedirs(output_dir, exist_ok=True)

# Input image
img_path = "./images/book2.jpg"

# Run detection
results = model(img_path)

# Save results
for i, result in enumerate(results):
    # Print optional info
    xyxy = result.boxes.xyxy  # bounding box coordinates
    confs = result.boxes.conf  # confidence scores
    names = [result.names[cls.item()] for cls in result.boxes.cls.int()]
    print(xyxy)

    # Save visualization
    save_image_path = os.path.join(output_dir, f"result_{i}.jpg")
    result.save(filename=save_image_path)

    save_txt_path = os.path.join(output_dir,f"result_{i}.txt")
    tensor_to_txt(xyxy, save_txt_path)

    print(f"Saved image to {save_image_path}")
    print(f"Saved coordinates to {save_txt_path}")
