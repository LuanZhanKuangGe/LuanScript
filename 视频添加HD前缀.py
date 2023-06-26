import os.path
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog
from pathlib import Path

import cv2

root = tk.Tk()
root.withdraw()
root_dir = filedialog.askdirectory() + r"//"

for item in os.listdir(root_dir):
    folder = Path(root_dir) / item
    if folder.is_dir():
        for video in folder.iterdir():
            if video.suffix in ['.avi', '.mp4', '.mkv', 'wmv']:
                tag = '[SD]'
                cap = cv2.VideoCapture(str(video))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cap.release()
                if height >= 720:
                    tag = '[HD]'
                # print(video, tag)
                for old_file in folder.iterdir():
                    if old_file.name.split(' ')[0] == video.name.split(' ')[0]:
                        new_file = folder / (tag  + old_file.name)
                        print(old_file, new_file)
                        shutil.move(old_file, new_file)

