import cv2
import pytesseract
import numpy as np

# Load image
image_path = "./images/book2.jpg"
image = cv2.imread(image_path)

# Text boxes already within object bbox
text_boxes_within_objects = [
    [(196, 427), (254, 427), (254, 442), (196, 442)],
    [(194, 441), (277, 441), (277, 456), (194, 456)],
    [(194, 453), (248, 453), (248, 470), (194, 470)],
    [(246, 453), (320, 453), (320, 470), (246, 470)],
    [(194, 468), (275, 468), (275, 483), (194, 483)],
    [(192, 482), (254, 482), (254, 497), (192, 497)]
]

# Function to extract text from a single 4-point box
def extract_text_from_box(image, box, idx=None):
    pts = np.array(box, dtype="float32")

    # Compute width and height of the cropped region
    width = int(max(np.linalg.norm(pts[0] - pts[1]), np.linalg.norm(pts[2] - pts[3])))
    height = int(max(np.linalg.norm(pts[0] - pts[3]), np.linalg.norm(pts[1] - pts[2])))

    dst = np.array([
        [0, 0],
        [width - 1, 0],
        [width - 1, height - 1],
        [0, height - 1]
    ], dtype="float32")

    # Perspective transform
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (width, height))

    # Use Tesseract
    config = "--psm 7"  # Assume a single line of text
    text = pytesseract.image_to_string(warped, config=config)

    if idx is not None:
        print(f"[Text #{idx}]: {text.strip()}")

    return text.strip()

# Extract text from all boxes
for i, box in enumerate(text_boxes_within_objects):
    extract_text_from_box(image, box, idx=i+1)
