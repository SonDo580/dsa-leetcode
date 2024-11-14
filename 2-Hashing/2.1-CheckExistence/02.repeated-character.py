# Given a string s, return the first character to appear twice. 
# It is guaranteed that the input will have a duplicate character.

def repeated_character(s: str) -> str | None:
    seen = set()
    for c in s:
        if c in seen:
            return c
        seen.add(c)
    return None

# Time complexity: O(n)
# Space complexity: O(m) - where m is the number of allowable characters