class TreeNode:
    def __init__(self, val, left, right):
        self.val = val 
        self.left = left
        self.right = right 

def pre_order_dfs(node):
    if not node:
        return
    
    print(node.val)
    pre_order_dfs(node.left)
    pre_order_dfs(node.right)

def in_order_dfs(node):
    if not node:
        return
    
    pre_order_dfs(node.left)
    print(node.val)
    pre_order_dfs(node.right)

def post_order_dfs(node):
    if not node:
        return
    
    pre_order_dfs(node.left)
    pre_order_dfs(node.right)
    print(node.val)