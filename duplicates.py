import os
import sys
import platform
from collections import defaultdict
from tkinter import filedialog
from PIL import Image
import imagehash
import progressbar
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue

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

        # Scan for image files
        image_files = [image.path for image in os.scandir(self.path) if image.path.endswith(('.png', '.jpg', '.jpeg'))]

        # Initialize progress bar
        pbar = progressbar.ProgressBar(max_value=len(image_files), widgets=widgets)

        # Queue to communicate between threads
        self.task_queue = queue.Queue()
        for img in image_files:
            self.task_queue.put(img)

        with ThreadPoolExecutor() as executor:
            futures_to_image = {executor.submit(self.hash_image, img): img for img in image_files}

            for future in as_completed(futures_to_image):
                hash, image_path = future.result()
                file_array.append((image_path, hash))
                self.task_queue.get()  # Mark task as completed
                pbar.update(len(image_files) - self.task_queue.qsize())

        # Group by hash and check for duplicates
        hash_to_images = defaultdict(list)
        for image_path, hash in file_array:
            hash_to_images[hash].append((image_path, os.stat(image_path).st_size))

        duplicates = []
        for images in hash_to_images.values():
            if len(images) > 1:  # Check if there are any duplicates
                duplicates.append(images)

        return duplicates

    def hash_image(self, image_path):
        """Compute the average hash of an image"""
        with Image.open(image_path) as img:
            hash = imagehash.average_hash(img)
        return hash, image_path

    def delete_duplicates(self, duplicates):
        """Delete duplicate images"""
        self.counter = 0
        self.counter_filesize = 0

        for images in duplicates:
            images.sort(key=lambda lst: lst[1])  # Sort by file size
            del images[-1]  # Remove the largest image
            for file_path, _ in images:
                try:
                    self.counter_filesize += os.stat(file_path).st_size
                    os.remove(file_path)
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
