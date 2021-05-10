# REST with JWT

* Presentation ([odp](flask_rest_api_with_jwt.odp), [pdf](flask_rest_api_with_jwt.pdf))
* Code examples

  * [Generating a Model with scikit-learn](model)
  * [Open Model REST API](model_rest)
  * [Using JWT](jwt_quickstart)
  * [Using JWT (hashed passwords)](jwt_quickstart_hashed)
  * [Using JWT (hashed passwords loaded from file)](jwt_quickstart_hashed_from_file)
  * [JWT Model REST API](model_rest_jwt)

## Notes:

* You can create the virtual environments in each sub-directory as follows:

  ```commandline
  python3 -m venv venv
  ./venv/bin/pip install -r requirements.txt
  ```

* The REST APIs get started via:

  ```commandline
  ./venv/bin/python app.py
  ```

* Other models get launched via `./venv/bin/python FILE.py`

* [curl](https://en.wikipedia.org/wiki/CURL) is used to simulate clients in some of the examples, otherwise the [requests](https://docs.python-requests.org/) Python library is used.
