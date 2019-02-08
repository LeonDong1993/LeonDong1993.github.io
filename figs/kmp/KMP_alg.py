#coding:utf-8
# KMP algorithm
# refs:
# 	https://www.zhihu.com/question/21923021/answer/281346746
# 	http://blog.csdn.net/ghost165/article/details/78231293
#	https://www.cnblogs.com/zhangtianq/p/5839909.html


# s - target string
# p - pattern
def get_next(p):
	next = [-1,0]
	i = 1 ; j = 0
	while i < (len(p)-1):
		if p[i]==p[j] or j == -1:
			i += 1 ; j += 1
			# print "Next",i,"is",j
			next.append(j)
		else:
			# print "Ret",j,"to",next[j]
			j = next[j]
	return next

def get_nextval(p):
	next = [-1,0]
	i = 1 ; j = 0
	while i < (len(p)-1):
		# print "is",i
		if p[i]==p[j] or j == -1:
			i += 1 ; j += 1
			# next[i]=j
			if p[i] == p[j]:
				next.append(next[j])
			else:
				next.append(j)
		else:
			# print "Ret",j,"to",next[j]
			j = next[j]
	return next

def kmp(S,P):
	i = 0 ; j = 0
	next = get_next(P)
	found_pos = -1
	while i < len(S) and j < len(P):
		if S[i] == P[j] or j == -1:
			i += 1
			j += 1
		else:
			j = next[j]
	if j == len(P):
		found_pos = i-j
	return found_pos


def kmp_all(S,P):
	i = 0 ; j = 0
	next = get_next(P)
	found_pos = []
	while i < len(S):
		if S[i] == P[j] or j == -1:
			i += 1 ; j += 1
		else:
			j = next[j]
		if j == len(P):
			found_pos.append( i-j )
			i =  i-j+1 ;j = 0
	return found_pos


if __name__ == '__main__':
	s = "abacaabacabac"
	p = "abacab"
	# print len(p)
	# print get_next(p)
	# print get_nextval(p)
	print kmp_all(s,p)
