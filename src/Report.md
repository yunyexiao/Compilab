# Report on lab1

## 1. Motivation/Aim
To make a simple lex which takes basic REs as input and generates a lexical 
analyzer in a .cc file. After compiling that .cc file, an executable lexical 
analyzer should be in place.

## 2. Content Description

### 2.1 The `rules.txt` file
This file contains the lexical rules defined by an alphabet and several 
regular expressions. The first line is about the alphabet, splitted by 
comma ','. Several characters are reserved: '|', '\*', '&', '(', and ')'.
Also, all white characters would be ommited. The next lines are word 
categories and REs, splitted by tab '\t'. Only '\*', '|', '()' and cat 
operations are supported at present. 

Define your own alphabet and categories of words as you like.

### 2.2 The `lex.py` file
The real src of lex in python 3. It takes `rules.txt` as input. Use *python3* 
to run the script. Aftering running, a `lexical_analyser.cc` should come out.

### 2.3 The `lat.cc` file
Lexical Analyzer Template file in *c++11* std. A template for the generated 
lexical analyzer.

### 2.4 The `lexical_analyser.cc` file
Generated lexical analyzer src file by `lex.py` in *c++11* std using `lat.cc` 
template. Use `make` command to compile.

### 2.5 The `Makefile` file
A script to compile `lexical_analyser.cc` if on Linux.

### 2.6 The `make.cmd` file
A script to compile `lexical_analyser.cc` if on Windows.

### 2.7 The `lexical_analyser.exe` file
The executable analyzer on Windows. If on Linux, use `make` to generate a 
correct executable yourself please. Type command `lexical_analyser input.txt` 
(append './' if on Linux) and tokens would be output.

### 2.8 The `input.txt` file
This file contains all the input strings for the generated executable lexical 
analyser.

### 2.9 The `Report.md` file
A document for this lab.

## 3. Ideas/Methods
1. Insert '&' into correct places of the input RE string.
2. Convert RE into postfix expression.
3. Convert postfix RE into NFA using Algorithm 3.23 defined in Dragon Book.
4. Convert NFA to DFA using Algorithm 3.20 defined in Dragon Book.
5. Copy `lat.cc` into `lexical_analyser.cc` and insert DFA data into its main 
function.

## 4. Assuptions
1. For alphabet: Cannot include '&', '|', '\*', '\\', '(', ')'. 
2. For RE: Only support '|', '\*', '(', ')' and concat operation.
3. For `rules.txt`: Alphabet should be defined only on the first line. 
Categories and REs should start from the second line. There should always 
be a '\t' between a category and a RE.
4. Only `rules.txt` and	`input.txt` can be modified.
5. Only python3 can be used to run `lex.py`.

## 5. Data Structures
1. F: Final state dict. Containing (state, category) pairs for all final 
states.
2. move: State move array. Containing all moves for all state, each move 
represented by a dict of (input char, next state) pairs. An index stands 
for a state.
3. FA: a set consisting of a starting state, an F, and a move array.

## 6. Core Algorithm
1. Algorithm 3.23 in Dragon Book to convert RE into NFA.
2. Algorithm 3.20 in Dragon Book to convert NFA into DFA.

## 7. Use Cases
rules.txt:
```
a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9
key	(a|b)*abb
hakurei	a(c|b)*dd*ee*
kirisame	mm*a*(s|t)*err*
yakumo	(ke|kaii*)*11*
kero	(kero|kaeru)(kero|kaeru)*
test0	x|y
test1	z(x|y)
test2	zz(x|y)
```

input.txt:
```
abbabaabb
kekeke1
abccbbcddddde
master
kekaiikaiiii11111
kerokerokerokaeru
zx x zzy zzx zy y
```

and the output:
```
(key,abbabaabb)
(yakumo,kekeke1)
(hakurei,abccbbcddddde)
(kirisame,master)
(yakumo,kekaiikaiiii11111)
(kero,kerokerokerokaeru)
(test1,zx)
(test0,x)
(test2,zzy)
(test2,zzx)
(test1,zy)
(test0,y)
```

