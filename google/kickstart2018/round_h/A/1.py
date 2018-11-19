def double_for_loop(F):
    base = F.pop(0)
    l = len(base)
    ans = [base]
    rmd = []
    for j in xrange(len(F)):
        compare = F[j]
        if base == compare[:l]:
            pass
        else:
            rmd.append(compare)
    return ans, rmd

def preproc(F):
    f_ans = []
    F = sorted(F, key=len)
    while len(F) != 0:
        ans, F = double_for_loop(F)
        f_ans += ans
    return f_ans

def fn_1(N, F):
    total = 2 ** N
    for seq in F:
        total -= 2 ** (N - len(seq))
    return total

f = open('A-large.in', 'r')
f = f.read().strip().split('\n')
output = open('1_large.txt', 'w')
T = int(f.pop(0))
for i in xrange(T):
    NP = f.pop(0)
    N, P = NP.split(' ')
    N, P = int(N), int(P)
    F = []
    for j in xrange(P):
        F.append(f.pop(0))
    F = preproc(F)
    ans = fn_1(N, F)
    output.write("Case #%d: %d\n" %(i+1, ans))
    # print fn_1(N, P, F)

