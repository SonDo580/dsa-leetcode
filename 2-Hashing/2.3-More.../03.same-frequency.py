# Given a string s, determine if all characters have the same frequency.

# For example, given s = "abacbc", return true. All characters appear twice. 
# Given s = "aaabb", return false. "a" appears 3 times, "b" appears 2 times. 3 != 2.

def same_frequency(s: str) -> bool:
    counts = {}
    for c in s:
        if c not in counts:
            counts[c] = 0
        counts[c] += 1
    
    return len(set(counts.values())) == 1

# Time complexity: O(n)
# - O(n) to populate the hash map
# - O(n) to convert hash map values to a set  

# Space complexity: O(k) where k is the number of allowable characters
# (the space occupied by the hash map is the number of unique elements)
