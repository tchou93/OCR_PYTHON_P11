# Project P11

## Steps to install the environment:
```
* Clone the project from github:
$ git clone https://github.com/tchou93/OCR_PYTHON_P11.git

* Install the last version of python
https://www.python.org/downloads/

* Use a virtual environment
$ python -m venv env
$ source env/Scripts/activate

* Install some specific packets on this virtual environment
$ pip install -r requirements.txt
```

## Step to run Flask server from the project root:
```
$ export FLASK_APP = "server.py"
$ flask run
```

## Information about how to run the Unitary/Integrations/Functional tests from the project root:
```
* All the tests:
$ pytest

* Unitary tests:
$ pytest tests/unit_test

* Integrations tests:
$ pytest tests/integration_test

* Functional test:
$ pytest tests/functional_test
```

## Information about how to run the Performance test from the project root:
```
Step 1:
* Run flask server

Step 2:
$ cd tests/performance_test
$ locust

Step 3:
* Enter to the url http://localhost:8089 then enter the followings informations:
 Number of users: 6
 Spawn rate: 1
 Host: http://127.0.0.1:5000/
* Click to start swarming
```