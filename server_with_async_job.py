from multiprocessing import Process
from flask import Flask, jsonify, request
import time


app = Flask(__name__)


@app.route('/render', methods=['GET'])
def render_script():
    data = request.args.to_dict()
    heavy_process = Process(  # Create a daemonic process with heavy "my_func"
        target=my_func,
        args=(data['id']),
        daemon=True
    )
    heavy_process.start()
    return jsonify(
        mimetype='application/json',
        status=200
    )

# Define some heavy function
def my_func(id):
    time.sleep(10)
    print("Process finished. id: {}".format(id))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6018)
