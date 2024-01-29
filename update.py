import json
import paramiko
from pathlib import Path
from tqdm import tqdm

config = {"MangaPath": Path(r"U:\Manga"), "AVHD": Path(r"Y:"), "AVSD": Path(r"Z:"), "AVFC2": Path(r"W:"),
          "Rule34": Path(r"X:\rule34"),"MMD": Path(r"X:\MMD")}

database = {"rule34_data": [], "rule34_artist": [], "mmd_data": [], "manga": {}, 'jav_id': [], 'jav_actor': {}}

# 更新mmd数据
folder_list = []
for folder in tqdm(list(config["MMD"].iterdir()), desc="update MMD"):
    if folder.is_dir() and not folder.name.startswith('[Del]'):
        for video in folder.glob("*.mp4"):
            video_id = video.stem.replace('[Source]', '')
            video_id = video_id.split('[')[-1].split(']')[0]
            database["mmd_data"].append(video_id)
        folder_name = folder.name.split(' ')[0]
        if folder_name not in folder_list:
            folder_list.append(folder_name)
        else:
            print(folder_name)

# 更新rule34数据
for video in tqdm(list(config["Rule34"].rglob("*.mp4")), desc="update Rule34"):
    rule34_id: str = video.stem.split('_')[-1]
    rule34_artist: str = video.stem.split('_')[0]
    database["rule34_data"].append(rule34_id)
    if rule34_artist not in database["rule34_artist"]:
        database["rule34_artist"].append(rule34_artist)

# 更新manga数据
for manga in tqdm(list(config["MangaPath"].iterdir()), desc="update Manga"):
    if "] " not in manga.stem:
        print(manga)
        continue
    manga_artist = manga.stem.split("] ", 1)[0] + "]"
    name = manga.stem.split("] ", 1)[1]
    if manga_artist not in database['manga']:
        database['manga'][manga_artist] = []
    database['manga'][manga_artist].append(name)

# 更新JAV数据
for video in tqdm(list(config["AVHD"].rglob("*.nfo")), desc="update AVHD"):
    video_id = video.stem.split(" ")[0]
    if video_id.find("]") != -1:
        video_id = video_id.split("]")[1]
        if video_id[-1] == 'z':
            video_id = video_id[0:-1]
        if video_id not in database['jav_id']:
            database['jav_id'].append(video_id)
        else:
            print(video_id)
    else:
        print(video)

for video in tqdm(list(config["AVSD"].rglob("*.nfo")), desc="update AVSD"):
    video_id = video.stem.split(" ")[0]
    if video_id.find("]") != -1:
        video_id = video_id.split("]")[1]
        if video_id[-1] == 'z':
            video_id = video_id[0:-1]
        if video_id not in database['jav_id']:
            database['jav_id'].append(video_id)
        else:
            print(video_id)
    else:
        print(video)

for video in tqdm(list(config["AVFC2"].rglob("*.nfo")), desc="update AVFC2"):
    video_id = video.stem.split(" ")[0]
    database['jav_id'].append(video_id)
    video_id = video_id.replace('-', '-PPV-')
    database['jav_id'].append(video_id)

with open("data.json", "w", encoding="utf8") as fp:
    json.dump(database, fp, ensure_ascii=False)


# 连接到 Linux 主机
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname='192.168.5.1', username='root', password='1234')

# 传输文件
sftp_client = ssh_client.open_sftp()
# sftp_client.put('./server.py', '/share/script/server.py')
sftp_client.put('./data.json', '/share/script/data.json')
sftp_client.close()

# 断开连接
ssh_client.close()
