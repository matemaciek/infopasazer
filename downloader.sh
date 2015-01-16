#!/bin/bash
wget "$1" -O ip.html
grep productsFilter ip.html -A6 | python processor.py
