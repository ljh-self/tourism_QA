# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from flask import Flask, jsonify, request
from __init__ import app, db
from flask_cors import *


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# app = Flask(__name__)


# 模型定义
class ProductTest(db.Model):
    __tablename__ = 'ProductTest'
    UID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Token = db.Column(db.String(50), nullable=False)
    INIT_STATE = db.Column(db.Integer, nullable=False)
    RESP = db.Column(db.String(50), nullable=False)


# 跨域配置
CORS(app, supports_credentials=True)


# 对象转json格式函数
def to_json(self):
    # """将实例对象转化为json"""
    item = self.__dict__
    if "_sa_instance_state" in item:
        del item["_sa_instance_state"]
    return item


# 查询设备状态
@app.route('/query', methods=["GET", "POST"])
def query1():
    # 定义参数uid从请求中获取用户设备识别码
    # 查询INIT_STATE参数，写入JSON返回前端
    with app.app_context():
        uid = request.values.get("uid")
        line = ProductTest.query.get(uid)
        if line == None:
            return jsonify({"code": "0", "msg": "查询失败,检查UID是否输入正确"})
        return jsonify({"code": "1", "msg": "查询成功", "data": to_json(line)})


# 检查到命名意图，将名字和设备识别号作为参数提交至服务端
@app.route('/UpdateToken')
def update_token():
    with app.app_context():
        uid = request.values.get("uid")
        Token = request.values.get("Token")
        line = ProductTest.query.get(uid)
        if line == None:
            return jsonify({"code": "0", "msg": "查询失败,检查UID是否正确"})
        line.Token = Token
        line.RESP = '你好！我是' + line.Token
        line.INIT_STATE = 1
        db.session.commit()
        line = ProductTest.query.get(uid)
        print(to_json(line))
        return jsonify({"code": "1", "msg": "更新成功", "data": to_json(line)})


@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.debug = True
    app.run()
