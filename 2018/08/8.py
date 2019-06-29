import sys

in_vals = list(map(int, sys.stdin.read().rstrip().split(' ')))

class Node:
    def __init__(self):
        self.children = []
        self.meta = []

def read_node(stack):
    nchildren = stack.pop(0)
    nmeta = stack.pop(0)

    n = Node()
    for i in range(nchildren):
        n.children.append(read_node(stack))
    for i in range(nmeta):
        n.meta.append(stack.pop(0))
    return n

def sum_meta(root):
    return sum(root.meta) + sum(map(sum_meta, root.children))

def value(root):
    if not root.children:
        return sum(root.meta)
    
    val = 0
    for m in root.meta:
        if not 0 <= m - 1 < len(root.children):
            continue
        val += value(root.children[m-1])
    return val


root = read_node(in_vals)
print(sum_meta(root))
print(value(root))