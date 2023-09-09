---
title: Find Majority Element in Linear Time
layout: post
date: 2019-2-8 13:58:04
tags: [algorithm]
math: 'yes'
cdn: 'header-off'
header-img: "/imgs/default-post-cover.jpg"
subtitle: "线性Majority查找算法"
author: "Hailiang Dong"
---

## Problem Description
**Input**: an array of elements with size $N​$, and there exists an element $M​$ accounts for more than 50% of the array (called Majority). In other words, the number of $M​$ in the array is at least $\lfloor \frac{N}{2}\rfloor+1​$.

**Output**: find the element $M$.

## Linear Time Algorithm
The idea of this algorithm is to scan the whole array and record the current majority candidate and a counter.

Initially, the candidate is set to the first element is the array and the counter is 1. Then, we go through each element in the array.
- If the  counter is  zero, set the counter to 1 and the candidate majority to this element
- If counter is not zero and current element equals the candidate majority, increase the counter by 1
- If counter is not zero and current element is not the same with the candidate majority,  decrease counter by 1

When we have done this scan, the final candidate majority is guranteed to be the majority of the whole array.

Here is a sample code write in python.
```python
def FindMajority(array):
	candidate = array[0]
	counter = 1
	for elem in array[1:]:
		if counter == 0:
			counter = 1
			candidate = elem
		else:
			if candidate == elem:
				counter += 1
			else:
				counter -= 1
	return candidate
```

## Proof of Correctness
The algorithm seems to easily come up with, but why is correct?
To analysis this algorithm, we consider two cases:
1. the counter never decrease to 0
2. the counter goes to 0 at some point

For the first case, it is obvious that the first element is the majority we want to find. For the second case, we begin with analyze the first time that the counter decrease to zero. Assume this event occurs at step t.  In this case, the number of $M$ in array[1:t] is at most $\frac{t}{2}$. This can be proved by contradiction.

Therefore, when the counter goes to zero at first time, the length of the rest array is $N-t$, while there exists at least $\lfloor \frac{N}{2}\rfloor+1 - \frac{t}{2}$ elements. Note that $t$ must be an even number, we have
$$
\lfloor \frac{N}{2}\rfloor+1 - \frac{t}{2} = \lfloor \frac{N-t}{2}\rfloor+1
$$
This means $M$ is still the majority for the  array[t+1..N].

When the counter goes to zero for the second time, we will have the same analysis as above. Finally, there must exist $i$, such that the counter is 0 at step $i$, but the counter will never goes to zero again at array[i+1:N].

## A Similar Problem

The above problem asks you to find the majority element in a given array, where each element is known by advance.
**What if we are give a bunch of elements that are unknow (but we can determine whether two of them are same in constant time) ? **
Actually, the same strategy can be applied here, we just randomly pick an element to start with and determine whether the rest is  same with this element.

## Reference
1. https://www.cs.utexas.edu/~moore/best-ideas/mjrty/example.html
2. https://www.quora.com/What-is-the-proof-of-correctness-of-Moores-voting-algorithm