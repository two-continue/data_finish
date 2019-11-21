# server.py
import os
# request フォームから送信した情報を扱うためのモジュール
# redirect  ページの移動
# url_for アドレス遷移
from flask import Flask, request, render_template, redirect, url_for
# ファイル名をチェックする関数
from werkzeug.utils import secure_filename
# 画像のダウンロード
from flask import send_from_directory

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)







@app.route('/')
def index():
    return render_template('index.html')
@app.route('/view.html')
def view():
    return render_template('view.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)