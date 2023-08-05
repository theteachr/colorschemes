#!/bin/bash

python3.11 generate.py

cd colors
elm-live src/Main.elm -- --output=main.js --debug
