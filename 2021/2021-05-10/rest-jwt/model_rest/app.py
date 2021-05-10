from flask import Flask, jsonify, request
from joblib import load
import json
import numpy as np

app = Flask(__name__)
model = None
model_path = './model.ser'


def load_model(filename_p):
    print('Loading model from %s' % filename_p)
    p = load(filename_p)
    print('Model loaded!')
    return p


@app.route('/', methods=['POST'])
def index():
    global model
    if request.method == "POST":
        if model is None:
           model = load_model(model_path)
        print(request.data)
        parsed = json.loads(request.data)
        x = np.array(parsed['data'])
        X = np.array([x])
        scores = model.predict(X)
        r = dict()
        r['result'] = int(scores[0])  # int64 is not json serializable!
        print(r)
        return jsonify(r)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

