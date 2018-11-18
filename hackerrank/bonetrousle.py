def bonetrousle(n, k, b):
    # Initialize smallest set.
    answer = [i for i in range(1, b + 1)]
    total = sum(answer)
    if total == n:
        pass
    elif n < total:
        answer = [-1]
    else:
        difference = n - total
        i = len(answer) - 1
        delta = k - answer[i]
        while delta <= difference:
            answer[i] += delta
            i -= 1
            difference -= delta
        answer[i] += difference
    return answer

f = open('bonetrousle_6.txt', 'r')
n = int(f.readline())
for _ in range(n):
    line = f.readline()
    n, k, b = map(lambda i: int(i), line.strip().split())
    print "Parameters: ",n,k,b
    print bonetrousle(n, k, b)
    # print sum(bonetrousle(n, k, b))

