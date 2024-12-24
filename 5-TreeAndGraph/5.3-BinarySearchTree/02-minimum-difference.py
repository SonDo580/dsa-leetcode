# Given the root of a BST,
# return the minimum absolute difference between
# the values of any two different nodes in the tree.

# ===== Naive approach =====
# - Go through the tree and put all values in an array
# - Loop over all pairs to find the minimum difference
# -> Time complexity: O(n^2)

# ===== Better approach =====
# - Go through the tree and put all values in an array
# - Sort the array
# - Iterate over the adjacent elements
# -> Time complexity: O(n*log(n))

# ===== Leverage BST property =====
# If we perform an in-order traversal on a BST, we visit the nodes in sorted order
# -> Get the nodes in sorted order without the O(n*log(n)) sort
# -> Overall time complexity: O(n)


class TreeNode:
    def __init__(self, val, left, right):
        self.val = val
        self.left = left
        self.right = right


def get_minimum_difference_recursive(root: TreeNode) -> int:
    def dfs(node, values):
        if not node:
            return

        dfs(node.left, values)
        values.append(node.val)
        dfs(node.right, values)

    # Store node values
    values = []

    # Call dfs to perform an in-order traversal on the tree
    dfs(root, values)

    # 'values' is now in increasing order

    # Find the minimum difference on the whole tree
    min_diff = float("inf")
    for i in range(1, len(values)):
        min_diff = min(min_diff, values[i] - values[i - 1])

    return min_diff


def get_minimum_difference_iterative(root: TreeNode) -> int:
    def iterative_in_order_dfs(root):
        '''
        Visit nodes in the left->current->right order
        Produce the array of node values in increasing order  
        '''

        stack = []
        values = []
        current = root

        while current or len(stack) > 0:
            if current:
                # current is not None -> keep exploring the left subtree
                
                # push current node the stack (return to it later)
                stack.append(current)
                
                # move to the left subtree
                current = current.left
            else:
                # current is None -> reached the end of a branch
                # -> time to backtrack 
                
                # get the most recent ancestor to visit
                current = stack.pop() 

                # process the node
                values.append(current.val)

                # start exploring the right subtree
                current = current.right

        return values

    values = iterative_in_order_dfs(root)
    min_diff = float("inf")

    for i in range(1, len(values)):
        min_diff = min(min_diff, values[i] - values[i - 1])

    return min_diff


# ===== Analyze =====
# - Time and space complexity is O(n)
