#! /bin/bash

sudo apt update
sudo apt full-upgrade -y
sudo apt install -y python3-pip python3-venv build-essential git
# Needed for working with Raspberry Pi 4
sudo apt install -y python3-libcamera python3-kms++ libcap-dev

# TODO setup all apt dependencies here