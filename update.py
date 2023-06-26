import json
import paramiko
from pathlib import Path

config = {"MangaPath": Path(r"N:\HentaiPicture\Manga"), "AVPath": Path(r"N:\AV"),
          "Rule34": Path(r"N:\HentaiVideo\rule34"),"MMD": Path(r"N:\HentaiVideo\MMD")}

database = {"rule34_data": [], "rule34_artist": [], "mmd_data": [], "manga": {}, 'jav_id': [], 'jav_actor': {}}

# 更新mmd数据
for folder in config["MMD"].iterdir():
    if folder.is_dir() and not folder.name.startswith('[Del]'):
        for video in folder.glob("*.mp4"):
            video_id = video.stem.split('[')[-2].split(']')[0]
            database["mmd_data"].append(video_id)


# 更新rule34数据
for video in config["Rule34"].rglob("*.mp4"):
    rule34_id: str = video.stem.split('_')[-1]
    rule34_artist: str = video.stem.split('_')[0]
    database["rule34_data"].append(rule34_id)
    if rule34_artist not in database["rule34_artist"]:
        database["rule34_artist"].append(rule34_artist)

# 更新manga数据
for manga in config["MangaPath"].iterdir():
    if "] " not in manga.stem:
        print(manga)
        continue
    manga_artist = manga.stem.split("] ", 1)[0] + "]"
    name = manga.stem.split("] ", 1)[1]
    if manga_artist not in database['manga']:
        database['manga'][manga_artist] = []
    database['manga'][manga_artist].append(name)

# 更新JAV数据
for video in config["AVPath"].rglob("*.nfo"):
    video_id = video.stem.split(" ")[0]
    if video_id.find("]") != -1:
        video_id = video_id.split("]")[1]
        if video_id[-1] == 'z':
            video_id = video_id[0:-1]
        database['jav_id'].append(video_id)
    else:
        print(video)

# # 更新JAV演员数据
# for actor in (config["AVPath"] / "[[单体]]").iterdir():
#     if actor.is_dir():
#         actor_name = actor.stem.split("_")[0]
#         database['jav_actor'][actor_name] = []
#         for video in actor.rglob("*.nfo"):
#             video_id = video.stem.split(" ")[0].split("]")[1]
#             if video_id[-1] == 'z':
#                 video_id = video_id[0:-1]
#             database['jav_actor'][actor_name].append(video_id)

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
