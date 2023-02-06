#Imports
from my_package.model import ImageCaptioningModel
from my_package.data import Dataset, Download
from my_package.data.transforms import FlipImage, RescaleImage, BlurImage, CropImage, RotateImage
import numpy as np
import os
from PIL import Image


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
        print("Image name: " +data['label'], "\nCaption: ", data['captions'])

    # Download images to ./data/imgs/ folder using download object
    for idx in range(len(dataset)):
        data = dataset.__getitem__(idx)
        img_path = os.path.join(outputs, data['label'])
        url = data['url']
        download(img_path, url)

    # Transform the required image (roll number mod 10) and save it seperately
    for _ in range(len(dataset)):
        data = dataset.__getitem__(_)
        img_path = os.path.join(outputs, data['label'])
        image = Image.open(img_path)
        for idx, transform in enumerate(transforms):
            image = transform(image)
            if outputs:
                output_path = os.path.join(outputs, f"{idx}_transformed.jpg")
                image.save(output_path)
            else:
                image.show()

    # Get the predictions from the captioner for the above saved transformed image
    for _ in range(len(dataset)):
        if outputs:
            transformed_path = os.path.join(outputs, f"{_}_transformed.jpg")
            transformed_image = Image.open(transformed_path)
        else:
            data = dataset.__getitem__(_)
            img_path = os.path.join(outputs, data['label'])
            transformed_image = Image.open(img_path)

        for idx, transform in enumerate(transforms):
            transformed_image = transform(transformed_image)
            caption = captioner(transformed_path, len(data["captions"]))
            print(f"Captions for transformed image {idx}: {caption}")

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

main()