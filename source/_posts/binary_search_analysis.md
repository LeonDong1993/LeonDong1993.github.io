---
title: Analysis of Binary Search
layout: post
date: 2016-10-03 22:00
tags: [algorithm]
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "二分查找性质分析"
author: "Leon Dong"
---
## Background
Days before, I was studying the tree structure. In tree search operation, we need to find a minimum element in a node that is bigger (in this blog, bigger do not include equal) than the giving key. Since the element in tree node is ordered, therefore the idea of binary search can be used. So this problem can be simplified as follows:
> Given a sorted array and a key, how to efficiently find position of the minimum element that is bigger than key ?

At the beginning, I thought it was easy to develop a efficiently binary locate algorithm to solve this problem, but later I find that my understanding to binary search is just preliminary. In this blog, I will give you a better understanding of binary search and develop a efficiently binary locate algorithm.

## Analyze the Binary Search
There are many ways to write a binary search code, here is an example.
```c
int BinSearch(int *arr,int len,int key){
    int low=0,high=len-1,mid=0;
    while(low <= high) {
        mid=(low+high)/2;
        if( arr[mid] > key) {
            high=mid-1;
        } else if( arr[mid] < key) {
            low=mid+1;
        } else {
            return mid; /* line a */
        }
    }
    return -1; /* line b */
}
```
The idea of this classical algorithm is easy to understand, but we need to know deeply how it works. In other words, when a binary search was done. What is the value of low, mid and high? This is very important when we develop a locate algorithm based on binary search. In the next, I will give some observations and the corresponding analysis.
First, **mid is between the low and high (include low and high themselves)**. From the code above, at the first line, this claim hold true. In the later stage of this algorithm, we find that `mid=(low+high)/2`, so mid is between the low and high. Note that the value of low is bigger than high in the last if we can not find the key in array.
Second, **if key is not in array, mid is equal to either high or low**. This is because that if the key is not in array, this algorithm will return at **line b**, which means `low<=high` is not true. Since high and low will decrease or increase by 1 in each iteration, before this iteration, we have `low=high`. Under this situation, by executing `mid=(low+high)/2`, we have `mid=high=low`. Thus, mid will equal to high or low in the last no matter  `low=mid+1` or `high=mid-1` was executed.
Third, **the element array[low] is bigger than key if key is not in array**. From the deduction above, we know that in the last, low is bigger than high, therefore array[low] is bigger than array[high]. Additionally, in the last iteration, if `high=mid-1` is executed, we have arr[mid] is bigger than key. When the program return from **line b**, we have `mid=low=high+1`, therefore, `arr[low]=arr[mid]` is bigger than key.
Fourth, **the element array[high] is smaller than key if key is not in array**. Based on the above deduction, this is obvious.

Note the observation 2,3,4 are only true when key is not equal to any element in array, i.e., the program return from line b. Here is an example for you to make it clear. If we have an array as follows and we want to find 4, which is in array.


|Pos|0|1|2|3|4|5|6|
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
|Value|1|4|6|7|8|11|13|

Based on the algorithm above, we check element 7 first. Since 7 is bigger than 4, we have `low=0,mid=3,high=2` now. In the next iteration, we check the element 4. Since this element is just the one we want to find, therefore the program directly return from **line a**, and we have `low=0,mid=1,high=2`. From this example, we know that claim 2,3,4 are not true.

## Develope a Binary Locate Algorithm
From the analysis above, it is easy to implement this algorithm. We just need to modify two lines of code in the previous code.
First, if the key is in array, we know the program will return at line a, and the element array[mid] is equal to key, therefore the minimum element bigger than key is at mid+1. Second, if the key is not in array, based on the deduction above, we just need to return low. The detail code are shown as follows.
```c
int BinLocate(int *arr,int len,int key){
    int low=0,high=len-1,mid=0;
    while(low <= high) {
        mid=(low+high)/2;
        if( arr[mid] > key) {
            high=mid-1;
        } else if( arr[mid] < key) {
            low=mid+1;
        } else {
            return mid+1; /* line a */
        }
    }
    return low; /* line b */
}
```

## Another Version
As I have mentioned before, there are many ways to write to binary search. And therefore there is verious kinds of binary locate implementation. I have find another implementation and I think this one is better.
```c
int BinLocate(int *arr,int len,int key){
    int low=-1,high=len,mid=0;
    while( (low+1) < high) {
        mid=(low+high)/2;
        if( arr[mid] > key) {
            high=mid;
        } else if( arr[mid] < key) {
            low=mid;
        } else {
            return mid+1; /* line a */
        }
    }
    return high; /* line b */
}
```
Which one you is the one you like? For me, I think this one is better since this code is much more easy to read and understand (the last line `return high` clearly demonstrated the function of this code).

<!-- ### The Key Can Be Found
If the key is in array, thus the program must return at line `return mid`, what's the meaing of low and high in this situation? Actually, the value of low and high can not indicate anything.

### Key Cannot Be Found
In this situation, things turn to be different, definitely you will get -1 as return value, indicate that the key is not in the array. But this time, the value of low and high are useful. Actually, **low stands for the first element bigger than key** and **high stands for the last element smaller than key**, the **successor and precursor**, which is  very useful
For examle, if you search 0 in this array, the low will be 0 and the high will be -1, this is a special case, if you search 9, you will get low=5 and high=4, since 8 < 9 < 11
# Modification
Just make little modification to the previous code and you can get a more powerful binary search, here is a sample code in C . -->



