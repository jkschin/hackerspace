import numpy as np

class Node:
    def __init__(self, parent, bounds):
        self.parent = parent
        self.bounds = bounds
        self.width = bounds[1] - bounds[0] - 1
        self.idx = -1
        self.l_max = -1
        self.r_max = -1
        self.left = None
        self.right = None

class Tree:
    def __init__(self, root):
        self.root = root

    def insert(self, node):
        if node.left == None and node.right == None:
            l_b, r_b = node.bounds
            mid = (r_b-1 - l_b+1) / 2 + l_b
            node.idx = mid
            if (mid - l_b) == 1:
                node.left = -1
                node.l_max = -1
            else:
                node.left = Node(node, [l_b, mid])
                node.l_max = node.left.width
            if (r_b - mid) == 1:
                node.right = -1
                node.r_max = -1
            else:
                node.right = Node(node, [mid, r_b])
                node.r_max = node.right.width
            return max(node.l_max, node.r_max), node
        elif node.l_max < node.r_max:
            child = node.right
            val, ans = self.insert(child)
            node.r_max = val
            return max(node.r_max, node.l_max), ans
        elif node.l_max >= node.r_max:
            child = node.left
            val, ans = self.insert(child)
            node.l_max = val
            return max(node.r_max, node.l_max), ans

    def update(self, node):
        while True:
            if node == None:
                break
            if node.l_max <= node.left.width:
                node.l_max = node.left.width
            if node.r_max <= node.right.width:
                node.r_max = node.right.width
            node = node.parent

    def trace(self, node):
        print node.bounds, node.width, node.l_max, node.r_max, node.idx
        if node.left == None and node.right == None:
            return 0
        else:
            self.trace(node.left)
            self.trace(node.right)

def main(n, k):
    tree = Tree(Node(None, [0, n-1+2]))
    for i in xrange(k):
        ph = 0
        a, ans = tree.insert(tree.root)
    # print ans.idx, ans.bounds
    ls = ans.idx - 1 - ans.bounds[0]
    rs = ans.bounds[1] - ans.idx - 1
    return max(ls, rs), min(ls, rs)

def main2(n, k):
    i, p = 2, 0
    while True:
        if k < i**p:
            p -= 1
            break
        else: p += 1
    if i**p != 1: lines = i**p - 1 + 2
    else: lines = i**p + 2
    bins = lines - 1
    q, r = (n+2 - lines) / (bins), (n+2 - lines) % (bins)
    if (k-(lines-2)) == 0: return max(q, q+r), min(q, q+r)
    elif r < k-(lines-2): q += 0
    elif r >= k-(lines-2): q += 1
    q -= 1
    return max(q/2, q-(q/2)), min(q/2, q-(q/2))
# print main2(999, 127)
# print main2(500, 128)

def io(inp, out):
    inp = open(inp, 'r')
    out = open(out, 'w')
    n = int(inp.readline())
    for i in xrange(n):
        print 'Case', i+1
        out.write("Case #%d: " %(i+1))
        l = map(lambda x: int(x), inp.readline().split())
        ans = main2(l[0], l[1])
        out.write("%d %d\n" %(ans[0], ans[1]))

io('C-large.in', 'C-large.ans')
