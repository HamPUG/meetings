from flask import Flask, jsonify, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from hashlib import sha256
from joblib import load
import json
import numpy as np


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = []
with open("./users.json", "r") as uf:
    data = json.load(uf)
    for k in data:
        users.append(User(len(users) + 1, k, data[k]))

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), sha256(password.encode('utf-8')).hexdigest()):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'super-secret'

model = None
model_path = './model.ser'


def load_model(filename_p):
    print('Loading model from %s' % filename_p)
    p = load(filename_p)
    print('Model loaded!')
    return p

jwt = JWT(app, authenticate, identity)

@app.route('/', methods=['POST'])
@jwt_required()
def predict():
    global model
    if model is None:
       model = load_model(model_path)
    parsed = json.loads(request.data)
    x = np.array(parsed['data'])
    X = np.array([x])
    scores = model.predict(X)
    r = dict()
    r['result'] = int(scores[0])  # int64 is not json serializable!
    return jsonify(r)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

