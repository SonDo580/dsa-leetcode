# You are given a string s. Continuously remove duplicates
# (two of the same character beside each other) until you can't anymore.
# Return the final string after this.
#
# For example, given s = "abbaca", you can first remove the "bb" to get "aaca".
# Next, you can remove the "aa" to get "ca". This is the final answer.


def remove_adjacent_duplicates(s: str) -> str:
    stack = []

    for c in s:
        # - if the top of the stack is the same as the current character,
        #   they are adjacent duplicates and can be deleted
        # - note that some adjacent duplicates are available after the
        #   deletions of in-between characters

        if len(stack) > 0 and stack[-1] == c:
            stack.pop()
        else:
            stack.append(c)

    return "".join(stack)
