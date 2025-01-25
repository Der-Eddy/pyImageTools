import os
import sys
import platform
from collections import defaultdict
from tkinter import filedialog
from PIL import Image
import imagehash
import progressbar
import time

class DuplicateFinder:
    def __init__(self, path):
        self.start_time = time.time()
        self.path = path
        self.duplicates = self.find_duplicates()
        self.delete_duplicates(self.duplicates)
        self.print_summary()
        self.halt_windows()

    def find_duplicates(self):
        """Find duplicate images in the given directory"""
        file_array = []
        widgets = [
            'Getting images: [', progressbar.SimpleProgress(), '] ',
            progressbar.Bar(),
            ' (', progressbar.Timer(), ') '
        ]

        for image in progressbar.progressbar(os.scandir(self.path), widgets=widgets, max_value=len(os.listdir(self.path))):
            if image.path.endswith(('.png', '.jpg', '.jpeg')):
                hash = imagehash.average_hash(Image.open(image.path))
                file_array.append((image, hash))

        # Group by hash and check for duplicates
        hash_to_images = defaultdict(list)
        for image, hash in file_array:
            hash_to_images[hash].append((image, os.stat(image.path).st_size))

        duplicates = []
        for images in hash_to_images.values():
            if len(images) > 1:  # Check if there are any duplicates
                duplicates.append(images)

        return duplicates

    def delete_duplicates(self, duplicates):
        """Delete duplicate images"""
        self.counter = 0
        self.counter_filesize = 0

        for images in duplicates:
            images.sort(key=lambda lst: lst[1])  # Sort by file size
            del images[-1]  # Remove the largest image
            for file in images:
                try:
                    self.counter_filesize += os.stat(file[0].path).st_size
                    os.remove(file[0].path)
                    self.counter += 1
                except FileNotFoundError:
                    pass

    def print_summary(self):
        """Print summary of deleted duplicates"""
        end_time = time.time()
        elapsed_time = round(end_time - self.start_time, 2)
        if self.counter > 0:
            print(f'Deleted {self.counter} duplicates (Saved {round(self.counter_filesize / 1024 / 1024, 2)} MB)')
        else:
            print('No duplicates found!')
        print(f'Runtime {elapsed_time} seconds')

    @staticmethod
    def halt_windows():
        """Halt console on Windows"""
        if platform.system() == 'Windows':
            os.system('pause')


if __name__ == '__main__':
    try:
        path = sys.argv[1]
    except IndexError:
        path = filedialog.askdirectory()

    DuplicateFinder(path)
