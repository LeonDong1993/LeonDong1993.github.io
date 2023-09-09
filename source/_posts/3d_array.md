---
title: Dynamically Create N-D array in C
layout: post
date: 2017-04-15 21:30
tags: [coding,c/c++]
math: 'yes'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "C语言里面动态创建N维数组的方法"
author: "Hailiang Dong"
---

[1]: /figs/default/3d_array.png

## Traditional way
In a C program, If we want to create an N-dimension array in heap (dynamically), we need to allocate the memory space step by step. For instance, if we want to create an 3-D array, we can use the code below.

```c
int ***create_3d_array(int len1,int len2,int len3)
{
    int i,j,k;
    int ***array3 = (int ***)malloc(sizeof(int **) * len1);
    for (i=0;i<len1;i++){
        array3[i] = (int **)malloc(sizeof(int *) * len2);
        for (j=0;j<len2;j++){
            array3[i][j] = (int *)malloc(sizeof(int) * len3);
        }
    }
    return array3;
}
```

What you need to understand is the type of pointer in each step. If the type is wrong, it will incur unpredictable errors (may be in my future blog will talk about this issue). Therefore, for a novice in c/c++ programming, it is not easy to write a function to create N-dimension array.

## An alternative way
Actually, we can allocate an one dimensional array with the same size. After that, if we want to access the N-dimension array, we first calculate the offset in the 1-D array. Let us take 3-D dimensional array as an example.

Assume the size of 3-D array is 8,9 and 10, respectively. Then we use the following code to create an one dimensional array with the same size.

```c
int *arr = (int *)malloc(sizeof(int)*8*9*10);
```

After that, if we want to set the value at (3,4,5) to 10, we first calculate the offset. In other words, what is the corresponding position in the 1-D array for the element (3,4,5) in 3-D dimensional array. Through simple mathematic calculation, we can get the offset by calculate `3*9*10 + 4*10 + 5`. Generally, if we have a N-dimension array and the size of each dimensional is denoted as $(l_1,l_2,...,l_n)$, the offset for element $(i_1,i_2,...,i_n)$ is

![the formula][1]

You can use the program below to verify the correctness of this way.
```c
#include <stdio.h>
#include <stdlib.h>
#define MALLOC(n, type) ( (type *) malloc((n)* sizeof(type)))
#define SET_ELEM(arr,l1,l2,l3,i,j,k,val) ( arr[ (( (i)*(l2) )+(j) )*(l3) + (k)] = val)
#define READ_ELEM(arr,l1,l2,l3,i,j,k,val) ( val = arr[ (( (i)*(l2) )+(j) )*(l3) + (k)] )

int main()
{
    int ***a3d = create_3d_array(8,9,10); // 3-d
    int *linear3d = (int *)malloc(sizeof(int) * 8*9*10); // 1-d
    int i,j,k;
    int val = 0;
    for(i=0;i<8;i++){
        for(j=0;j<9;j++){
            for(k=0;k<10;k++){
                a3d[i][j][k] = val;
                SET_ELEM(linear3d,8,9,10,i,j,k,val);
                val++;
            }
        }
    }

    READ_ELEM(linear3d,8,9,10,7,3,7,val);
    printf("3D val is %d\n",a3d[7][3][7]);
    printf("1D val is %d\n",val);

    return 0;
}
```

## Comparison
For the traditional way, it is much hard to initialize an N-dimension array. However, it is more efficient since we can directly access the element. For the alternative way, since we need to calculate the offset when access a certain element, it is applicable when the dimension is not very big, such as 2 or 3 dimensions.