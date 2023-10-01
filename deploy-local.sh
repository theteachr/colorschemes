#!/bin/bash

set -xe

python3.11 generate.py

cd colors
elm-live --host 0.0.0.0 src/Main.elm -- --output=main.js --debug
