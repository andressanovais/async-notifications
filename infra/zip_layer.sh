#!/bin/bash
mkdir -p copy

cp -a $directory_to_zip/. copy
cd copy
pip install -r requirements.txt -t python

zip -r ../$output *

cd ..
rm -r copy