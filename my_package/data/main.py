# Imports
import sys

sys.path.append("/Users/pratik/Desktop/untitled folder/my_package/")
from model import ImageCaptioningModel
from . import Dataset, Download
from .transforms import FlipImage, RescaleImage, CropImage, RotateImage
from .transforms.blur import BlurImage
import numpy as np
from PIL import Image
import os 

def experiment(annotation_file, captioner, transforms, outputs):
    '''
        Function to perform the desired experiments

        Arguments:
        annotation_file: Path to annotation file
        captioner: The image captioner
        transforms: List of transformation classes
        outputs: Path of the output folder to store the images
    '''
    # Create the instances of the dataset, download
    dataset = Dataset(annotation_file)
    download = Download()

    # Print image names and their captions from annotation file using dataset object
    for idx in range(len(dataset)):
        data = dataset.__getitem__(idx)
        print("Image name:", data['image_id'], "Caption:", data['caption'])

    # Download images to ./data/imgs/ folder using download object
    for idx in range(len(dataset)):
        data = dataset.__getitem__(idx)
        img_path = os.path.join("./data/imgs/", data['image_id'])
        url = data['url']
        download(img_path, url)

    # Transform the required image (roll number mod 10) and save it seperately
    for idx in range(len(dataset)):
        if idx % 10 == 0:
            data = dataset.__getitem__(idx)
            img_path = os.path.join("./data/imgs/", data['image_id'])
            image = Image.open(img_path)
            for transform in transforms:
                image = transform(image)
            if outputs:
                output_path = os.path.join(outputs, f"{idx}_transformed.jpg")
                image.save(output_path)
            else:
                image.show()

    # Get the predictions from the captioner for the above saved transformed image
    for idx in range(len(dataset)):
        if idx % 10 == 0:
            if outputs:
                transformed_path = os.path.join(outputs, f"{idx}_transformed.jpg")
                transformed_image = Image.open(transformed_path)
            else:
                data = dataset.__getitem__(idx)
                img_path = os.path.join("./data/imgs/", data['image_id'])
                transformed_image = Image.open(img_path)
                for transform in transforms:
                    transformed_image = transform(transformed_image)
            caption = captioner(transformed_image)
            print(f"Caption for transformed image {idx}: {caption}")

def main():
    captioner = ImageCaptioningModel()
    transforms = [
        FlipImage(),
        BlurImage(1),
        RescaleImage(2),
        RescaleImage(0.5),
        RotateImage(270),
        RotateImage(45)
    ]
    experiment('.\\annotations.json', captioner, transforms, ".\\data\\imgs") # Sample arguments to call

print("bakchdi nai")
main()