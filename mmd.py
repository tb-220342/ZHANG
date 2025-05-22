import json
import logging
from flask import Flask, send_from_directory

with open('data/db/config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
mmd_port = int(config["3D角色网页端口"])
app = Flask(__name__, static_folder='dist')
logging.getLogger('werkzeug').setLevel(logging.ERROR)


@app.route('/')
def index():
    return app.send_static_file('mmd_web.html')


@app.route('/vmd')
def index_vmd():
    return app.send_static_file('mmd_vmd_web.html')


@app.route('/assets/<path:path>')
def serve_static(path):
    return send_from_directory('./dist/assets', path)


@app.route('/api/get_mouth_y')
def read_txt():  # 读取缓存
    with open("data/cache/cache.txt", "r") as f:
        return json.dumps({"y": f.read()})


def run_mmd():
    print(f"http://127.0.0.1:{mmd_port}\nhttp://127.0.0.1:{mmd_port}/vmd")
    app.run(port=mmd_port, host="0.0.0.0")
