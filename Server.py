from flask import Flask, render_template
from pathlib import Path
import json
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

app.config["MangaPath"] = Path("Y:\Manga")
app.config["AVPath"] = Path("X:\\")
app.config["3DPath"] = Path("Z:\\rule34\\")

@app.route("/updateav", methods=["GET"])
def update_av():
    dict = {}
    for actor in app.config["AVPath"].iterdir():
        if actor.is_dir():
            dict[actor.stem.split("_")[0]] = []
            for video in actor.rglob("*.nfo"):
                dict[actor.stem.split("_")[0]].append(video.stem.split(" ")[0])
    with open("av.json", "w", encoding="utf8") as fp:
        json.dump(dict, fp, ensure_ascii=False)
    logging.info("av.json done!")
    return "更新AV完成"


@app.route("/updatemanga", methods=["GET"])
def update_manga():
    dict = {}
    for manga in app.config["MangaPath"].iterdir():
        artist = manga.stem.split("] ", 1)[0] + "]"
        name = manga.stem.split("] ", 1)[1]
        if artist not in dict:
            dict[artist] = []
        dict[artist].append(name)
    with open("manga.json", "w", encoding="utf8") as fp:
        json.dump(dict, fp, ensure_ascii=False)
    logging.info("manga.json done!")
    return "更新manga完成"

@app.route("/update3d", methods=["GET"])
def update_3d():
    dict = {}
    dict["data"] = []
    for video in app.config["3DPath"].iterdir():
        dict["data"].append(video.stem)
    with open("3d.json", "w", encoding="utf8") as fp:
        json.dump(dict, fp, ensure_ascii=False)
    logging.info("3d.json done!")
    return "更新3D完成"


@app.route("/", methods=["GET"])
def api_main():
    return render_template('server.html')


@app.route("/manga", methods=["GET"])
def api_manga():
    with open("./manga.json", "r", encoding="utf8") as fp:
        dict = json.load(fp)
        return dict


@app.route("/av", methods=["GET"])
def api_av():
    with open("./av.json", "r", encoding="utf8") as fp:
        dict = json.load(fp)
        return dict

@app.route("/3d", methods=["GET"])
def api_3d():
    with open("./3d.json", "r", encoding="utf8") as fp:
        dict = json.load(fp)
        return dict

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8864")
