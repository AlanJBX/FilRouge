#!/bin/bash

pip install flask
pip install boto3
pip install botocore
pip freeze > requirements.txt

# Puis : sls deploy