import json
import sys

import paramiko
from pathlib import Path
from tqdm import tqdm
from gooey import Gooey, GooeyParser

@Gooey(program_name="Update GUI")
def main():
    config = {"MangaPath": Path(r"U:\Manga"), "AVHD": Path(r"Y:"), "AVSD": Path(r"Z:"), "AVFC2": Path(r"W:"),
              "Rule34": Path(r"X:\rule34"),"MMD": Path(r"X:\MMD")}

    database = {"rule34_data": [], "rule34_artist": [], "mmd_data": [], "mmd_artist": [], "manga": {}, 'jav_id': [], 'jav_actor': {}}

    parser = GooeyParser(description="Update")
    parser.add_argument('--update_mmd', metavar='Checkbox', help='Update MMD', action='store_true')
    parser.add_argument('--update_rule34', metavar='Checkbox', help='Update rule34', action='store_true')
    parser.add_argument('--update_manga', metavar='Checkbox', help='Update manga', action='store_true')
    parser.add_argument('--update_javhd', metavar='Checkbox', help='Update JAV HD', action='store_true')
    parser.add_argument('--update_javsd', metavar='Checkbox', help='Update JAV SD', action='store_true')

    args = parser.parse_args()

    if args.update_mmd:
        # 更新mmd数据
        for folder in tqdm(list(config["MMD"].iterdir()), desc="update MMD"):
            if folder.is_dir() and not folder.name.startswith('[Del]'):
                for video in folder.rglob("*.mp4"):
                    video_id = video.stem.replace('[Source]', '')
                    video_id = video_id.split('[')[-1].split(']')[0].lower()
                    if video_id not in database["mmd_data"]:
                        database["mmd_data"].append(video_id)
                    else:
                        print(video)
                if folder.name.startswith('['):
                    artist = folder.name.split(']')[0].split('[')[1]
                    if artist not in database["mmd_artist"]:
                        database["mmd_artist"].append(artist)
                    else:
                        print(artist)

    if args.update_rule34:
        # 更新rule34数据
        for video in tqdm(list(config["Rule34"].rglob("*.mp4")), desc="update Rule34"):
            rule34_id: str = video.stem.split('_')[-1]
            rule34_artist: str = video.stem.split('_')[0]
            database["rule34_data"].append(rule34_id)
            if rule34_artist not in database["rule34_artist"]:
                database["rule34_artist"].append(rule34_artist)

    if args.update_manga:
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

    if args.update_javhd:
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

        for video in tqdm(list(config["AVFC2"].rglob("*.nfo")), desc="update AVFC2"):
            video_id = video.stem.split(" ")[0]
            database['jav_id'].append(video_id)
            video_id = video_id.replace('-', '-PPV-')
            database['jav_id'].append(video_id)

    if args.update_javsd:
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

if __name__ == "__main__":
    sys.exit(main())
