from flask import Flask
from flask import request, jsonify
import os
from thuglife import Thug

application = Flask(__name__)
th = Thug()

@application.route('/', methods=['GET'])
def hello():
    return "OK"

@application.route('/thuglife', methods=['POST'])
def thuglife():
    if request.method == "POST":
        base64_string = request.form['img_base64']
        base64_string = base64_string.replace("data:image/jpeg;base64,","")
        thug_b64_img = th.process(base64_string)
        result = {"thugImg": thug_b64_img}
        # print(result)
        return jsonify(isError = False,
                    message= "Success",
                    statusCode= 200,
                    data = result), 200

if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 33507))
    # application.run(threaded=False, debug=False, port=port)
    application.run()