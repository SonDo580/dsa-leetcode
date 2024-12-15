class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def pre_order_dfs(root):
    if not root:
        return

    stack = [root]

    while len(stack) > 0:
        node = stack.pop()
        print(node.val)

        if node.left:
            stack.append(node.left)

        if node.right:
            stack.append(node.right)
