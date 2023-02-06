#Imports
from PIL import Image
import random

class CropImage(object):
    '''
        Performs either random cropping or center cropping.
    '''

    def __init__(self, shape, crop_type='center'):
        '''
            Arguments:
            shape: output shape of the crop (h, w)
            crop_type: center crop or random crop. Default: center
        '''
        self.shape = shape
        self.crop_type = crop_type

    def __call__(self, image):
        '''
            Arguments:
            image (numpy array or PIL image)

            Returns:
            image (numpy array or PIL image)
        '''
        if isinstance(image, Image.Image):
            image_width, image_height = image.size
            target_width, target_height = self.shape

            if self.crop_type == 'center':
                left = (image_width - target_width) / 2
                top = (image_height - target_height) / 2
                right = (image_width + target_width) / 2
                bottom = (image_height + target_height) / 2
            elif self.crop_type == 'random':
                left = random.randint(0, image_width - target_width)
                top = random.randint(0, image_height - target_height)
                right = left + target_width
                bottom = top + target_height
            else:
                raise ValueError("Invalid crop_type. Choose 'center' or 'random'.")

            return image.crop((left, top, right, bottom))
        else:
            raise ValueError("Input must be a PIL Image.")
