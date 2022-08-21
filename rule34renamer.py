from pathlib import Path
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()
target = filedialog.askdirectory()

fo = open("rule34.txt", "r")

print(target)

lines = fo.readlines()
for line in lines:
    src = Path(target) / Path(line.split("?")[0].strip().split("/")[-1])
    name = Path(target) / Path(line.split("?")[1].strip() + ".mp4")

    if src.exists():
        src.rename(name)
        print(src, " 重命名为 ", name)
    else:
        print(src, " 不存在")
