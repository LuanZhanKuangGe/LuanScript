import os.path
import shutil
import tkinter as tk
from tkinter import filedialog

import cv2

root = tk.Tk()
root.withdraw()
root_dir = filedialog.askdirectory()

for parent, dir_names, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith(".avi") or filename.endswith(".mp4") or filename.endswith(".mkv") or filename.endswith(
                ".wmv"):
            old_name_1 = parent + "/" + filename
            new_name_1 = old_name_1

            if old_name_1.find("/HD/") == -1:
                cap = cv2.VideoCapture(old_name_1)
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cap.release()
                if height >= 720:
                    new_name_1 = parent + "/HD/" + filename
                else:
                    new_name_1 = parent + "/SD/" + filename
                ex = os.path.splitext(old_name_1)[1]
                old_name_2 = old_name_1.replace(ex, ".nfo")
                new_name_2 = new_name_1.replace(ex, ".nfo")
                old_name_3 = old_name_1.replace(ex, "-fanart.jpg")
                new_name_3 = new_name_1.replace(ex, "-fanart.jpg")
                old_name_4 = old_name_1.replace(ex, "-poster.jpg")
                new_name_4 = new_name_1.replace(ex, "-poster.jpg")
                if height >= 720:
                    if not os.path.exists(parent + "/HD"):
                        os.mkdir(parent + "/HD")
                else:
                    if not os.path.exists(parent + "/SD"):
                        os.mkdir(parent + "/SD")
                shutil.move(old_name_1, new_name_1)
                shutil.move(old_name_2, new_name_2)
                shutil.move(old_name_3, new_name_3)
                shutil.move(old_name_4, new_name_4)
