from PIL import Image

class RotateImage(object):
    '''
        Rotates the image about the center of the image.
    '''

    def __init__(self, degrees):
        '''
            Arguments:
            degrees: rotation degree.
        '''
        self.degrees = degrees

    def __call__(self, image):
        '''
            Arguments:
            image (PIL Image)

            Returns:
            image (PIL Image)
        '''
        return image.rotate(self.degrees)
