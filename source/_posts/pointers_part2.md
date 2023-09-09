---
title: Understanding the Pointers Advanced
layout: post
date: 2017-05-06 09:30
tags: [c/c++]
math: 'no'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "理解C/C++指针类型进阶"
author: "Hailiang Dong"
---

[1]:/2017/04/16/pointers-01/

## Introduction
This blog is the second one that talking about the pointers. In the [previous one][1], I talked about what is the pointer and why the type of pointers is very important. In this blog, I want to talk about the mysterious relationship between the pointer and the array.


## The name of the array
In `C/C++`, when we create a array like `int a[6]`, what is the name `a` means? Actually, `a` is the address of the first element and can be use like a pointer. For example,

```c
int a[6];
```
Here, `a` is just like a pointer. If we want to access the third element in this array, we can use `*(a+3)` instead of using `a[3]`. Similarly, we can use the following codes to traverse the whole array.
```c
for(i=0;i<6;i++){
    foo = *(a+i);
}
```
However, the following way is wrong.
```c
for(i=0;i<6;i++){
    foo = *a;
    a++; //error
}
```
This is because that `a` is a constant value, which cannot be altered. But we can create a pointer 'p' and do traverse like the code above.
```c
int *p =a;
for(i=0;i<6;i++){
    int foo = *p;
    p++; //actually plus 4
}
```
Note that `a` is already a pointer (address), and we create a pointer `p` points to the same address like `a`.

### `a` is not a pointer
As stated before, `a` is the address of the first element and it can used like a pointer. However, it is not a pointer. We can use two different methods to verify the fact.

```c
int main()
{
	int a[6];
	int *p = a ;
	printf("%d %d\n",sizeof(a),sizeof(p)); // -- A
	printf("%p %p %p\n",a,&a, &p); // B
	return 0;
}
```

Execute the code above in any 64-bit machine, at line A, you will get output `24 8`. It indicated that `a` is not a pointer otherwise the size of `a` should be `8`. Another evidence can be found at line B, the first two address are same while the third are different from that. On my computer, it gives the output `0x7ffee2b8edb0 0x7ffee2b8edb0 0x7ffee2b8eda8`. It indicates that `a` cannot be a pointer otherwise `&a` and `a` must have different addresses just like `&a` and `&p` since two variables cannot have the same address.

### `a` and `&a`
From the above example, we found another puzzling fact: `a` and `&a` have the same address. What does this mean ? In fact, `a` is the address of the first element and `&a` is the begining address of the whole array. Therefore, they must have the same value but there are some important difference we need to know.

First, it is about the element type. For `a`, it is an address of `int` element, therefore we can create a pointer `int *p =a;`. For `&a`, it is an address of the whole array, if you still using `int *p = &a;`, the compiler will give you a warning says `initialization from incompatible pointer type`. In other words, the type of `&a` is not `int *`. Actually, we need a pointer point to the whole array other than the single element, i.e., `int (*p)[6] = &a;`. Here, we call `p` as array pointer.

The difference in type leads to the difference when conducting add/minus operations.

```c
int a[5]={1,2,3,4,5};
int *ptr=(int *)(&a+1);
printf("%d,%d",\*(a+1),\*(ptr-1));
```
The output of this program is `2 5`, let me tell you why. It is easy to understand that `\*(a+1) = 2 ` but why `\*(ptr-1)` is 5 other than 1. The reason is that `&a+1` differ from `a+1`. As stated before, `&a` is a pointer points to the whole array. Therefore, when calculate `&a+1`, the actual address is `a + sizeof(array) = a + sizeof(int)*5`.
Since `ptr` is casted into `int *` type, `ptr -1` equals `a + sizeof(int)*4`, i.e. the address of element `a[4]`.

Last, when using array pointer to traverse the array, the right way is using `(*p)[i]`. Do not use `p[i]` since it equals `*(p+i)`. Since `p+i` is actually `p+i*sizeof(array)`, it is definitely not right!


### Pointer array and array pointer
Many people cannot distinguish between array pointer and pointer array. With the above understandings, let us talk about some difference between pointer array and array pointer.

