# jwt_quickstart_hashed

* Based on:

  https://pythonhosted.org/Flask-JWT/

* Start the app

  ```commandline
  ./venv/bin/python app.py
  ```

* obtain a token

  ```commandline
  curl -H "Content-Type: application/json" -X POST -d '{"username":"user1","password":"abcxyz"}' http://localhost:5000/auth
  ```

*  make a REST request (and replace `REPLACE_WITH_TOKEN` with the token the previous command generated)

  ```commandline
  curl -X GET http://localhost:5000/protected -H "Authorization: JWT REPLACE_WITH_TOKEN"
  ```

