# Klang - A Modern Programming Language

A new programming language built on top of Python

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

Klang supports `for` and `while` loops as any other languages. `for` loop uses `to` and `step` to determine the conditions of the loop. Both loops uses `do` keyword to specify which statements to execute each iteration. And Klang also supports `continue` and `break` within a loop, and uses `end` to end the block to provide readability. The syntax is as follows:

```sh
let a = []
for i = 1 to 20 step 2 do

	if i == 5 or i == 15 then
		continue
	end

	if i == 17 then
		break
	end

	append(a, i ^ 2)
end

while len(a) do
	pop(a, 0)
end
```

### Functions

I personally prefer functional programming. Klang supports two ways of defining a function, either by using the `=>` keyword inspired by JavaScript or plain `return` statement.

```sh
fun add(a, b)
	return a + b
end

fun mul(a, b) => a * b
```

### Built-In Functions

Klang provides some useful built-in functions, one you've seen so far is `len()` which outputs the length of an array. Some other built-in functions and variables are:

- `NULL`: Integer 0
- `TRUE`: Interger 1
- `FALSE`: Interger 0
- `PI`: Mathematical constant 3.1415926...
- `say(x)`: Prints `x` to the console
- `input()`: Takes in user input
- `clear()` & `cls()`: Clear the console
- `is_num(x)`: Returns boolean of whether `x` is a number or not
- `is_str(x)`: Returns boolean of whether `x` is a string or not
- `is_func(x)`: Returns boolean of whether `x` is a function or not
- `append(list, element)`: Adds an `element` to the end of a `list`
- `pop(list, idx)`: Removes an element at index of `idx` in a `list`
- `extend(list1, list2)`: Merges two lists as one list
- `len(list)`: Returns the length of the `list
- `run(program)`: Interprets an external Klang program

## How to Use

Run the following command:

```
python shell.py
```

To run the example program, run the following command in the Klang shell:

```sh
run("example.klang")
```
