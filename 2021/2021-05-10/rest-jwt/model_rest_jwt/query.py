import requests
import json
from sklearn import datasets
from sklearn.model_selection import train_test_split
from hashlib import sha256


iris = datasets.load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


d = dict()
d['username'] = 'user1'
d['password'] = 'abcxyz'
r = requests.post('http://127.0.0.1:5000/auth', json=d)
j = r.json()
token = j['access_token']
print(token)


for i in range(len(X_test)):
    j = dict()
    j['data'] = list(X_test[i])
    r = requests.post('http://127.0.0.1:5000/', data=json.dumps(j), headers={'Authorization': "JWT " + token})
    j = r.json()
    act = y_test[i]
    pred = j['result']
    print(X_test[i], act, pred, ("" if (act == pred) else "error"))
