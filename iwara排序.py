import re
from pathlib import Path

def get_video_count(folder_name):
    match = re.search(r'#(\d+)v', folder_name)
    return int(match.group(1)) if match else 0

def get_rating(folder_name):
    match = re.search(r'#(\d+\.?\d*)k', folder_name)
    return float(match.group(1)) if match else 0

mmd_folder = Path('X:/MMD')

folder_info = []

for folder in mmd_folder.iterdir():
    if folder.is_dir() and "#del" not in folder.name and "#2024" not in folder.name:
        video_count = get_video_count(folder.name)
        rating = get_rating(folder.name)
        folder_info.append((folder, video_count, rating))

print("文件夹信息：")
# 对folder_info进行排序，先根据视频数（降序），视频数相同则按评分（降序）
sorted_folder_info = sorted(folder_info, key=lambda x: (-x[1], -x[2]))

print("排序后的文件夹信息：")
for folder, video_count, rating in sorted_folder_info:
    print(f"文件夹: {folder.name}, 视频数: {video_count}, 评分: {rating}")