


def check_tidy(n):
    n = str(n)
    m = sorted(n)
    m = ''.join(m)
    if n == m:
        return True
    else:
        return False

def main(n):
    strn = str(n)
    idx = -1
    while True:
        if int(strn[idx-1]) > int(strn[idx]):
            a = strn[idx]
            strn = strn[:idx-1] + a + strn[idx:]
        else:
            a = str(int(strn[idx]))
            strn = strn[:idx-1] + a + strn[idx:]
        idx -= 1
        if idx == -len(strn)+1:
            break
    print strn


def io(inp, out):
    f = open(inp, 'r')
    out = open(out, 'w')
    n = int(f.readline())
    for i in xrange(n):
        l = f.readline()
        print l
        out.write('Case #%d: ' %(i+1))
        ans = main(int(l))
        out.write(str(ans) + '\n')

io('B-large.in', 'b_large_ans.txt')

