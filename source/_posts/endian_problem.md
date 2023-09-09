---
title: Endian Problem in Coding
layout: post
date: 2016-10-02 10:00
tags: [c/c++,coding]
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "编程中的大小端问题"
author: "Leon Dong"
---

## Introduction to Endian
As we know, the storage unit of modern computer system is `Byte` and each byte is 8-bit long. Most of the programming language have integer varible type that have the size of more than one byte. What's more, for processor which can process more than 8-bit size of data in one instruction, how to save data in memory becomes a problem.
To solve this problem, there are two kinds of formats proposed. The first one is call `Big Endian` and the other one is called `Small Endian`. Specifically, Big endian save the integer from higher bits (treat it like a string) while the small endian save the number from lower bits. To better understand the difference between this two formats. Let me give you an vivid example, suppose we have a hexadecimal number **0x12345678** , suppose the number is saved at address 0x100, the following table shows the difference between these two types.

| Address | 0x100 | 0x101 | 0x102 | 0x103 |
|:-------:|:-----:|:------:|:-----:|:-----:|
| Big Endian | 0x12 | 0x34 | 0x56 | 0x78 |
| Small Endian | 0x78 | 0x56 | 0x34 | 0x12 |

Just as the table shows, Big endian seems to be natural than small endian, treat it like a string. All the network protocol use Big endian to transfer data and big endian is easier for sorting algorithm (since we only need to check whether or not the higher bits of A is bigger than B).

Small endian seems kind of weird  to some extent, but it also have lot of [advantages][1] and is widely employ in Intel X86 CPU.
<!-- seems like the digital image processing -->

- if you want to get the lower bytes of an integer (simplely by casting a pointer), small endian system do not need to increase the pointer. In short, **cast in little endian system is treated as no-op**
- addition and subtraction can be done easier since we should begin add or subtraction from less significant bit to see if there is a carry.
- a lot of algorithms just naturally start working at the least significant end (such as addition), and want those ends to be matched.

## The Effects of Endian on Coding
Actually, in most of situations, endian will do nothing to you program. However, when you are using techniques like pointer casting in some programming language like `C`, you need to care about the endian type of you machine.

Here is an example that how endian affect my program and this is also how I find endian is important. I was implementing a simple algorithm to check if a 252 bits bitmap was full. Since 252 is not a multiple of 8, I use an array consist of 32 Bytes to save the bitmap. Therefore, I have 4 bits unused in bitmap, and this is also the key factor leads to a bug in my code.

Here is an efficient way to detect if all the 252 bits is valid (equal to one),
```c
int is_full(Byte *bmp)
{
    long *foo=(long *)bmp;
    if( foo[0]==0xFFFFffffFFFFffff &&
        foo[1]==0xFFFFffffFFFFffff &&
        foo[2]==0xFFFFffffFFFFffff &&
        foo[3]==0xFFFFffffFFFFfff0  ){
        return 1;
    }else{
        return 0;
    }
}
```
Is this code right? Actually it works on big endian machine, but unfortunately my computer was based on intel x86 architecture. Thus, this function keep returning 0 and finally my program was crashed. This is because that in small endian machine, **foo[3] equals 0xf0ffFFFFffffFFFF**.

## Get Endian Type of Your Computer

Based on the introduction above, it is easily to design a program to see which type of your machine is, and the following is an example written by `C`.

```c
int isBigEndian (void) {
    int digit = 0x12345678;
    if ( *(char *)&digit == 0x78 ) {
        return 0;
    } else {
        return 1;
    }
}
```

[1]:http://programmers.stackexchange.com/questions/95556/what-is-the-advantage-of-little-endian-format/95587