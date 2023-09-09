---
title: BUG-Crash When Calling Function
layout: post
date: 2017-04-08 17:00
tags: [coding,c/c++]
math: 'no'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "BUG-调用函数就崩溃"
author: "Hailiang Dong"
---

[1]: https://en.wikipedia.org/wiki/Call_stack#Subroutine_entry_processing


## Background
Recently, one of my teammate asked me to help him to debug a program. The behavior of the program was so strange that makes him unable to identify the bugs in it. The bug is caused by stack overflow. Since I have also encounter several cases like that, I decide to write this blog to analyze these programs and help you to understand the program in a system level. These types of bugs are hard to debug even if you utilize the debug mode provided by the IDE since **the debugger cannot tell you which line of code causes the crash of the program**. We need to analyze the program in a system level.
<!-- Actually, his program causes the stack overflow  -->
<!-- After minutes of debugging, I found the bug in his program, which was caused by stack overflow. This made me recall other  -->

## A Real Instance
In this section, I will show an example code a bug that will cause the program crash when invoking a specific function. Here is the code, some irrelevant details are omitted.

```c
#include <stdio.h>
#define MAX_LENGTH 100

void SCS_3(){
	printf("2\n");
	int i;
	int scs[MAX_LENGTH][MAX_LENGTH][MAX_LENGTH]={0};
	// .......
	return;
}

int main(){
	char buffer[MAX_LENGTH];
	read_string(buffer);
	printf("1\n");
	SCS_3();
	return 0;
}
```
Two `printf` statement are used for debugging. However, the program crashed with **only 1 printed** in the console. At the beginning, I thought the bug was in the function `read_string`. The buffer might be too small to hold the input and causing the buffer overflow. Consequently, the entrance address of the function `SCS_3` might be changed to an invalid memory address, which will cause the program crash down.

Unfortunately, this is not the case. After I commented those codes in the program, the bug is still there. And I quickly noticed that the bug must be in function `SCS_3`. Since the statement `printf("2\n");` is not successfully executed, the error should occurred in the initial process of this function. Actually, the bug is caused the third line in function `SCS_3`. The programmer created a local variable, which is a three dimension array (this is not a good coding habit, since this program is just for testing, the programmer took a shortcut). Notice that the local variables are store in the stack, and this leaves an hidden trouble in the initial process of the function. Next, I am going to analyze the bug in detail, which will involve some facts about how the system handle the function invoking, if you are not very clear, you can visit [Wiki][1] for help.

In a matter of fact, when the function `main` attempt to invoking function `SCS_3`,some prologue codes must be executed first. Specifically, it will save the return address (the address of main function) and the frame pointer into the call stack. Next, the prologue code will **allocate the memory space for parameter and local variables** in stack and change the stack pointer if needed. If all works correctly, the function are ready to run. Since **the local variable `scs` is too large, which has `1MB`, for stack, the stack overflowed in the initial process** and therefore the program crashed down.

It is easy to fix this bug, we can allocate the three dimension array `scs` in the heap using dynamic allocation method. However. it is not very easy to crate a 3-D array in programming language like `C`, in the next blog, I will introduce a general way to create multi-dimensional array.

<!-- If frame pointers are being used, the prologue will typically set the new value of the frame pointer register from the stack pointer. Space on the stack for local variables can then be allocated by incrementally changing the stack pointer. -->