import os
import os.path
import cv2
import numpy as np
import zipfile
import shutil

import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm

root = tk.Tk()
root.withdraw()
rootdir = filedialog.askdirectory()

print(rootdir)

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), -1)
    return cv_img

def cv_imwrite(path,img):
    suffix = os.path.splitext(path)[-1]
    cv2.imencode(suffix, img)[1].tofile(path)


print("unzip start!!!")
for root,dirs,files in os.walk(rootdir):
    for file in tqdm(files):
        name = os.path.splitext(file)[0]
        name = name.replace("(成年コミック) ","")
        name = name.replace(" [DL版]","")
        if name[0] == '(':
            name = name.split(') ', 1)[1]
        if name[-1] == ' ':
            name = name[:-1]
        end = os.path.splitext(file)[-1]
        if end=='.zip':
            name = os.path.join(rootdir,name)
            file = os.path.join(rootdir,file)
            os.makedirs(name)
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(name)

print("unzip stop!!!")

print("resize start!!!")
for root,dirs,files in os.walk(rootdir):
    print(root)
    for file in tqdm(files):
        end = os.path.splitext(file)[-1]
        if end=='.jpg' or end=='.png':
            name = os.path.join(root,file)
            name = name.replace('\\', '/')
            img = cv_imread(name)
            size = 0.0
            if img.shape[0]>img.shape[1]:
                size = 780/img.shape[1]
            else:
                size = 780/img.shape[0]
            img = cv2.resize(img, None, fx=size, fy=size)
            name = name.replace('.png', '.jpg')
            cv_imwrite(name,img)

print("resize stop!!!")

cmddir = rootdir.replace("/","\\")
print("del start!!!")
os.system("del /S " + cmddir +  "\\*.png")
os.system("del /S " + cmddir +  "\\*.zip")
print("del stop!!!")

print("zip start!!!")

for root,dirs,files in os.walk(rootdir):
    for dir in tqdm(dirs):
        name = os.path.join(root, dir)
        shutil.make_archive(name, 'zip', name)
        shutil.rmtree(name)

print("zip stop!!!")