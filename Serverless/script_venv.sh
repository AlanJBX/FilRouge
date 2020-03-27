#!/bin/bash

npm init -f
npm install --save-dev serverless-wsgi serverless-python-requirements
virtualenv venv --python=python3

# Puis : source venv/bin/activate