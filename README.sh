#!/bin/bash -e

# you need: (see below for details)
# mlr
# input.orig.csv
# jq (optional for validity check)
# python3.7 or newer
# gen.html.py

# data input:
# in libreoffice Calc save the table as csv
# set delimiter to ','
# note: tick formatting checkbox: quotes around text
# save as $INPUT_ORIG_FILE
# note: 'libreoffice --headless ---convert-to csv' was troublesome :(

INPUT_ORIG_FILE=input.orig.csv

# replace german header with english header and generate cleaned up version "input.csv"
# new header line contains the json keys
# also get rid of all lines like this one:
# 1750-1790,,,,,
# original header line of $INPUT_ORIG_FILE
# "Zeitraum","Jahr","Autor/ Autorin","Titel","Epoche","Gattung","Stufe","URL","label_author","label_title","Vorname","Nachname","Schlagworte"
echo "INFO FIXUP STEP: get better json keys"
grep -v ',,,,,' $INPUT_ORIG_FILE | perl -pe 's/^"Zeitraum.*/id,year,author,title,epoch,genre,level,url,label_author,label_title,first_name,last_name,tags/'  | tr -s '\n' > input.csv

# get mlr ("miller") to convert csv to json
# to make use of json.load in python
# https://github.com/johnkerl/miller/releases

mlr --c2j --jlistwrap cat input.csv > input.json

echo "INFO FIXUP STEP: fixup 10 int instead of str"
perl -i -pe 's/"level": 10,/"level": "10",/g' input.json

echo "INFO: json VALIDITY CHECK"
# would have loved to use:
# python3 -mjson.tool input.json
# but json.tool replaces umlauts :/
# TODO: find option to suppress this behaviour
# for the time being use jq [https://jqlang.github.io/jq/]

# caution: false positive
# jq input.json
# jq: error: input2/0 is not defined at <top-level>, line 1:
# input.json
# jq: 1 compile error

# but useless use of cat / STDIN works fine though:
# cat input2.json | jq
jq < input.json && echo "json successful validated by jq, now onto creating those html snippets..."

# clean up html results of last run
rm -f 10_nach_*.html BF_nach_*.html LF_nach_*.html

time -p ./gen.html.py
