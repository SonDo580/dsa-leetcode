# You are given an absolute path for a Unix-style file system,
# which always begins with a slash '/'.
# Your task is to transform this absolute path into its simplified canonical path.
#
# The rules of a Unix-style file system are as follows:
# - A single period '.' represents the current directory.
# - A double period '..' represents the previous/parent directory.
# - Multiple consecutive slashes such as '//' and '///' are treated as a single slash '/'.
# - Any sequence of periods that does not match the rules above should be treated
#   as a valid directory or file name.
#   For example, '...' and '....' are valid directory or file names.
#
# The simplified canonical path should follow these rules:
# - The path must start with a single slash '/'.
# - Directories within the path must be separated by exactly one slash '/'.
# - The path must not end with a slash '/', unless it is the root directory.
# - The path must not have any single or double periods ('.' and '..') used to denote
#   current or parent directories.
#
# Return the simplified canonical path.

# Example 1:
# Input: path = "/home/"
# Output: "/home"
# Explanation: The trailing slash should be removed.

# Example 2:
# Input: path = "/home//foo/"
# Output: "/home/foo"
# Explanation: Multiple consecutive slashes are replaced by a single one.

# Example 3:
# Input: path = "/home/user/Documents/../Pictures"
# Output: "/home/user/Pictures"
# Explanation: A double period ".." refers to the directory up a level (the parent directory).

# Example 4:
# Input: path = "/../"
# Output: "/"
# Explanation: Going one level up from the root directory is not possible.

# Example 5:
# Input: path = "/.../a/../b/c/../d/./"
# Output: "/.../b/d"
# Explanation: "..." is a valid name for a directory in this problem.

# Constraints:
# - 1 <= path.length <= 3000
# - path consists of English letters, digits, period '.', slash '/' or '_'.
# - path is a valid absolute Unix path.


from typing import List


def simplify_path(path: str) -> str:
    n = len(path)

    # The first '/' (root directory) always remains in the stack
    stack: List[str] = [path[0]]

    for i in range(n):
        # Handle consecutive slashes
        if stack[-1] == "/" and path[i] == '/':
            continue

        # Handle single period (current directory)
        #
        # [a]/./[b] -> [a]//[b] (the extra '/' will be skipped in the next iteration)
        # [a]/.END -> [a]/END (the trailing '/' will be popped after the loop)
        if stack[-1] == "/" and path[i] == "." and (i == n - 1 or path[i + 1] == "/"):
            continue

        # Handle double period
        #
        # [a]/[b]/../[c] -> [a]//[c] (the extra '/' will be skipped in the next iteration)
        # [a]/[b]/..END -> [a]/END (the extra '/' will be skipped in the next iteration)
        # /../[b] -> //[b] (keep the root)
        if stack[-1] == "." and stack[-2] == "/" and path[i] == "." and (i == n - 1 or path[i + 1] == "/"):
            # Remove the current directory to go back to the parent directory
            # unless it is the root directory
            # -> keep popping characters from the stack until 
            # + encountering a second '/' (remove 1 '/')
            # + OR the stack only has 1 character left
            slash_removed = False
            while len(stack) > 1:
                if stack[-1] == "/":
                    if slash_removed:
                        break
                    slash_removed = True
                stack.pop()

            continue

        # Append the current character to the stack
        stack.append(path[i])

    # Remove the trailing '/' if it is not the root
    if len(stack) > 1 and stack[-1] == "/":
        stack.pop()

    # Form the simplified canonical path
    return "".join(stack)

# ===== Complexity =====
# 
# Time complexity:
# - Loop through the path string: O(n)
# - Pop characters from the stack for double period: O(n) across all iterations
# => Overall: O(n)
#
# Space complexity: O(n)
# - Space for the stack
