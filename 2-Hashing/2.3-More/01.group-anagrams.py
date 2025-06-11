# Given an array of strings strs, group the anagrams together.
# For example, given strs = ["eat","tea","tan","ate","nat","bat"], 
# return [["bat"],["nat","tan"],["ate","eat","tea"]].

# ===== Analyze =====
# - If 2 strings are anagrams, they are equal after sorted
# => Use a hashmap with sorted string as key.
#    The value will group the original strings.

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = {}
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

# ===== Complexity =====
# - Let n be strs.length; m is average string length
# 
# 1. Time complexity:
# - Iterate over strs: O(n)
#   + sort the string in each iteration: O(m*log(m))
# - Iterate through 'groups' entries to build result: O(n)
# => Overall: O(n*m*log(m))
# 
# 2. Space complexity: 
# - Space for 'groups'
#   + at most n entries, each key occupies m: O(n*m)
#   + store all the original strs across values: O(n*m)
# => Overall: O(n*m)