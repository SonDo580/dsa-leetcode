"""
https://leetcode.com/problems/two-sum-iv-input-is-a-bst/

Given the root of a binary search tree and an integer k,
return true if there exist two elements in the BST
such that their sum is equal to k, or false otherwise.
"""

from __future__ import annotations


class TreeNode:
    def __init__(
        self, val: int, left: TreeNode | None = None, right: TreeNode | None = None
    ):
        self.val = val
        self.left = left
        self.right = right


# === 1.1) Flatten to sorted array + 2 pointers ===
"""
- Perform in-order traversal to collect node values in sorted order.
- Use 2 pointers on the sorted array to check:
  . a = 0, b = n - 1
  . Adjust a and b suck that arr[a] + arr[b] goes toward k.
    . sum > k -> decrease sum -> b -= 1
    . sum < k -> increase sum -> a += 1
    . sum == k -> found
"""


def find_target(root: TreeNode | None, k: int) -> bool:
    sorted_vals: list[int] = []

    def _in_order_dfs(node: TreeNode | None) -> None:
        if not node:
            return
        _in_order_dfs(node.left)
        sorted_vals.append(node.val)
        _in_order_dfs(node.right)

    _in_order_dfs(root)

    left = 0
    right = len(sorted_vals) - 1
    while left < right:
        s = sorted_vals[left] + sorted_vals[right]
        if s == k:
            return True
        elif s > k:
            right -= 1
        else:
            left += 1
    return False


"""
Complexity:
- Let n = number of nodes
      h = tree height
  . worst case: skewed tree -> O(h) = O(n)
  . best case: complete tree -> O(h) = O(log(n))

1. Time complexity: O(n)
- DFS: O(n) (each node is processed once)
- 2-pointers on sorted_vals: O(n)

2. Space complexity: O(n + h)
- DFS: O(h) for recursion stack
- sorted_vals: O(n)
"""

# === 1.2) Flatten to array + hashing ===
"""
- Collect node values into an array 'vals'.
  Don't use sorted property so any DFS order would work.
- Check if there are 2 elements that sum to k:
  . Iterate through 'vals' once. Add seen values to a set.
  . Return True if compliment of a value has been seen before.
"""


def find_target(root: TreeNode | None, k: int) -> bool:
    vals: list[int] = []

    # any DFS order would work
    def _pre_order_dfs(node: TreeNode | None) -> None:
        if not node:
            return
        vals.append(node.val)
        _pre_order_dfs(node.left)
        _pre_order_dfs(node.right)

    _pre_order_dfs(root)

    seen: set[int] = set()  # seen values
    for val in vals:
        if k - val in seen:
            return True
        seen.add(val)
    return False


"""
Complexity:

1. Time complexity: O(n)
- DFS: O(n)
- Iterate through 'vals': O(n)

2. Space complexity: O(n + h)
- DFS: O(h) for recursion stack
- 'vals': O(n)
- 'seen': O(n)
"""


# === 1.3) Flatten to sorted array + binary search ===
"""
- Perform in-order traversal to collect node values in sorted order.
- Check if there are 2 elements that sum to k:
  . Iterate through 'vals'.
  . For each value, binary search for complement on the remaining section
    (Don't need to revisit iterated items. If there's a valid answer there,
     it should have been found in a previous iteration)
"""


def find_target(root: TreeNode | None, k: int) -> bool:
    sorted_vals: list[int] = []

    def _in_order_dfs(node: TreeNode | None) -> None:
        if not node:
            return
        _in_order_dfs(node.left)
        sorted_vals.append(node.val)
        _in_order_dfs(node.right)

    _in_order_dfs(root)

    n = len(sorted_vals)
    for i in range(n - 1):
        # binary search for complement
        complement = k - sorted_vals[i]
        left = i + 1
        right = n - 1
        while left <= right:
            mid = (left + right) // 2
            if sorted_vals[mid] == complement:
                return True
            elif sorted_vals[mid] < complement:
                left += 1
            else:
                right -= 1

    return False


"""
Complexity:

1. Time complexity: O(n*log(n))
- DFS: O(n)
- Iterate through sorted_vals and binary search 
  on remaining section for each value:
  . log(n - 1) + log(n - 2) + ... + log(1)) < n * log(n)
    ---------------------------------------
                n - 1
=> Total: O(n) + O(n*log(n)) = O(n*log(n))

2. Space complexity: O(n + h)
- DFS: O(h) for recursion stack
- sorted_vals: O(n)
"""


# === 2.1) 2 pointers on tree - recursive (generators as iterators) ===
"""
- Define 2 iterators that yield values in increasing/decreasing order.
  Each iterator will perform in-order traversal.
"""

from typing import Generator


def find_target(root: TreeNode | None, k: int) -> bool:
    if not root:
        return False

    def _in_order_dfs(
        node: TreeNode | None, desc: bool
    ) -> Generator[TreeNode, None, None]:
        """Yield tree nodes in sorted order (increasing or decreasing)."""
        if not node:
            return

        first, last = node.left, node.right
        if desc:
            first, last = node.right, node.left

        yield from _in_order_dfs(first, desc)
        yield node
        yield from _in_order_dfs(last, desc)

    forward_iter = _in_order_dfs(root, desc=False)
    backward_iter = _in_order_dfs(root, desc=True)

    # Kickstart
    left = next(forward_iter, None)
    right = next(backward_iter, None)

    while left != right:  # guaranteed to meet before left or right becomes None
        s = left.val + right.val
        if s == k:
            return True
        elif s > k:
            right = next(backward_iter, None)
        else:
            left = next(forward_iter, None)

    return False


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(h) for recursion stack
"""


# === 2.1.1) 2 pointers on tree - iterative (no generators) ===
"""
- Use 2 explicit stacks to perform in-order traversal
  in forward and backward order.
