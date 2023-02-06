import jsonlines
from PIL import Image
import urllib.request as rt
import os
import numpy as np

class Dataset(object):
    '''
        A class for the dataset that will return data items as per the given index
    '''

    def __init__(self, annotation_file, transforms=None):
        '''
            Arguments:
            annotation_file: path to the annotation file
            transforms: list of transforms (class instances)
                        For instance, [<class 'RandomCrop'>, <class 'Rotate'>]
        '''
        self.annotation_file = annotation_file
        self.transforms = transforms
        self.dataset = []

        # Read the annotations file and store the data
        with jsonlines.open(annotation_file) as reader:
            for obj in reader:
                self.dataset.append(obj)

    def __len__(self):
        '''
            return the number of data points in the dataset
        '''
        return len(self.dataset)

    def __getitem__(self, idx):
        '''
            return the data items for the index idx as an object
        '''
        obj = self.dataset[idx]

        # Load the image and transform it if required
        rt.urlretrieve(obj["url"], obj["file_name"])
        image = Image.open(obj["file_name"])
        if self.transforms:
            for t in self.transforms:
                image = t(image)

        return {'image': image, 'label': obj['file_name'], 'captions': obj['captions'], 'url': obj["url"]}

    def __transformitem__(self, path):
        '''
            return transformed PIL Image object for the image in the given path
        '''
        image = Image.open(path)
        if self.transforms:
            for t in self.transforms:
                image = t(image)
        return image
