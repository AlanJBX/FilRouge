#!/bin/bash

pip install npm
mkdir my-flask-application && cd my-flask-application
npm init -f
npm install --save-dev serverless-wsgi serverless-python-requirements
virtualenv venv --python=python3

# Puis : source venv/bin/activate.csh