- Process a node on 2nd pop from stack, not 1st pop.
  (process order: left -> node -> right)
  -> stack item: (node, should_process)
- At any step, compare 2 current items (should_process=True) on 2 stacks.
"""


def find_target(root: TreeNode | None, k: int) -> bool:
    if not root:
        return False

    forward_stack: list[tuple[TreeNode, bool]] = [(root, False)]
    backward_stack: list[tuple[TreeNode, bool]] = [(root, False)]

    def next_node(stack: list[tuple[TreeNode, bool]], desc: bool) -> TreeNode | None:
        while stack:
            node, should_process = stack.pop()
            if should_process:
                return node

            first, last = node.left, node.right
            if desc:
                first, last = node.right, node.left

            # process order: first -> node -> last
            # -> push order: last -> node -> first
            if last:
                stack.append((last, False))
            stack.append((node, True))  # process on next encounter
            if first:
                stack.append((first, False))

        return None

    # Kickstart
    left = next_node(forward_stack, desc=False)
    right = next_node(backward_stack, desc=True)

    while left != right:  # guaranteed to meet before left or right becomes None
        s = left.val + right.val
        if s == k:
            return True
        elif s > k:
            right = next_node(backward_stack, desc=True)
        else:
            left = next_node(forward_stack, desc=False)

    return False


"""
Complexity:
1. Time complexity: O(n) (each node is visited twice)
2. Space complexity: O(h) for 2 stacks
"""


# === 2.2) DFS/BFS + hashing ===
"""
- Use a set to store all seen values.
- At each node, check if its complement has been seen.
- Any traversal order would work.
"""


def find_target(root: TreeNode | None, k: int) -> bool:
    if not root:
        return False

    # Use pre-order DFS (other orders also work)
    stack: list[TreeNode] = [root]

    seen: set[int] = set()  # seen values
    # - add when pop node from stack, not when push node to stack
    # - what if we add value to 'seen' when push node to stack:
    #   . if node.val == k - node.val,
    #     the check 'k - node.val in seen' will evaluate to True
    #     even if there's no other node with value k - node.val
    # - alternative: track seen nodes, not just node values.

    while stack:
        node = stack.pop()
        if k - node.val in seen:
            return True
        seen.add(node.val)

        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)

    return False


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n + h) 
- stack: O(h)
- 'seen': O(n)
"""


# === 2.3) DFS/BFS + binary search ===
"""
- Any traversal order would work.
- At each node, binary search on the whole tree for its complement.
"""


def find_target(root: TreeNode | None, k: int) -> bool:
    if not root:
        return False

    def _search(node: TreeNode | None, exclude: TreeNode, target: int) -> bool:
        """True if found a node where node.val == target and node != exclude."""
        if not node:
            return False

        if node.val == target and node != exclude:
            return True
        elif target < node.val:
            return _search(node.left, exclude, target)
        else:
            return _search(node.right, exclude, target)

    # Any traversal order would work
    def _pre_order_dfs(node: TreeNode | None) -> bool:
        """Return True found 2 nodes in current subtree with sum = k."""
        if not node:
            return False
        if _search(root, exclude=node, target=k - node.val):
            return True
        return _pre_order_dfs(node.left) or _pre_order_dfs(node.right)

    return _pre_order_dfs(root)


"""
Complexity:

1. Time complexity: O(n*h)
- Each node is visited once
  . Binary search for complement for each node: O(h)

2. Space complexity: O(h) 
- recursion stack (_dfs + _search): O(h*2) 
"""


# === 2.3.1) in-order DFS + binary search (similar to idea 1.3)===
"""
- Use in-order DFS to visit nodes in sorted order.
- At each node, binary search for its complement on the tree section
  with val > node.val
  -> Skip searching node.left (if there's a valid answer there,
     it should have been found when visiting node.left).
  -> Reduce search space (but doesn't change complexity)
"""


def find_target(root: TreeNode | None, k: int) -> bool:
    if not root:
        return False

    def _search(node: TreeNode | None, exclude: TreeNode, target: int) -> bool:
        """True if found a node where node.val == target and node != exclude."""
        if not node:
            return False

        if node.val == target and node != exclude:
            return True
        elif target < node.val:
            if node == exclude:
                # Skip exclude.left (visited and searched for complements)
                return False
            return _search(node.left, exclude, target)
        else:
            return _search(node.right, exclude, target)

    def _in_order_dfs(node: TreeNode | None) -> bool:
        """Return True found 2 nodes in current subtree with sum = k."""
        if not node:
            return False
        if _in_order_dfs(node.left):
            return True
        if _search(root, exclude=node, target=k - node.val):
            return True
        return _in_order_dfs(node.right)

    return _in_order_dfs(root)


"""
Complexity: same as (2.3)

1. Time complexity: O(n*h)
- Each node is visited once
  . Binary search for complement for each node: O(h)

2. Space complexity: O(h) 
- recursion stack (_dfs + _search): O(h*2) 
"""
