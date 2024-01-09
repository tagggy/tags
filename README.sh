#!/bin/bash -e

rm -f 10_nach_Autoren.html 10_nach_Jahren.html 10_nach_Schlagworten.html BF_nach_Autoren.html BF_nach_Jahren.html BF_nach_Schlagworten.html LF_nach_Autoren.html LF_nach_Jahren.html LF_nach_Schlagworten.html

clear

# data input:
# copy table from M$ Word docx to libreoffice calc
# TOOD: input could be a table from the beginning as the word document only contains that table
# in libreoffice save as csv
# set delimiter to ','
# note: tick formatting checkbox: quotes around text
# save as input.orig.csv

echo "INFO FIXUP STEP to get better json keys"
# replace german header with english header 
# also get rid of all lines like this:
# 1750-1790;;;;;;

# "Zeitraum","Jahr","Autor/ Autorin","Titel","Epoche","Gattung","Stufe","URL","label_author","label_title","Vorname","Nachname","Schlagworte"
grep -v ',,,,,' input.orig.csv  | perl -pe 's/^"Zeitraum.*/id,year,author,title,epoch,genre,level,url,label_author,label_title,first_name,last_name,tags/'  | tr -s '\n' > input.csv

# get miller (mlr)
# https://github.com/johnkerl/miller/releases

mlr --c2j --jlistwrap cat input.csv > input.json

echo "INFO: fixup 10 int instead of str in json"
perl -i -pe 's/"level": 10,/"level": "10",/g' input.json

echo "INFO: json VALIDITY CHECK"
# caution: json.tool replaces umlauts TODO: find option to suppress this behaviour
# python3 -mjson.tool input.json 

# caution: false positive
# jq input2.json
# jq: error: input2/0 is not defined at <top-level>, line 1:
# input2.json
# jq: 1 compile error

# but useless use of cat / STDIN works fine though: 
# cat input2.json | jq
jq < input.json && echo "json successful validated by jq, now onto creating those html snippets..."


rm -f *.html


#time -p ./gen.html.py
