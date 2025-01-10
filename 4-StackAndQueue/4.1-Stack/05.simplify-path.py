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
    # The first '/' always remains in the stack
    stack: List[str] = [path[0]]

    n = len(path)
    for i in range(n):
        if stack[-1] == "/":
            # Treat multiple consecutive '/' as a single '/'
            if path[i] == "/":
                continue

            # Handle single period
            #
            # [a]/./[b] -> [a]//[b] (the extra '/' will be skipped in the next iteration)
            # [a]/.END -> [a]/END (the trailing '/' will be popped after the loop)
            if path[i] == "." and (i == n - 1 or path[i + 1] == "/"):
                continue

        if stack[-1] == ".":
            # Handle double period
            #
            # [a]/[b]/../[c] -> [a]//[c] (the extra '/' will be skipped in the next iteration)
            # [a]/[b]/..END -> [a]/END (the extra '/' will be skipped in the next iteration)
            # /../[b] -> //[b] (keep the root)
            if path[i] == "." and (i == n - 1 or path[i + 1] == "/"):
                # Check if the current directory is 'normal'
                if stack[-2] != "/":
                    stack.append(path[i])
                    continue

                # Remove the current directory to go back to the parent directory
                # unless it is the root directory
                # -> keep popping characters off the stack until encountering a second '/'
                #    or the stack only has 1 item left
                slash_encountered_once = False
                while len(stack) > 1:
                    if stack[-1] == "/":
                        if slash_encountered_once:
                            break
                        slash_encountered_once = True
                        
                    stack.pop()

                continue

        stack.append(path[i])

    # Remove the trailing '/' if needed
    if len(stack) > 1 and stack[-1] == "/":
        stack.pop()

    # Form the simplified canonical path
    return "".join(stack)
