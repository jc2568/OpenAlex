#!/bin/bash

### Author: Joshua Chu
### Data: January 25, 2023

### This bash script was written to clean up the file prior to pass it to the cleanparas.pl script
### that is used for the final clean prior to terracing the data.

### Command structure: sh finalProcessing.sh


### sets the file as a variable
file="./openalexoneline.tsv"

### pipes the sed commands and lowercase strings in a single command. The output file is the input
### for cleanparas.pl
sed -e 's/"//g' $file | sed -e 's/\$//g' | sed -e 's/{//g' | sed -e 's/}//g' | sed -e 's/(//g' | sed -e 's/)//g' | sed -e 's/\[//g' | sed -e 's/\]//g' | sed -e 's/\\\\//g' | \
     sed -e 's/\*//g' | sed -e 's/\^//g' | sed -e 's/@//g' | sed -e 's/\\//g' | sed -e 's/\"//g' | sed -e "s/'//g" | sed -e 's/\///g' | sed -e 's/\‘//g' | sed -e 's/\’//g' | \
     tr '[:upper:]' '[:lower:]' > openalexlower.tsv

