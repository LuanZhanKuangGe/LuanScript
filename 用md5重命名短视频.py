from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import hashlib

root = tk.Tk()
root.withdraw()
target = filedialog.askdirectory() + r"//"

p = Path(target)

for dir in p.iterdir():
    if dir.is_dir():
        for file in dir.iterdir():
            if file.is_file():
                md5 = hashlib.md5(open(file, 'rb').read()).hexdigest()
                name = file.parent / Path(file.parent.stem + " - " + md5).with_suffix(file.suffix)
                print(str(file) + " : " + str(name))
                try:
                    file.rename(name)
                except:
                    print(str(name) + " : 文件重复")
                print(name)

# for file in p.iterdir():
#     if file.is_file() and file.suffix!='.ini':
#         actor = file.name.split(' - ')[0]
#         folder = file.parent/actor
#         if not folder.exists():
#             folder.mkdir()
#         name = folder/file.name
#         file.rename(name)
#         # print(file, name)
