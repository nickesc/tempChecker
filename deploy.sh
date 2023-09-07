#!/usr/bin/env sh

deploypath="/Volumes/CIRCUITPY"

cp -rv "lib" $deploypath
cp -v "code.py" $deploypath
cp -v "settings.toml" $deploypath
