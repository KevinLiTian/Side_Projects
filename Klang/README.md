# Klang - A Modern Programming Language

A new programming language built on top of Python

## How to Use

Run the following command:

```
python shell.py
```

## Syntax

Klang is inspired by two of my favourite languages, Python and JavaScript, with some of my own flavours. It is designed to be easy to use and intuitive with its syntax just like Python. It also has some pretty JavaScript syntax like the `let` keyword to initialize a variable, and the `=>` arrow keyword to quickly define a function

### Math Operation

Math operations and numbers in Klang is basically the same as any other language. Basic operators are supported such as `+`, `-`, `*` and `/`. Power operation is also supported with `^` operator

#### Example in Klang Shell

```sh
Klang > 1 + 1
2
Klang > 1.5 - 1
0.5
Klang > 2 * 3
6
Klang > 3 / 2
1.5
Klang > 2 ^ 3
8
```

### Variables

A symbol of whether a language is a "programming language" or not is variables. Klang uses `let` keyword inspired by JavaScript to initialize variables

#### Example in Klang Shell

```sh
Klang > let a = 5
5
Klang > a + 5
10
Klang > a
5
Klang > a = a + 5
10
Klang > a
10
```

### If Statements

Klang also supports sophiscated logical conditions that are used in if-elif-else statements. Klang uses keywords `if`, `elif` and `else` like in Python with the `:` replaced by the keyword `then` which is a more easy to understand syntax. Then after the entire if statement block, Klang uses the `end` keyword to provide readability of code as they form blocks

#### Example Program

```sh
let a = 5
if (a == 6 or 3 == 4) and (3 == 3 and not 5 == 6) then
	# Will not execute this block
elif a == 5 or 1 == 2 then
	# Will execute this block
else
	# Will not execute this block
end
```

### Loops

### Functions

### Built-In Functions
