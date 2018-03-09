#!/usr/bin/env bash

curl -O http://sqlite.org/2016/sqlite-src-3140100.zip
unzip sqlite-src-3140100.zip
if [ "$(uname)" == "Darwin" ]; then
    gcc -g -fPIC -dynamiclib sqlite-src-3140100/ext/misc/json1.c -o json1
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    gcc -g -fPIC -shared sqlite-src-3140100/ext/misc/json1.c -o json1.so
fi
