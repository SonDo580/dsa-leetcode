"""
https://leetcode.com/problems/search-suggestions-system/

You are given an array of strings 'products' and a string searchWord.

Design a system that suggests at most 3 product names from 'products'
after each character of searchWord is typed.

Suggested products should share a common prefix with 'searchWord'.

If there are more than 3 products with a common prefix,
choose the 3 lexicographical minimums.

Return a list of lists of the suggested products after each character of searchWord is typed.
"""

"""
lexicographical order:
- Compare 2 strings from left to right
  . Compare the first characters.
  . If they differ -> the one with smaller character comes first.
  . If they're equal -> move on to the next character.
  . If one string ends before the other -> the shorter one comes first.
"""

# ===== Brute-force approach =====
# ================================
"""
- For each prefix, iterate over 'products' and check which ones match.
- Reuse list of products already matched with shorter prefix.
  -> only have to check the current character.
- Sort 'products' in ascending order (for choosing 3 lexicographical minimums).
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
      k = average products[i] length
      m = len(searchWord)

1. Time complexity:
- Sort 'products': O(n*k*log(n))    (string comparison costs O(k))
- Iterate over 'searchWord': m iterations
  - Iterate over 'filtered_products': O(n)
=> Overall: O(n*k*log(n) + n*m)

2. Space complexity: 
- sort 'products': O(n)
- 'filtered_products': O(n)
=> Overall: O(n)
"""


# ===== Improvement 1 =====
# =========================
"""
- Build a trie from 'products'.
- For each prefix:
  . Traverse the trie following characters in prefix.
  . Perform DFS/BFS from the reached node to find matched products.
  . To limit to k suggestions, use DFS and stop early.
  . Prioritize the lexicographical lower keys.
- Optimization:
  . Avoid string slicing to get prefix.
    -> pass 'searchWord' and upper bound index i.
  . Avoid repeating traversal for incremental prefix.
    -> start from the reached node for previous prefix.
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
        Find all words with prefix = search_word[0:i+1].
        Just match search_word[i] character, starting from start_node,
        which is the node reached by matching previous prefix search_word[0:i].

        Returns:
        - the last node reached by matching prefix,
          or None if there's no path matches prefix.
        - list of matching words (limited).
        """
        # start_node is None -> matching failed from a previous prefix
        if not start_node:
            return None, []

        # Go along 1 path with prefix
        # (match search_word[i] character starting from start_node,
        #  don't re-traverse from the root except for i = 0)
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
      k = average products[i] length
      m = len(searchWord)
      A = alphabet size (26, fixed)
      L = suggestions limit (3, fixed)

1. Time complexity:
- Build trie from 'products': O(n * k)
- Traverse prefixes of 'searchWord': O(m)
  (each character is matched once, reuse previous traversal with start_node) 
- Finding suggestions for 1 prefix:
  . DFS starts from the reached node, stops after L words are found,
    with max depth ~ O(k): O(L * k) ~ O(k)
  . children keys sorting: O(A * log(A)) ~ O(1)
-> Finding suggestions for all prefixes: O(m * k)
=> Overall: O(n*k + m*k)

2. Space complexity: 
- trie: O(n * k)
- stack: O(k)
- sorted keys: O(L) ~ O(1)
=> Overall: O(n * k)
"""


# ===== Improvement 2 =====
# =========================
"""
- Use an attribute 'matched_words' at each trie node to store the products 
  that share common prefix up to that node.
- Limit the size of 'matched_words' to 3 and keep it sorted.
  -> Sort products in lexicographical order, then insert in that order.
- Once the trie is built, we can instantly know the answer when arriving at a node.
"""


class TrieNode2:
    def __init__(self):
        self.children: dict[str, TrieNode2] = {}
        self.matched_words: list[str] = []


class Trie2:
    def __init__(self, words: list[str] = []):
        self.root = TrieNode2()
        for word in words:
            self.insert(word)

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
            # if matching an earlier prefix failed
            if failed:
                results.append([])

            if c not in current.children:
                failed = True
                results.append([])
            else:
                # Match the current character then get matched words
                current = current.children[c]
                results.append(current.matched_words)

        return results


def suggested_products(products: list[str], search_word: str) -> list[list[str]]:
    products.sort()
    trie = Trie2(products)
    return trie.find_matched_words_at_all_prefixes(search_word)


"""
Complexity:
- Let n = len(products)
      k = average products[i] length
      m = len(searchWord)
      A = alphabet size (26, fixed)
      L = suggestions limit (3, fixed)

1. Time complexity:
- Sort 'products': O(n*k*log(n))    (string comparison costs O(k))
- Build trie from 'products': O(n * k)
- Traverse trie with 'searchWord' to collect answers: O(m)
=> Overall: O(n*k*log(n) + n*k + m)

2. Space complexity: 
- trie: O(n * k)
  . matched_words per node: O(L) ~ O(1)
=> Overall: O(n * k)
"""
