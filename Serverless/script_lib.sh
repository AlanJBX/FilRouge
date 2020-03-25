#!/bin/bash

pip install flask
pip install boto3
pip install botocore
pkg install docker
pip freeze > requirements.txt

# Puis : sls deploy