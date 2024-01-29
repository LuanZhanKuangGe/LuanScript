import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import pymediainfo
from tqdm import tqdm

root = tk.Tk()
root.withdraw()
root_dir = filedialog.askdirectory() + r"//"

for dir in tqdm(list(Path(root_dir).glob('*'))):
    if dir.is_dir():
        for nas_dir in Path(r"Y:").glob('*'):
            if nas_dir.is_dir():
                if nas_dir.name.split(' - ')[0] == dir.name:
                    new_dir_path = Path(root_dir) / nas_dir.name
                    dir.rename(new_dir_path)
                    print(f"重命名文件夹: {dir} -> {new_dir_path}")

for dir in tqdm(list(Path(root_dir).rglob('*'))):
    if dir.is_dir():
        nfo_files = list(dir.glob("*.nfo"))
        if nfo_files:
            for item in dir.iterdir():
                if item.suffix!='.nfo' and item.suffix!='.jpg':
                    print(f"找到视频文件: {item}")
                    media_info = pymediainfo.MediaInfo.parse(item)
                    for track in media_info.tracks:
                        if track.track_type == 'Video':
                            width = track.width
                            height = track.height
                            tag = '[SD]'
                            if height >= 720:
                                tag = '[HD]'
                                print(f"视频分辨率：{width}x{height}", tag)
                    for file_path in dir.iterdir():
                        if file_path.name.split(' ')[0] == item.name.split(' ')[0]:
                            file_name = file_path.name
                            new_file_name = f"{tag}{file_name}"
                            new_file_path = dir / new_file_name
                            file_path.rename(new_file_path)
                            print(f"重命名文件: {file_path} -> {new_file_path}")


