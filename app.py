from flask import Flask, request
from find import detect

app = Flask(__name__)


@app.route('/test')
def hello_world():
    return 'hello'


@app.route('/findDup', methods=['POST'])
def detectWithFlask():
    print("test in")
    picStr = request.get_json()
    result_dict = detect(picStr)  # detect returns a 2-D array
    return str(result_dict)
