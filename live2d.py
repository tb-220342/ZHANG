# 角色网页模块
import json
import logging
from flask import Flask, send_from_directory

with open('data/db/config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
live2d_port = int(config["2D角色网页端口"])
app = Flask(__name__, static_folder='dist')
logging.getLogger('werkzeug').setLevel(logging.ERROR)


@app.route('/')
def index():  # 首页
    return app.send_static_file('live2d_web.html')


@app.route('/assets/<path:path>')
def serve_static(path):  # 静态资源
    return send_from_directory('./dist/assets', path)


@app.route('/api/get_mouth_y')
def read_txt():  # 读取缓存
    with open("data/cache/cache.txt", "r") as f:
        return json.dumps({"y": f.read()})


def run_live2d():  # 启动服务
    app.run(port=live2d_port, host="0.0.0.0")
