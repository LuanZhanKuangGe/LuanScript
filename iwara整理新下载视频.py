from pathlib import Path
from func import iwara_headers
import requests


def list_files(directory):
    """列出指定目录下的所有文件"""
    path = Path(directory)
    files  = [f for f in path.iterdir() if f.is_file()]
    return files

def list_folders(directory):
    """列出指定目录下的所有文件夹,并按名称排序"""
    path = Path(directory)
    folders = [f for f in path.iterdir() if f.is_dir()]
    folders.sort(key=lambda x: x.name)
    return folders

folder_names = {}
folders = list_folders("X:/MMD")
for folder in folders:
    # 只处理以'['开头且不以'[Del]'开头的文件夹
    if not folder.name.startswith('[') or folder.name.startswith('[Del]'):
        continue
    user_name = folder.name.split('[')[1].split(']')[0]
    folder_names[user_name] = folder

files = list_files("X:/MMD/#Download")

for index,file in enumerate(files):
    print(f"正在处理[{index+1}/{len(files)}]: {file.name}")

    # 检查文件名中是否包含视频ID
    if '[' in file.name and ']' in file.name:
        video_id = file.name.replace('[Source]','').split('[')[-1].split(']')[0]
        print(f"视频ID: {video_id}")

        # 使用API获取视频信息
        url = f"https://api.iwara.tv/video/{video_id}"
        response = requests.get(url, headers=iwara_headers)
        if response.status_code == 200:
            dict = response.json()
            user_id = dict['user']['username']
            user_name = dict['user']['name']
            
            # 确定目标文件夹
            if folder_names.get(user_id) is not None:
                folder_path = folder_names[user_id]
            else:
                folder_path = f"X:/MMD/#Download/[{user_id}] {user_name}"
            
            # 创建目标文件夹(如果不存在)并移动文件
            Path(folder_path).mkdir(parents=True, exist_ok=True)
            file.rename(Path(folder_path, file.name))
            print(f"已移动到 {folder_path}")
        else:
            print(f"获取视频信息失败 https://www.iwara.tv/video/{video_id}, 请更新headers")
    else:
        print(f"在文件名 {file.name} 中未找到ID")
