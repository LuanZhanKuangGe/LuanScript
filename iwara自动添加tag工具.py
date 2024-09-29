# 导入所需的库
from pathlib import Path
import requests
from func import iwara_headers

def get_video_likes(user_id):
    """获取用户视频的平均点赞数(以千为单位)"""
    video_likes = 0
    url = f"https://api.iwara.tv/videos?sort=likes&page=0&user={user_id}"
    response = requests.get(url, headers=iwara_headers)
    if response.status_code == 200:
        videos_json = response.json()
        if len(videos_json['results']) > 0:
            for video in videos_json['results']:
                likes = video['numLikes']
                video_likes += likes
            return round((video_likes / len(videos_json['results'])) / 1000, 1)
        else:
            return 0
    else:
        print(f"访问URL失败: {url}")
        return 0

def get_last_video_year(user_id):
    """获取用户最后一个视频的发布年份"""
    url = f"https://api.iwara.tv/videos?sort=date&page=0&user={user_id}"
    response = requests.get(url, headers=iwara_headers)
    if response.status_code == 200:
        videos_json = response.json()
        if len(videos_json['results']) > 0:
            last_video_year = videos_json['results'][0]['createdAt'].split('-')[0]
            return last_video_year
        else:
            return None
    else:
        print(f"访问URL失败: {url}")
        return None


def get_profile_json(name):
    """获取用户的个人资料信息"""
    user_name = None
    last_video_year = None
    video_likes = 0

    url = f"https://api.iwara.tv/profile/{name}"
    response = requests.get(url, headers=iwara_headers)
    if response.status_code == 200:
        dict = response.json()
        user_id = dict['user']['id']
        user_name = dict['user']['name']
        last_video_year = get_last_video_year(user_id)
        video_likes = get_video_likes(user_id)
    elif response.status_code == 404:
        last_video_year = 'del'
    else:
        print(f"访问URL失败: {url}")
    return user_name, last_video_year, video_likes


def list_folders(directory):
    """列出指定目录下的所有文件夹"""
    path = Path(directory)
    folders = [f for f in path.iterdir() if f.is_dir()]
    folders.sort(key=lambda x: x.name)
    return folders

folders = list_folders("X:\MMD\#Download")
for index,folder in enumerate(folders):
    if not folder.name.startswith('[') or folder.name.startswith('[Del]'):
        continue
    
    print(f"正在处理[{index+1}/{len(folders)}]: {folder.name}")
    
    mp4_files = list(folder.glob('*.mp4'))
    mp4_count = len(mp4_files)

    if mp4_count < 10:
        mp4_count = 0
    elif 10 <= mp4_count < 50:
        mp4_count = 10
    elif 50 <= mp4_count < 100:
        mp4_count = 50
    else:
        mp4_count = 100
    
    name = folder.name.split('[')[1].split(']')[0]
    user_name, last_video_year, video_likes = get_profile_json(name)

    if last_video_year is not None:
        new_folder_name = f"[{name}] {user_name} #{last_video_year}"
        if video_likes != 0:
            new_folder_name = f'{new_folder_name} #{video_likes}k'
        if mp4_count != 0:
            new_folder_name = f'{new_folder_name} #{mp4_count}v'
        new_folder_path = folder.parent / new_folder_name
        print(f"正在将文件夹从 '{folder.name}' 重命名为 '{new_folder_name}'")
        folder.rename(new_folder_path)
    else:
        print(f"无法获取 {user_name} 的最后视频年份")

