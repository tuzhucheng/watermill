#!/usr/bin/env bash

curl -O http://sqlite.org/2016/sqlite-src-3140100.zip
unzip sqlite-src-3140100.zip
gcc -g -fPIC -dynamiclib sqlite-src-3140100/ext/misc/json1.c -o json1
