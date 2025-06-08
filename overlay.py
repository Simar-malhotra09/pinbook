import cv2
import numpy as np
import os

CRAFT_RESULTS = "./result/res_book2.txt"
YOLO_IMAGE_RESULTS = "./yolo_results/result_0.jpg"
YOLO_TXT_RESULTS = "./yolo_results/result_0.txt"
OUTPUT_DIR = "./results/overlay_results"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "book2.jpg")

# Make sure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load YOLO image
image = cv2.imread(YOLO_IMAGE_RESULTS)

# Load YOLO boxes: assume format is `class x1 y1 x2 y2`
yolo_boxes = []
with open(YOLO_TXT_RESULTS, 'r') as f:
    for line in f:
        # print(line)
        parts = line.strip().split(',')
        # print(parts)
        if len(parts)==4:
            x1, y1, x2, y2 = map(float, parts)
            yolo_boxes.append((x1, y1, x2, y2))

print(f" yolo_boxes {yolo_boxes}")

# Helper: check if all points are inside any YOLO box
def is_within_yolo_box(text_points, yolo_boxes, tolerance=3):
    for (x1, y1, x2, y2) in yolo_boxes:
        x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])  # convert YOLO float to int for comparison
        inside = all(
            (x1 - tolerance <= x <= x2 + tolerance) and
            (y1 - tolerance <= y <= y2 + tolerance)
            for (x, y) in text_points
        )
        if inside:
            return True
    return False

# Parse and draw only valid CRAFT boxes
bbox_within=[]
with open(CRAFT_RESULTS, 'r') as f:
    for line in f.readlines():
        pts = [int(pt) for pt in line.strip().split(',')]
        if len(pts) == 8:
            points = [(pts[i], pts[i + 1]) for i in range(0, 8, 2)]  # 4 (x, y) pairs
            print(f"Object bbox: {yolo_boxes}")
            print(f"Text bbox: {points}")
            if is_within_yolo_box(points, yolo_boxes):
                print("Within")
                bbox_within.append(points)
                coords = np.array(points, np.int32).reshape((-1, 1, 2))
                cv2.polylines(image, [coords], isClosed=True, color=(0, 255, 0), thickness=2)
            else:
                print("Not within")
# Save the result
cv2.imwrite(OUTPUT_PATH, image)
print(f"Overlay saved to: {OUTPUT_PATH}")

print(f"text within objects: \n {bbox_within}")
