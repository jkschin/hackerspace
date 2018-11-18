
def get_max(N, seq):
    window = N / 2 + N % 2
    seq = [int(i) for i in list(seq)]
    cur_window = sum(seq[0: 0 + window])
    max_vals = [cur_window]
    for i in xrange(1, len(seq) - window + 1):
        cur_window -= seq[i-1]
        cur_window += seq[i+window-1]
        max_vals.append(cur_window)
    return max(max_vals)

inp_filename = 'B-small-attempt0.in'
out_filename = 'B-wtf.out'
inp = open(inp_filename, 'r').read().split('\n')
out = open(out_filename, 'w')
T = int(inp.pop(0))
for i in xrange(T):
    N = int(inp.pop(0))
    seq = inp.pop(0)
    ans = get_max(N, seq)
    out.write('Case #%d: %d\n' %(i + 1, ans))

