import base64
from pathlib import Path

from jmcomic import create_option_by_file
from flask import Flask, jsonify, redirect, url_for, request, send_from_directory
from waitress import serve
from flask_swagger_ui import get_swaggerui_blueprint

from config import config
from album_service import get_album_pdf_path
import os

# 读取配置文件
cfg = config()
host = cfg.host
port = cfg.port
pdf_pwd = cfg.pdf_pwd
optionFile = cfg.option_file
pdf_dir = cfg.pdf_dir

# 可复用，不要在下方函数内部创建
opt = create_option_by_file(optionFile)

# 监听optionFile文件的变化, 实现配置文件的热更新
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 当配置文件发生变化时，重新读取配置文件
class cfgFileChangeHandler(FileSystemEventHandler):
    def __init__(self, observer):
        self.observer = observer

    def on_modified(self, event):
        if not event.is_directory and Path(optionFile).exists():
            global opt, pdf_dir
            opt = create_option_by_file(optionFile)
            pdf_dir = opt.plugins.after_album[0].kwargs.get('pdf_dir', './')
            print("配置文件已更新")

observer = Observer()
observer.schedule(cfgFileChangeHandler(observer), path=optionFile, recursive=False)
observer.start()

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "JMComic API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# 只保留根路径重定向到docs
@app.route('/')
def index():
    return redirect('/docs')

# 根据 jm_album_id 返回 pdf 文件
@app.route('/get_pdf/<jm_album_id>', methods=['GET'])
def get_pdf(jm_album_id):
    try:
        path, name = get_album_pdf_path(jm_album_id, pdf_dir, pdf_pwd, opt)
        if path is None:
            return jsonify({
                "success": False,
                "message": "PDF 文件不存在"
            }), 500
        with open(path, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode('utf-8')

        return jsonify({
            "success": True,
            "message": "PDF 获取成功",
            "name": name,
            "data": encoded_pdf
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

# 根据 jm_album_id 获取 pdf 文件下载到本地，返回绝对路径
@app.route('/get_pdf_path/<jm_album_id>', methods=['GET'])
def get_pdf_path(jm_album_id):
    try:
        path, name = get_album_pdf_path(jm_album_id, pdf_dir, pdf_pwd, opt)
        abspath = (os.path.abspath(path))
        if path is None:
            return jsonify({
                "success": False,
                "message": "PDF 文件不存在"
            }), 500
        else:
            return jsonify({
                "success": True,
                "message": "PDF 获取成功",
                "data": abspath,
                "name": name
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

if __name__ == '__main__':
    print(f"\nJMComic API 服务已启动!")
    print(f"API 文档地址: http://{host}:{port}/docs")
    print(f"服务地址: http://{host}:{port}\n")
    serve(app, host=host, port=port)