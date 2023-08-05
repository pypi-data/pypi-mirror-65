#!/bin/bash

# Project Rocket
# This is the upload script required for delivery on the packaging server

# Author: Martin Shishkov
# Created : 30.03.2020
#

python setup.py register sdist --format=gztar upload
