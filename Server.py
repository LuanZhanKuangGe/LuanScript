from flask import Flask
from pathlib import Path
import json
import logging


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

app.config["MangaPath"] = Path("Y:\Manga")


@app.route("/manga", methods=["GET"])
def api_manga():
    logging.info("获取Manga文件列表")
    dict = {}
    for manga in app.config["MangaPath"].iterdir():
        artist = manga.stem.split(" ", 1)[0]
        name = manga.stem.split(" ", 1)[1]
        if not artist in dict:
            dict[artist] = []
        dict[artist].append(name)
    return json.dumps(dict)


if __name__ == "__main__":
    # print(api_manga())
    app.run(host="0.0.0.0", port="8864")
