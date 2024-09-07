#!/usr/bin/env bash

python3 -m venv .venv

source .venv/bin/activate
pip3 install -U pip
pip3 install -U flask
pip3 install -U python-dotenv
pip3 install -U gunicorn
pip3 install -U wakeonlan
