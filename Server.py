from flask import Flask
from pathlib import Path
import json
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

app.config["MangaPath"] = Path("Y:\Manga")
app.config["AVPath"] = Path("X:\\")

@app.route("/", methods=["GET"])
def api_main():
    # logging.info("更新全部json")
    # dict = {}
    # dict["actor"] = []
    # dict["av"] = []
    # for av in app.config["AVPath"].rglob('*.nfo'):
    #     id = av.name.split(" ")[0]
    #     dict["av"].append(id)
    # with open('av.json','a',encoding='utf8')as fp:
    #     json.dump(dict,fp,ensure_ascii=False)
    # logging.info("av.json done!")

    dict = {}
    for manga in app.config["MangaPath"].iterdir():
        artist = manga.stem.split(" ", 1)[0]
        name = manga.stem.split(" ", 1)[1]
        if artist not in dict:
            dict[artist] = []
        dict[artist].append(name)
    with open('manga.json','a',encoding='utf8')as fp:
        json.dump(dict,fp,ensure_ascii=False)
    logging.info("manga.json done!")

    return "更新完成"

@app.route("/manga", methods=["GET"])
def api_manga():
    with open('./manga.json','r',encoding='utf8')as fp:
        dict = json.load(fp)
        return dict


@app.route("/av", methods=["GET"])
def api_av():
    with open('./av.json','r',encoding='utf8')as fp:
        dict = json.load(fp)
        return dict

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8864")
