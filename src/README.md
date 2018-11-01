# User Manual

## Step 1. About the `rules.txt` file
This file contains the lexical rules defined by an alphabet and several 
regular expressions. The first line is about the alphabet, splitted by 
comma ','. Several characters are reserved: '|', '*', '&', '(', and ')'.
Also, all white characters would be ommited. The next lines are word 
categories and REs, splitted by tab '\t'. Only '*', '|', '()' and cat 
operations are supported at present. 

Define your own alphabet and categories of words as you like.

## Step 2. Generating the lexical analyser
Run `lex.py` with python3, and it would generate a file named 
`lexical_analyser.cc`. After that, type command `make` at the current 
directory. An executable named `lexical_analyser` would be generated.

## Step 3. About the `input.txt` file
This file contains all the input strings for the generated lexical analyser.
You can change the file name as you like.

## Step 4. Run lexical analyser
Just type command `./lexical_analyser [input_file]`where `[input_file]` is 
the file name of input you set at Step 3, and tokens would be output.

