#!/bin/bash
git rm *.html && cp ../*.html . && git add * && git commit -m 'test' && git push
