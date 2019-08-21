import os.path
import argparse
from tkinter import filedialog
from duplicates import Duplicates
from cropBorder import CropBorder

parser = argparse.ArgumentParser(description='Provides several tools to manage folders of images')

availablePrograms = ['dupe', 'exactdupe', 'cropborder']
availableProgramsStr = ', '.join(availablePrograms)
parser.add_argument('program', type=str,
                    help=f'Specific tool you want to run (Default: dupe)\nAvailable programs: {availableProgramsStr}',
                    default='dupe')

parser.add_argument('path', type=str,
                    help='Path of an image folder to test (Default: . / the path you are currently in)',
                    default='.')

args = parser.parse_args()
if not os.path.exists(args.path):
    path = filedialog.askdirectory()
    if os.path.exists(path):
        raise Exception('Please specify a valid path')
else:
    path = args.path

if not args.program.lower() in availablePrograms:
    raise Exception(f'Please specify a correct program ({availableProgramsStr})')

#print(args)
parser.print_help()

if args.program.lower() == 'dupe':
    #images = Duplicates(path)
    pass
elif args.program.lower() == 'cropborder':
    CropBorder(path)