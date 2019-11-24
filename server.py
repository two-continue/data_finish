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
#画像の処理
import cv2

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def average_rgb(cutphoto):
    img = cv2.imread('./uploads/camera_capture_2.jpg')
    averages = img.mean(0).mean(0) # BGRの値を全ピクセルで平均した値
    return averages


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file', filename=filename))
            in_jpg = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            out_jpg = "./uploads/camera_capture_2.jpg"

            #画像を読み込み
            image1 = cv2.imread(in_jpg)
            #グレースケールに変換
            image_gs = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            # 「./haarcascade_frontalface_alt.xml」をカレントディレクトリィに置くと確実
            cascade = cv2.CascadeClassifier("./haarcascade_mcs_mouth.xml")
            #引数についてはcascade.detectMultiScaleで検索
            face_list = cascade.detectMultiScale(image_gs,scaleFactor=1.1,minNeighbors=2)
            #ここで切り出し
            if len(face_list) > 0:
                for rect in face_list:
                    image_cut = image1[rect[1]:rect[1]+rect[3],rect[0]:rect[0]+rect[2]]
            else:
                print("no face")
            #切り出した画像を保存
            cutphoto = cv2.imwrite(out_jpg, image_cut)
            rgbs = average_rgb(cutphoto)
            if 0 <= rgbs[0] <= 68 and 52 <= rgbs[1] <= 82 and 108 <= rgbs[2] <= 138:
                return render_template('carrot.html')
            elif 35 <= rgbs[0] <= 75 and 42 <= rgbs[1] <= 82 and 97 <= rgbs[2] <= 137:
                return render_template('tomato.html')
            elif 37 <= rgbs[0] <= 87 and 61 <= rgbs[1] <= 101 and 55 <= rgbs[2] <= 95:
                return render_template('cucumber.html')
            elif rgbs[0] >= 230 and rgbs[1] >= 230 and rgbs[2] >= 230:
                return render_template('daikon.html')
            elif 21 <= rgbs[0] <= 61 and 68 <= rgbs[1] <= 108 and 85 <= rgbs[2] <= 125:
                return render_template('poteto.html')
            elif 70 <= rgbs[0] <= 109 and 40 <= rgbs[1] <= 96 and 61 <= rgbs[2] <= 110:
                return render_template('eggplant.html')
            else:
                return render_template('eggplant.html')
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    return render_template('view.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)