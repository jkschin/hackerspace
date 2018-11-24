# There was a timeout on the initial code. That's because I used a different way
# to get the counts of 1s in the binary string. Turns out that it is
# ridiculously inefficient and a few methods are explored in test_speed.py
def acmTeam(topic):
    dic = {}
    for i in xrange(len(topic)):
        a = int(topic[i], 2)
        for j in xrange(i+1, len(topic)):
            b = int(topic[j], 2)
            # This was the line that TLE.
            c = bin(a | b)[2:].count('1')
            if c not in dic:
                dic[c] = 1
            else:
                dic[c] += 1
    max_subs = max(dic.keys())
    max_teams = dic[max_subs]
    return [max_subs, max_teams]

f = open('acm-icpc-team.in').read().split('\n')[:-1]
print acmTeam(f)
