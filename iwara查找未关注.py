import os
from pathlib import Path
import requests
from func import iwara_headers

def get_folder_ids(directory):
    folder_ids = []
    for folder in Path(directory).iterdir():
        if folder.is_dir():
            folder_name = folder.name
            if '[' in folder_name and ']' in folder_name:
                folder_id = folder_name.split('[')[1].split(']')[0]
                file_count = len([f for f in folder.iterdir() if f.is_file()])
                folder_ids.append((folder_id, file_count))
    return folder_ids

mmd_directory = r"X:\MMD"
folder_ids = get_folder_ids(mmd_directory)

print(f"总共找到 {len(folder_ids)} 个文件夹ID。")

def get_following_ids():
    following_ids = []
    urls = [f"https://api.iwara.tv/user/252f2262-ec67-4e8b-89b6-7d98c0386ca9/following?page={i}" for i in range(17)]
    for url in urls:
        response = requests.get(url, headers=iwara_headers)
        if response.status_code == 200:
            data = response.json()
            following_ids.extend([user['user']['username'] for user in data['results']])
        else:
            print(f"获取关注列表失败，状态码：{response.status_code}")
    return following_ids

following_ids = get_following_ids()
print(f"总共获取到 {len(following_ids)} 个关注ID。")

print(f"未下载id：")
# 找出在following ids不在folder ids中的id
unfollowed_ids = [id for id in following_ids if id not in [folder_id for folder_id, _ in folder_ids]]
for id in unfollowed_ids:
    print(f"用户ID: {id}")

print(f"未关注id：")
# 找出在folder_ids中但不在following_ids中的ID和文件数
unfollowed_folders = [(folder_id, file_count) for folder_id, file_count in folder_ids if folder_id not in following_ids]

# 按文件数量从高到低排序
unfollowed_folders.sort(key=lambda x: x[1], reverse=True)

for folder_id, file_count in unfollowed_folders:
    print(f"用户ID: {folder_id}, 文件数量: {file_count}")




# print("\n以下是你已创建文件夹但尚未关注的用户ID和文件数（按文件数量从高到低排序）：")
# valid_unfollowed_folders = []
# for id, file_count in unfollowed_folders:
#     url = f"https://api.iwara.tv/profile/{id}"
#     response = requests.get(url, headers=iwara_headers)
#     if response.status_code == 200:
#         data_dict = response.json()
#         user_id = data_dict['user']['id']
#         url2 = f"https://api.iwara.tv/videos?user={user_id}"
#         response2 = requests.get(url2, headers=iwara_headers)
#         if response2.status_code == 200:
#             data2_dict = response2.json()
#             video_count = len(data2_dict['results'])
#             if video_count > 0:
#                 valid_unfollowed_folders.append((id, file_count))
#                 print(f"{id}: {file_count}个文件")

# print(f"总共有 {len(valid_unfollowed_folders)} 个已创建文件夹但尚未关注的有效用户。")




