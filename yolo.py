'''
Infrence yolov8m for object detection and segmentation to 
help seperate text inside the object and outside. 

This is done keeping in mind that the use case for this right now
is to extract author/book title of books placed in a 2d plane in the image,
ie a top view of a book on a desk or a frontal view of a book held vertically.

We need to account for rotational assymetry and text that is overlayed on 
the book surface for example captions in a social media post. 

'''
import os
from ultralytics import YOLO
import torch
import argparse
from file_utils import get_files

'''
Convert coordinates in the form of a tensor to txt to log.
These are in fact what is used to segregate text.
'''

class Yolo:

    def __init__(self, test_folder: str):
        self.model = YOLO("yolov8m.pt")
        self.test_folder = test_folder
        self.output_dir = "./results/yolo_results"
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def tensor_to_txt(tensor: torch.Tensor, filepath: str):
        with open(filepath, 'w') as f:
            for row in tensor:
                line = ' '.join([f"{v.item():.4f}" for v in row])
                f.write(line + '\n')

    def run(self):
        # Load input images
        image_list, _, _ = get_files(self.test_folder)
        # Inference
        _results = []
        for image_path in image_list:
            assert image_path.lower().endswith(('.png', '.jpg', '.jpeg')), \
    f"Invalid image format for file: {image_path}. Only PNG, JPG, and JPEG are allowed."
            result = self.model(image_path)  
            _results.append((os.path.basename(image_path), result))


        for filename, result in _results:
            base_name = os.path.splitext(filename)[0]  # remove extension for naming outputs


            # Get bounding boxes
            xyxy = result[0].boxes.xyxy
            class_names = [result[0].names[cls.item()] for cls in result[0].boxes.cls.int()]

            print(xyxy)

            # Save image
            save_image_path = os.path.join(self.output_dir, f"yolo_{base_name}.jpg")
            result[0].save(filename=save_image_path)

            # Save bounding box coordinates as text
            save_txt_path = os.path.join(self.output_dir, f"yolo_{base_name}.txt")
            self.tensor_to_txt(xyxy, save_txt_path)

            print(f"Saved image to {save_image_path}")
            print(f"Saved coordinates to {save_txt_path}")





if __name__ =='__main__':    
    parser = argparse.ArgumentParser(description='Object Detection & Segmentation with YOLO')
    parser.add_argument('--test_folder', default='./results/craft_results/', type=str, help='folder path to input images')
    args= parser.parse_args()

    yolo= Yolo(args.test_folder)
    yolo.run()




