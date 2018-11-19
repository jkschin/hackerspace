def inv(c):
    if c == '+':
        return '-'
    else:
        return '+'

def flip(pancakes, i, j):
    edit = ''
    for k in xrange(i, j):
        edit += inv(pancakes[k])
    return pancakes[:i] + edit + pancakes[j:]

def check(pancakes):
    for p in pancakes:
        if p != '+':
            return False
    return True

def greedy(pancakes, k):
    idx = 0
    count = 0
    while True:
        if pancakes[idx] == '-' and idx+k <= len(pancakes):
            pancakes = flip(pancakes, idx, idx+k)
            count += 1
        idx += 1
        if idx == len(pancakes):
            break
    if check(pancakes):
        return count
    else:
        return 'IMPOSSIBLE'

def io(f):
    f = open(f, 'r')
    out = open('a_large_ans.txt', 'w')
    n = int(f.readline())
    for i in xrange(n):
        out.write('Case #%d: ' %(i+1))
        l = f.readline()
        l = l.split()
        ans = greedy(l[0], int(l[1]))
        out.write(str(ans) + '\n')

io('A-large.in')

