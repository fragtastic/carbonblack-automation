#!/usr/bin/env bash

echo "Creating virtual environment"
python3 -m venv venv && echo "Success"

echo "Upgrading virtual environment"
python3 -m venv --upgrade venv && echo "Success"

echo "Entering virtual environment"
source venv/bin/activate

echo "Upgrading pip"
pip3 install --upgrade pip

echo "Installing dependencies"
pip3 install -r requirements.txt

echo "Please follow instructions completely in README.md"
