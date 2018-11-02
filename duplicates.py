import os
import sys
import platform
from tkinter import filedialog
from PIL import Image
import imagehash
import progressbar

class Duplicates:
    counter = 0
    counterFilesize = 0

    def __init__(self, path):
        self.path = path
        self.duplicates = self.getImages()
        self.deleteDuplicates(self.duplicates)
        if self.counter > 0:
            self.counterFilesize = round(self.counterFilesize / 1024 / 1024, 2)
            print(f'Found {self.counter} duplicates and deleted them (Saved {self.counterFilesize} MB)')
        else:
            print('Couldn\'t find any duplicates!')
        self.haltWindows()

    def getImages(self):
        fileArray = []
        duplicates = []

        widgets=[
            'Getting images: [', progressbar.SimpleProgress(), '] ',
            progressbar.Bar(),
            ' (', progressbar.Timer(), ') ',
        ]

        for image in progressbar.progressbar(os.scandir(self.path), widgets=widgets, max_value=len(os.listdir(self.path))):
            if image.path.endswith('Thumbs.db'):
                # Ignore Thumbs.db
                continue
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
            duplicate.pop()
            for file in duplicate:
                try:
                    self.counterFilesize += os.stat(file[0].path).st_size
                    os.remove(file[0].path)
                    self.counter += 1
                except FileNotFoundError:
                    pass

    def haltWindows(self):
        if platform.system() == 'Windows':
            os.system('pause')


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        path = filedialog.askdirectory()

    images = Duplicates(path)