# Given two strings s and t,
# return true if they are equal when both are typed into empty text editors.
# '#' means a backspace character.

# For example, given s = "ab#c" and t = "ad#c", return true.
# Because of the backspace, the strings are both equal to "ac"

def backspace_compare(s: str, t: str) -> bool:
    def get_final_string(string_with_backspaces):
        stack = []

        for c in string_with_backspaces:
            if c != "#":
                # add normal characters to the stack
                stack.append(c)
            elif len(stack) > 0:
                # remove the latest typed character if c is a backspace
                stack.pop()

        return "".join(stack)

    return get_final_string(s) == get_final_string(t)
