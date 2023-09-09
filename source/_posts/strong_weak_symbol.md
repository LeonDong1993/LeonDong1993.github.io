---
title: Strong and Weak Symbols in GCC
layout: post
date: 2017-04-15 09:30
tags: [coding,c/c++]
math: 'no'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "GCC里面的强符号和弱符号"
author: "Hailiang Dong"
---

[1]: https://en.wikipedia.org/wiki/Call_stack#Subroutine_entry_processing

## Motivation

Global variables are powerful but have the risk of being altered carelessly. Under most cases, we can add `static` modifier on this global variables such that these variables can only be altered in the file. However, there do have some situations that we have to use global variables across different files. In this case, we usually encounter an error happened in linking phase, i.e., `error:multiple definition`. Some of these errors are obvious and easily to debug while others can be really puzzling. Here I will give you an example that I encountered.

Suppose we have two source files, and the content is
```c
#include <stdio.h>
// main.c
int gvar;
int main(){
	printf("shared var is %d\n",gvar);
	return 0;
}
```
```c
// aux.c
int gvar = 5;
```
then we run the command
```
gcc -o test main.c test.c
```
and everything goes smoothly. That is to say, the code presented is correct, variable `gvar` is not `multiple definition`. Note that there is no `extern` modifier for `gvar` and the result of this program is 5, which means that the variable `gvar` is shared across two files. This is quite strange since we know that if two global variable have the same name in a project, it will incur `multiple definition` errors.

What is more, I found something more interesting. When we change the postfix of these two files,
```
mv main.c main.cpp
mv test.c test.cpp
gcc -o test test.cpp main.cpp  #error:multiple definition
```
the compiler told me that there is a `multiple definition` error for variable `gvar`. How does this happen, the content in the files are not changed and we only changed the file name. An intuitive explanation is that the different of `c++` and `c` cause the puzzling bug since `.cpp` is the file type for `c++` and `.c` is for `c`.

## Strong and weak symbols
Actually, these strange phenomenons are all caused by one features provided by GCC, called strong and weak symbols. For global variables, it was divided into three types.

- initialized to a non-zero value
- initialized to zero
- not initialized, just defined

In GCC, the first two types of global variables is called strong symbols that are store in `.DATA` and `.BSS` section. As for the third type, it is called weak symbols, and **it is saved in `.COMMON` section**.

There are three rules that must be followed for these variables

- only one strong symbol is allowed with the same name
- if there exists one strong symbol and several weak symbols, the weak symbols are overrode by strong symbols
- if there exists several weak symbols, GCC will choose one that have the largest size (memory occupation).

Now we can clarify why the c version program can run without any errors. In `aux.c`, we define a strong symbol `gvar` and it is initialized to 5. In `main.c`, we only define the variable `gvar`, and it is a weak symbol. When we compile the program using GCC, the `gvar` in `main.c` is overrode by `gvar` in `aux.c` according to the second rule. Therefore, the program runs smoothly and the result is 5. If we change the `main.c` as follows, it will incur `multiple definition` also.

```c
#include <stdio.h>
// main.c
int gvar=0; // this is a strong symbol
int main(){
	printf("shared var is %d\n",gvar);
	return 0;
}
```
Wait, there is still one puzzling problem left. Why the program incurs `multiple definition` error when the file name is changed ?
Actually, when we change the file type from `.c` to `.cpp`, the GCC compiler will use the rules for `c++` problem to compile this c program. Therefore, to answer this question, we need to investigate the difference when GCC handle the strong/weak symbol between `.cpp` and `.c`.

Here is my conclusion. For c program, if you define an global variable and not initialize it, GCC will regard it as weak symbol. However, for `c++` program, the default type is strong variable. That is to say, for line `int gvar;` in `main.cpp`, it is a strong symbol. Since we have another strong symbol with the same name in `aux.cpp`, the compiler gives the error.

If you want to use weak symbol in a `c++` program, you need to explicitly declare the variable is weak. For example, if we write a `c++` program like this,

```c
#include <stdio.h>
// main.cpp
int __attribute__((weak))  gvar=2;
int main(){
	printf("shared var is %d\n",gvar);
	return 0;
}
```
```c
// aux.cpp
int gvar = 5;
```
the program will have the same behavior like the c version.

To avoid the bugs like that, we can use the `-fno-common` option provided by GCC, it will regard all variables as strong symbols. However, in some cases, we have to use weak symbols (see next section). Therefore, we should develop a good coding habit. There are three rules we can follow,

- eliminate all global variables (hard)
- add `static` modifier for global variables, provide interfaces for accesses (medium)
- initialize all global variables, such as zero (easy)

## Function of s. w. symbols
It seems that we should use strong symbols instead of weak symbols in programming, so why does GCC provide weak symbols? As far as I known, weak symbols are useful for library functions. For example, if the symbols in library are weak symbols, users can easily override some library functions for personal objectives. What's more, programmers can declare some weak symbols of library functions. If the program is linked with the library, program can provide more powerful features, Otherwise, the program can still run without any errors. Here is a simple example.

```c

#include <stdio.h>
#include <pthread.h>

__attribute__((weak)) int pthread_create( pthread_t*, const pthread_attr_t*,
	void*(*)(void*), void*);

int main()
{
	if (pthread_create)
	{
		printf("This is multi-thread version!\n");
	}
	else
	{
		printf("This is single-thread version!\n");
	}
	return 0;
}
```
If the program is not linked with `pthread` library, it will run in single-thread mode. Otherwise, it can run in multi-thread mode.

## Manage your global variables
If you have to use global variables, here is an way to manage your global variables in an comfortable way. Create two files called `global_var.h` and `global_var.c`. Declare all global variables using `extern` modifier in `global_var.h`. Initialize all global variables in `global_var.c`. For instance,
```c
// global_var.h
#ifndef   GLOBAL_VAR
#define   GLOBAL_VAR
extern int  g_A;
extern char g_B;
#endif
```

```c
// global_var.c
int  g_A = 0;
char g_B = 'g';

```
When you need to use global variables in other files, such as `main.c`, simple include `global_var.h` and you will be able to access all global variables.


```c
// main.c
#include <stdio.h>
#include <global_var.h>
int main(){
	printf("var is %d\n",g_A);
	return 0;
}
```
Through this way, you can easily manage your global variables. However, **be sure to use global variables as less as possible**.

## Reference

http://www.bitscn.com/CL/741921.html
http://blog.csdn.net/astrotycoon/article/details/8008629
http://blog.csdn.net/hu_jiacheng/article/details/8800540