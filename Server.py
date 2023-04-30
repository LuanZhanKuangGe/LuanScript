from flask import Flask, render_template
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def api_main():
    with open("./data.json", "r", encoding="utf8") as fp:
        dict = json.load(fp)
        return dict


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="2233")
