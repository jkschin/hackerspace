def acmTeam(topic):
    dic = {}
    for i in xrange(len(topic)):
        a = int(topic[i], 2)
        for j in xrange(i+1, len(topic)):
            b = int(topic[j], 2)
            # c = sum([int(z) for z in list(bin(a | b)[2:])])
            c = a | b
            if c not in dic:
                dic[c] = 1
            else:
                dic[c] += 1

    new_dic = {}
    for key in dic.keys():
        val = dic[key]
        new_key = sum([int(z) for z in list(bin(key)[2:])])
        if new_key not in new_dic:
            new_dic[new_key] = val
        else:
            new_dic[new_key] += val
    max_subs = max(new_dic.keys())
    max_teams = new_dic[max_subs]
    return [max_subs, max_teams]

f = open('acm-icpc-team.in').read().split('\n')[:-1]
print acmTeam(f)