```c
int main()
{
	int *p_arr[5]; // pointer array
	int arr[5]; //normal array
	int (*arr_p)[5] = &arr; // array pointer
	printf("%ld %ld\n", sizeof(p_arr),sizeof(arr_p));
	printf("%p %p\n", p_arr+1 ,arr_p+1);
	return 0;
}
```
First, it is about the size. Pointer array is an array contains a lot of pointers while array pointer is just a pointer points to an array. Therefore, pointer array occupies more memory space than array pointer. In the above example, the size of `p_arr` is `5*sizeof(int *) = 40` while the size of `arr_p` is only 8 bytes.

Second, it is about the add or minus operations. For example `p_arr+1` is the address of the second element in the `p_arr` while `arr_p+1` directly points to the address `arr + 6`, which already exceed the range of `arr`.

Actually, array pointers are often used in 2-D array.
```c
int main()
{
	int a[2][2]={{1,2},{3,4}};
	int (*p)[2] = a;
	printf("%d\n", (*p)[0]);
	p = p +1;
	printf("%d\n", (*p)[0]);
}
```
In this example, the output is `1 3` and `a` is a 2-D array contains two rows. In line 2, we create a pointer points to one row (a element in 2-D array) of `a`. Since `a` is the address of the first element (a 1-D array), we do not need `&a` in this example. In line 3, we print the first element in the first row. In line 4, we move the pointer `p` points to the second row. In line 5, we print the first element of the second row, which is 5.

### An error caused by initialization

```c
int main()
{
   int a[3][2]={(0,1),(2,3),(4,5)};
   int *p;
   p=a[0];
   printf("%d",p[0]);
}
```

The right result of the program is 1 other than 0 since the programmer use `()` in initialization process. Actually, in this example, `a[3][2]={(0,1),(2,3),(4,5)}` equals `a[3][2] ={1,3,5}`.


## Declaration and definition
When a project contains multiple files, if we define a array in file1 but declare it as a pointer in file2, what will happen?

### Defined as an array and declared as a pointer
```c
//file1.c
int arr[4]={10,9,8,7};
//file2.c
extern int *arr;
printf("%d\n", arr[0];
```
In this case, in file2, when we access `arr[0]`, what is the detailed process ? We all know that we when access `p[0]`, it is same to access the address that `p` points to. In this example, what is the address `arr` points to ? Actually, it is `10` (32-bit system). Therefore, when we want to access `arr[0]`, the program crashed.

### Defined as an pointer and declared as a array
```c
//file1.c
char *p = "abcdefgh";
//file2.c
extern char p[];
printf("%d\n", p[0];
```
In this example, in file1, suppose the value of `p` is `0x12345678`, i.e., constant string `abcdefgh` is saved at address `0x12345678`. In file2, when we access `p[0]`, since compiler regard it as a char array with value  `0x12345678`, therefore, we have `p[0] = 0x12`.

These two examples tell us that pointer and array are two different things. Although they have some similarities, they are different in various aspects.


## Pointer function and function pointer
Pointer function is a special kind of function that return pointers. For example,
```c
int *get_array(int size)
{
	return (int *)malloc(size);
}
````

Function pointer is a point that points to a function. Just like array pointer, it is just a special kind of pointers.
```c
void fun1(){
	printf("A\n");
}
void fun2(){
	printf("B\n");
}
int main()
{
	void (*fp)(void);
	fp = fun1; // ok
	fp();
	fp = &fun2; // ok
	fp();
	return 0;
}
```
In this example, I create a function pointer `fp`. Then, we can let `fp` points to either `fun1` or `fun2`. Note that for functions, `fun` and `&fun` are both the entrance address of the function, they are the same.

## Array as the parameter
In `c` language, the array cannot be passed into the function. We can only pass the pointer into the function.
For example, when we defined a function `void fun(char a[3][4]);`, the parameter `char a[3][4]` can also be rewritten as `char (*p)[4]` or `char a[ ][4]`.
Note that it cannot be rewritten as `char a[][]`, otherwise when we do `a+1`, compiler will not know how to calculate the real address.

All in all, in `c` language, the size of the first dimension can be omitted, but not for any other dimensions.

## Reference
http://c.biancheng.net/cpp/u/cjinjie4/