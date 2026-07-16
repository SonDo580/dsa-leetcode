"""
https://leetcode.com/problems/search-suggestions-system/

You are given an array of strings 'products' and a string 'searchWord'.

Design a system that suggests at most 3 product names from 'products'
after each character of 'searchWord' is typed.

Suggested products should share a common prefix with 'searchWord'.

If there are more than 3 products with a common prefix,
choose the 3 lexicographical minimums.

Return a list of lists of the suggested products
after each character of 'searchWord' is typed.
"""

"""
lexicographical order:
- Compare 2 strings from left to right
  . Compare the first characters.
  . If they differ -> the one with smaller character comes first.
  . If they're equal -> move on to the next character.
  . If one string ends before the other -> the shorter one comes first.
"""

# ===== Approach 1: Brute-force =====
# ===================================
"""
- For each prefix, iterate over 'products' and check which ones match.
- At each character, only check products already matched shorter prefix.
- Sort 'products' in ascending order for choosing lexicographical minimums.
"""


def suggested_products(products: list[str], search_word: str) -> list[list[str]]:
    results: list[list[str]] = []
    products.sort()
    filtered_products: list[str] = products

    for i in range(len(search_word)):
        prefix_result: list[str] = []

        for product in filtered_products:
            if len(product) < i + 1:
                continue

            # Only check the current character
            # (previous part already matched)
            if product[i] == search_word[i]:
                prefix_result.append(product)

        filtered_products = prefix_result
        results.append(prefix_result[:3])

    return results


"""
Complexity:
- Let n = len(products)
      k = len(products[i])
      m = len(searchWord)

1. Time complexity: O(n*k*log(n) + n*m)
- Sort 'products': O(n*k*log(n))    (string comparison costs O(k))
- Iterate over 'searchWord': m iterations
  . Iterate over 'filtered_products': O(n)

2. Space complexity: O(n)
- sort 'products': O(n) (timsort)
- 'filtered_products': O(n)
"""


# === Approach 2.1: Trie + DFS ===
# ================================
"""
- Build a trie from 'products'.
- For each prefix:
  . Traverse the trie following characters in prefix.
  . Perform traversal from reached node to find matched products.
  . To limit to k suggestions, use DFS and stop early.
    Prioritize lexicographical lower keys.
- Optimization:
  . Avoid string slicing to get prefix.
    -> pass 'searchWord' and upper bound index i.
  . Avoid repeating traversal for incremental prefix.
    -> start from reached node for previous prefix.
"""


class TrieNode1:
    def __init__(self):
        self.children: dict[str, TrieNode1] = {}

        # Record if the path from root to this node forms a full word
        self.word: str | None = None


class Trie1:
    def __init__(self, words: list[str] = []):
        self.root = TrieNode1()
        for word in words:
            self.insert(word)

    def insert(self, word: str) -> None:
        current = self.root
        for c in word:
            if c not in current.children:
                current.children[c] = TrieNode1()
            current = current.children[c]
        current.word = word

    def find_by_prefix(
        self, start_node: TrieNode1 | None, search_word: str, i: int, limit: int
    ) -> tuple[list[str]]:
        """
        Find all words with prefix = search_word[0..i].
        Just match search_word[i] character, starting from start_node,
        which is the node reached by matching previous prefix search_word[0..i-1].

        Returns:
        - the last node reached by matching prefix (None if no paths match).
        - list of matching words (limited).
        """

        if not start_node:
            # matching failed from a previous prefix
            return None, []

        # Go along 1 path with prefix
        # - match search_word[i] character starting from start_node,
        #   don't re-traverse from the root except for i = 0.
        current = start_node
        c = search_word[i]
        if c not in current.children:
            return None, []

        current = current.children[c]

        # Perform DFS from 'current' to find matching words
        words: list[str] = []
        stack: list[TrieNode1] = [current]

        while stack:
            node = stack.pop()
            if node.word is not None:
                words.append(node.word)
            if len(words) == limit:
                break

            # Ensure lower keys are processed first
            for c in sorted(node.children.keys(), reverse=True):
                stack.append(node.children[c])

        return current, words


def suggested_products(products: list[str], search_word: str) -> list[list[str]]:
    results: list[list[int]] = []
    trie = Trie1(products)

    start_node: TrieNode1 = trie.root
    for i in range(len(search_word)):
        start_node, suggestions = trie.find_by_prefix(
            start_node, search_word, i, limit=3
        )
        results.append(suggestions)

    return results


"""
Complexity:
- Let n = len(products)
      k = len(products[i])
      m = len(searchWord)
      A = alphabet size (26, fixed)
      L = suggestions limit (3, fixed)

1. Time complexity: O(m*n*k)
- Build trie from 'products': O(n*k)
- Traverse prefixes of 'searchWord': O(m)
  . each character is matched once, reuse previous traversal with start_node
- Finding suggestions for 1 prefix: O(n*k)
  . DFS: O(n*k)
    . children keys sorting: O(A*log(A)) ~ O(1)
  -> Finding suggestions for all prefixes: O(m*n*k)

2. Space complexity: O(n*k)
- trie: O(n*k)
- stack: O(k)
- sorted keys: O(A) ~ O(1)
"""


# === Approach 2.2: store precomputed results at trie node ===
"""
- Use an attribute 'matched_words' at each trie node to store the products 
  that share common prefix up to that node.
- Limit the size of 'matched_words' to 3 and keep it sorted.
  -> Sort products in lexicographical order.
     Insert to trie in that order.
- Once the trie is built, we can instantly know the answer when arriving at a node.
"""


class TrieNode2:
    def __init__(self):
        self.children: dict[str, TrieNode2] = {}
        self.matched_words: list[str] = []


class Trie2:
    def __init__(self):
        self.root = TrieNode2()

    def insert(self, word: str) -> None:
        current = self.root
        for c in word:
            if c not in current.children:
                current.children[c] = TrieNode2()
            current = current.children[c]

            if len(current.matched_words) < 3:
                current.matched_words.append(word)

    def find_matched_words_at_all_prefixes(self, search_word: str) -> list[list[str]]:
        results: list[list[int]] = []
        current = self.root
        failed: bool = False

        for c in search_word:
            # Keep using empty list for subsequent prefixes
            # if failed to match an earlier prefix
            if failed:
                results.append([])
                continue

            if c not in current.children:
                failed = True
                results.append([])
            else:
                # Match the current character and collect precomputed result
                current = current.children[c]
                results.append(current.matched_words)

        return results


def suggested_products(products: list[str], search_word: str) -> list[list[str]]:
    trie = Trie2()
    products.sort()
    for word in products:
        trie.insert(word)
    return trie.find_matched_words_at_all_prefixes(search_word)


"""
Complexity:
- Let n = len(products)
      k = len(products[i])
      m = len(searchWord)
      A = alphabet size (26, fixed)
      L = suggestions limit (3, fixed)

1. Time complexity: O(n*k*log(n) + n*k + m) = O(n*k*log(n) + m)
- Sort 'products': O(n*k*log(n))    (string comparison costs O(k))
- Build trie from 'products': O(n*k)
- Traverse trie with 'searchWord' to collect answers: O(m)

2. Space complexity: O(n + n*k^2) = O(n*k^2)
- Sort 'products': O(n) (timsort)
- trie: O(n*k^2)
  . number of nodes: O(n*k)
  . matched_words per node: O(L*k) ~ O(k)
"""
