# You are given a binary string s (a string containing only "0" and "1").
# You may choose up to one "0" and flip it to a "1".
# What is the length of the longest substring achievable
# that contains only "1"?
#
# For example, given s = "1101100111", the answer is 5.
# If you perform the flip at index 2, the string becomes 1111100111.

# => Reframe the question:
# What is the longest substring that contains at most one "0"

def longest_substring(s: str) -> int:
    left = 0
    count_zero = 0
    max_length = 0

    for right in range(len(s)):
        if s[right] == "0":
            count_zero += 1

        while count_zero > 1:
            if s[left] == "0":
                count_zero -= 1
            left += 1

        max_length = max(max_length, right - left + 1)

    return max_length
