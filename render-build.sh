#!/bin/bash
# Upgrade pip first
pip install --upgrade pip

# Install Cython before any other packages
pip install Cython

# Install the rest of the dependencies
pip install -r requirements.txt
