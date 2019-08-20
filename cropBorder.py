import os
from PIL import Image, ImageChops

class cropBorder:
    fileArray = []

    def __init__(self, path):
        self.path = path
        self.getImages()
        print('Found {} images to crop'.format(len(self.fileArray)))
        self.trim()
        print('Done!')

    def getImages(self):
        for image in os.scandir(self.path):
            if image.path.endswith('.png') or image.path.endswith('.jpg') or image.path.endswith('.jpeg'):
                self.fileArray.append(image.path)
            
    def trim(self):
        for image in self.fileArray:
            print(image)
            with Image.open(image) as img:
                background = Image.new(img.mode, img.size, img.getpixel((0,0)))
                diff = ImageChops.difference(img, background)
                diff = ImageChops.add(diff, diff, 2.0, -100)
                bbox = diff.getbbox()
                if bbox:
                    img.crop(bbox).save(image)

if __name__ == '__main__':
    path = '/home/eddy/Dev/Python/pyImageTools/'
    cropBorder(path)