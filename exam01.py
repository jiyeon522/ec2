# request : client -> server 요청을 보냄
# response : server -> client 요청을 받음

# python server
# 1) flask : 마이크로 웹 프레임워크 (12000  line) 
# 2) Django : 모든 기능이 포함되어있음 (flask보다 10~20배 무겁다)

# 가상환경변경하는 법
# Ctrl + Shift + P -> interpreter 검색 -> select interpreter

# 터미널 창에서 Ctrl+L -> clear
from flask import Flask # route 경로, run 서버 실행
from flask import render_template # html load
from flask import request # 사용자가 보낸 정보
from flask import redirect # 페이지 이동
from flask import make_response # 페이지 이동 시 정보 유지!!

# aws.py 안에 detect ~ 함수만 쓰고 싶다면
from aws import detect_labels_local_file
from aws import compare_faces as cf

# 파일 이름 보안 처리 라이브러리
from werkzeug.utils import secure_filename

import os 
# static 폴더가 없다면 만들어라
if not os.path.exists("static"):
    os.mkdir("static")

app = Flask(__name__)
@app.route("/") # 웹사이트 경로 지정
def index():    # 사이트 들어가게되면 실행되는 함수
    return render_template("index.html") #같은 경로에 있는 templates 파일을 찾아 그 안에 있는 html 문서 실행 

@app.route("/compare", methods = ["POST"])
def compare_faces():
    if request.method == "POST":
        # 1. compare로 오는 file1, file2를 받아서
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        file1_name = secure_filename(file1.filename) # 보안정책상 한번 꼭 감싸주기
        file2_name = secure_filename(file2.filename)

        # 2. static폴더에 save
        file1.save("static/" + file1_name) # static/ 위치에 file1_name 저장
        file2.save("static/" + file2_name)

        # 3. 두개의 이미지 compare_faces 함수에 던지기
        r = cf("static/" + file1_name, "static/" + file2_name) 

    return r

@app.route("/detect", methods = ["POST"])
def dectect_label():

    # flask에서 보안 규칙상 file 이름을 secure 처리 해야 한다
    if request.method == "POST":
        file = request.files["file"]

        # file을 static 폴더에 저장하고
        file_name = secure_filename(file.filename)
        file.save("static/" + file_name)
        # 해당 경로를 detect_lo~ 함수에 전달
        r = detect_labels_local_file("static/" + file_name) 

    return r

@app.route("/secret", methods = ["POST"])
def box():
    try: 
        if request.method == "POST":
            # get -> args[key], post -> form[key]
            hidden = request.form["hidden"]
            return f"비밀정보 : {hidden}"
    except:
        return "데이터 전송 실패"

@app.route("/login", methods = ["GET"])
def login():
    if request.method == "GET":

        # 페이지 이동 : redirect 필요
        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]
        if login_id == "1234" and login_pw == "1234":
            # 로그인 성공
            response = make_response(redirect("/login/success"))
            response.set_cookie("user", login_id)
            return response
        else:
            # 로그인 실패
            return redirect("/")
    
    return "로그인 성공"

@app.route("/login/success", methods = ["GET"])
def login_success():
    login_id = request.cookies.get("user")
    return f"{login_id}님 방가방가"

if __name__ == "__main__":
    app.run(host="0.0.0.0")