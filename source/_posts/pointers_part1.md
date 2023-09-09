---
title: Understanding the Pointers in C/C++
layout: post
date: 2017-04-16 16:30
tags: [c/c++]
math: 'no'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "理解C/C++指针类型"
author: "Hailiang Dong"
---

[1]: /figs/default/pointer_type.png
[2]: /2016/10/02/endian-problem/
[3]: /2017/04/15/3d-array/
## Introduction
Pointers are most frequently used variable type in programming languages like `C/C++`. In this blog, I want to share my understandings about the pointers to you. Specifically, I will tell you how pointers are saved in memory and importance of the pointer type.


## Pointers in memory
To beginning, let us talk about what is the pointers and how they are saved in memories. A straightforward explanation is that pointers are addresses and we can apply some special operations like *dereference* on them. The value of a pointer is the address of a variable the pointer points to. Here is an vivid example.

Assume we write some codes like
```c
int x = 0x1234;
int *p = &x;
```
Assume variable `x` are saved at memory address `0x233`. The following picture shows how these two variables are organized in the memory.

![pointers in memory][1]

We know that each variable will occupy some memory space. Considering the `x86_64` architecture, pointer `p` will occupy 8 Bytes and `x` will occupy 4 Bytes. In the above figure, the numbers on the top of the rectangle is the address of the variable. The numbers inside the rectangle is the value while the characters on the left of the rectangle is the name of variable.

Since `&x` is the address of the variable, the statement `int *p = &x;` will create a pointer `p` and the value of p to `0x233`. Note that in this case, the function of symbol `*` is to indicate that `p` is a pointer. Without the symbol, we will create a integer variable with value `0x233`.

Since pointer `p` is pointed to variable `x`, languages like `C/C++` provided a useful operation called *dereference*, which enables us to manipulate variable `x` using the pointer `p`. For example, the following two statements have the same function.

```c
int n1 = x+1;
int n2 = *p+1;
```
The dereference operation `*` will first read the value of pointer `p` and gets `0x233`. Then, it will read the data saved at memory address `0x233`, i.e., the value of `x`. As we can see, we can use pointer `p` just like variable `x`, just like `p` is linked (pointed) to x, and this is why `p` is called pointer.

## Importance of pointer type
As stated before, the size of pointers are always 8 Bytes in `x86_64` system no matter what the type of the pointers. So here comes a question, can I use a pointer with different type with the variable the pointer points to ? Also, what is the function of pointer type?

For the first question, the answer is yes. Sometimes, we even intentionally change the pointer types to achieve a certain goal and this is called pointer casting. However, if you carelessly altered the type of pointers, it will incur unpredictable errors in your program. I will give your some examples later in this section. Let us first talk about the function of pointer types.

We know that memory can be regarded as a large one dimensional array where the storage unit is Byte. Therefore, when you create a pointer `p` for a variable `x`, the value of pointer `p` records the address of `x` such that we can access x using the pointer `p`. However, **if we do not know the type of pointer p, how can we rightly access the variable `x` without knowing the size of `x`**. Actually, the pointer type determined the size of Bytes to read from a certain memory address. Therefore, the pointer type must be accordance with the type of the variable. Otherwise, the value may be changed when we use pointer to access the variable.

Another important aspect of pointer type is that, **when we do mathematical calculations to a pointer, the pointer type also plays an important role in it**. For example, the value of `p` is `0x233`, the value of `p+1` will be `0x237` other than `0x234` since the size of an integer is four. In other words, when pointer `p` add/minus a certain value `v`, the final value of pointer `p` is `p +/- v*sizeof(type)`. This feature is very useful when we access an array using pointers.

Next, I will give you two examples to show the importance of pointer type.

### Example 1 - wrong value
In the previous example, we create a variable `x` and a pointer `p` with the same type points to it. Now we change the type of the pointer as follows.
```c
int x=0x1234;
char *p = &x;
printf("value is %d\n",*p);
```
Now, what is the value of `*p` ? The program tells us the value is 52, i.e., `0x34`, which is totally different from the value of `x`.

The reason is that we change the type of pointer `p` to `char *`, which only allows program to read 1 Byte of data from memory address `0x233`. Since the size of variable `x` is 4 Bytes with hexadecimal representation `0x00001234`, We only read the last Byte `0x34` of variable `x`. However, the result also can be `0x00` caused by different memory manage methods. If you are interested in it, you can visit my [blog][2] to see the detailed explanation.

However, in some special cases, we do need to get the lower Bytes of a variable. Pointers can help us a lot in situation like that.

### Example 2 - null pointer
Considering the following codes.

```c
int x = 0x1234;
int **foo = &x;
printf("%d %d\n",x,*foo);
```
The programmer want to create a pointer to `x` (need a point with type `int *`). However, it mistakenly create a pointer with type `int **`, which means the variable type the pointer `foo` points to is `int *` and this is not the type of `x`.

What is interesting is that, this program gives the right output, both the value of `x` and `*foo` is `0x1234`. However, this does not mean the program is absolutely right. Since the value of a pointer `*foo` (the type of `foo` is `int*`) is `0x1234`, i.e., we can dereference the the pointer `*foo`.

```c
x = 0;
printf("%d\n",**foo); //segmentation fault
```
However, there is a huge risk. If we set the value of x to 0, then we will get an pointer `*foo` with type `int *`. Therefore, when we try to dereference the pointer `*foo`, the program will crash due to the dereference of null pointer.

## MISC

### Pointer minus pointer
Sometimes, we want to calculate the offset of a specific element in an array. Suppose we have a pointer `p` that points to the element and the head pointer `h`, a simple idea to obtain the offset is to minus the two pointers. However, based on above understandings, we know that `p = h + offset*sizeof(type)`. Therefore, here comes a question: Is `p - h == offset*sizeof(type)` ?

```c
int main()
{
	int a[5];
	int *p = &a[4];
	printf("%ld\n", p-a); //4
	printf("%ld\n", (unsigned long)p-(unsigned long)a); //4*sizeof(int)=16
	return 0;
}
```
Actually, just like add operations, the minus result between pointers will be divided by `sizeof(type)` automatically. Therefore, `p-a` is 4 other than 16. However, if we want to obtain the exact value, we can cast the pointer to `unsigned long` and then employ the minus operation on two integers.

### Pointer cast
We can use pointer cast to do a lot of interesting things. Here is an example that using pointer cast to divide an long into a char array.
```c
long val = 0x0123456789ABCDEF;
char *p = &val;
for(i=0;i < sizeof(long);i++){
    printf("%c",p[i]);
}
```
Also, at [this blog][2], shows an fast algorithm used to judge if the bitmap is fully occupied by using the technique of pointer cast.

### 2-D array
In [this blog][3], I talked about how to create N-dimensional array in `c/c++`. However, we need to understand why the type of the head pointer of a 2-D array is `int **`.
The principle behind it is very simple. Suppose we have multiple 1-D arrays. As stated before, the name of these 1-D arrays are pointers (such as `int *`). Therefore, in order to create an 2-D array, we just need to organize this head pointers in a 1-D array. Since the element in this array is `int *`, the head pointer of the 2-D array should be `int **`, which means that it contains multiple 1-D arrays (`int *`).