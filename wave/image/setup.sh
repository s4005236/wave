#! /bin/bash

sudo apt update
sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv build-essential git

#to setup tflite and opencv:
# Create virtual environment
# source .venv/bin/activate
# pip install --upgrade pip setuptools wheel
# pip install tflite-runtime
# pip install opencv-python