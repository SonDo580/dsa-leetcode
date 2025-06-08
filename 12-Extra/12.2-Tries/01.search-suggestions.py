# You are given an array of strings products and a string searchWord. 
# Design a system that suggests at most three product names from products after each character of searchWord is typed. 
# Suggested products should share a common prefix with searchWord. 
# If there are more than three products with a common prefix, 
# choose the three lexicographical minimums. 
# Return a list of lists of the suggested products after each character of searchWord is typed.

# ===== Brute-force approach =====
# - Iterate over products for each prefix and check which ones match
# => Time complexity: O(n * m^2)
#    where n = products.length; m = searchWord.length

# ===== Improvement =====
# - Build a trie from products: O(n*k) where k is average product[i].length
# - Find all words with matching prefix: O(m)
# => Time complexity: O(n * k + m)
# (Note that we only build the trie once. Then every lookup takes O(m))

# ===== Further improvement =====
# - Use an attribute "suggestions" to store the products that should be returned.
#   Limit the size to 3 and keep it sorted.
# - Once the trie is built, we can instantly know the answer when arriving at a node.

class TrieNode:
    def __init__(self):
        self.children: dict[str, "TrieNode"] = {}
        self.suggestions: list[str] = []

def suggested_product(products: list[str], search_word: str) -> list[list[str]]:
    root = TrieNode()
    for product in products:
        current = root
        for c in product:
            if c not in current.children:
                current.children[c] = TrieNode()
            current = current.children[c]

            current.suggestions.append(product)
            current.suggestions.sort()
            if len(current.suggestions) > 3:
                current.suggestions.pop()

    answer = []
    current = root

    # When a prefix does not exist, add [] for all subsequent prefixes
    broken = False

    for c in search_word:
        if broken:
            answer.append([])
            continue

        if c in current.children:
            current = current.children[c]
            answer.append(current.suggestions)
        else:
            answer.append([])
            broken = True
    
    return answer