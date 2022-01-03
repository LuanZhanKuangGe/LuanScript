import os
import os.path
import cv2
import shutil
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm

root = tk.Tk()
root.withdraw()
rootdir = filedialog.askdirectory()

for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:
        if filename.endswith(".avi") or filename.endswith(".mp4") or filename.endswith(".mkv") or filename.endswith(".wmv"):
            oldname = parent +  "/" + filename
            newname = oldname

            if oldname.find("/HD/") == -1:
                cap = cv2.VideoCapture(oldname)
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cap.release()
                if height >= 720:
                    newname = parent +  "/HD/" + filename
                else:
                    newname = parent +  "/SD/" + filename
                # print(oldname)
                # print(newname)
                ex = os.path.splitext(oldname)[1]
                oldname2 = oldname.replace(ex, ".nfo")
                newname2 = newname.replace(ex, ".nfo")
                oldname3 = oldname.replace(ex, "-fanart.jpg")
                newname3 = newname.replace(ex, "-fanart.jpg")
                oldname4 = oldname.replace(ex, "-poster.jpg")
                newname4 = newname.replace(ex, "-poster.jpg")
                if height >= 720:
                    if not os.path.exists(parent+"/HD"):
                        os.mkdir(parent+"/HD")
                else:
                    if not os.path.exists(parent+"/SD"):
                        os.mkdir(parent+"/SD")
                shutil.move(oldname, newname)
                shutil.move(oldname2, newname2)
                shutil.move(oldname3, newname3)
                shutil.move(oldname4, newname4)