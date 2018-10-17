import os
import sys
from tkinter import filedialog
from PIL import Image
import imagehash

class Duplicates:
    counter = 0

    def __init__(self, path):
        self.path = path
        self.duplicates = self.getImages()
        self.deleteDuplicates(self.duplicates)
        if self.counter > 0:
            print(f'Found {self.counter} duplicates and deleted them')
        else:
            print('Couldn\'t find any duplicates!')

    def getImages(self):
        fileArray = []
        duplicates = []

        for image in os.scandir(self.path):
            hash = imagehash.average_hash(Image.open(image.path))
            fileArray.append((image, hash))

        for image1 in fileArray:
            duplicate = []
            for image2 in fileArray:
                if image1[1] - image2[1] == 0:
                    duplicate.append((image2[0], os.stat(image2[0].path).st_size))
            if len(duplicate) > 1:
                duplicates.append(duplicate)

        return duplicates

    def deleteDuplicates(self, imageArray):
        for duplicate in imageArray:
            duplicate.sort(key=lambda lst: lst[1]) # Sort by file size
            dontDelete = duplicate.pop()
            for file in duplicate:
                try:
                    os.remove(file[0].path)
                    self.counter += 1
                except FileNotFoundError:
                    pass


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        path = filedialog.askdirectory()

    images = Duplicates(path)