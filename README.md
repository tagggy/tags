#!/bin/bash -ex

# data input:
# copy table from docs to xlsx
# in libreoffice save as csv

# set delimiter to ','
# quotes around text
# save as input.orig.csv

# FIXUP
# replace german header with english header 
# id,year,author,title,epoch,genre,level,tags
# also get rid of all lines like this:
# 1750-1790;;;;;;

grep -v ',,,,,' input.orig.csv  | perl -pe 's/^"Zeitraum.*/id,year,author,title,epoch,genre,level,tags/'  | tr -s '\n' > input.csv

head -3 input.csv
sleep 3

# get mlr
# https://github.com/johnkerl/miller/releases

mlr --c2j --jlistwrap cat input.csv > input.json

# check validity of json

# caution: json.tool replaces umlauts
# python3 -mjson.tool input.json 

# caution: false positive
# jq input2.json
# jq: error: input2/0 is not defined at <top-level>, line 1:
# input2.json
# jq: 1 compile error

# but useless use of cat / STDIN works fine though: 
# cat input2.json | jq
jq < input.json && echo "json successful validated by jq"
