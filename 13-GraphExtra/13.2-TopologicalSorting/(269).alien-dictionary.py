"""
https://leetcode.com/problems/alien-dictionary/

There is a new alien language that uses the English alphabet.
However, the order of the letters is unknown to you.

You are given a list of strings 'words' from the alien language's dictionary.
Now it is claimed that the strings in 'words' are sorted
lexicographically by the rules of this new language.

If this claim is incorrect, and the given arrangement of string
in 'words' cannot correspond to any order of letters, return "".

Otherwise, return a string of the unique letters in the new alien language
sorted in lexicographically increasing order by the new language's rules.
If there are multiple solutions, return any of them.
"""

"""
Idea:
- Treat unique letters as nodes in graph.
- 'words' is sorted lexicographically
  -> At the same index, letter of current word <= letter of later word
     if the prefixes are the same
  -> There's a directed edge between those 2 letter
=> Collect nodes and directed edges, then apply topological sorting.

- Collect nodes and directed edges:
  . There's a directed edge from words[i][j] to words[i+x][j]
    if words[i][j] != words[i+x][j] AND words[i][:j] == words[i+x][:j]
  . Compare prefixes of every pair of words at each index j
    would be very inefficient.
    -> Use a trie.
=> Implementation:
  . Insert words sequentially to a trie.
    The root represent empty prefix ("").
  . If current letter has not been in children of current node,
    add a directed edge from last child to current letter.
    (prefixes match -> letter from previous word comes first).
  . If current letter has been in children current node
    and the last child is not current letter
    -> return "" right away.
       . adding directed edge will create cycle.
  . If current word is a prefix (not full word) of a previous word
    -> return "" right away.
       . words are sorted lexicographically, so if 2 words share prefix,
         the longer one should come later.

- Topological sorting to produce alien language's alphabet:
  Use Kahn's algorithm:
  . Start BFS from nodes with in-degree 0.
  . After a node is processed, reduce the in-degree of is children.
  . Continue until all nodes are processed, or cycle is detected
    (unprocessed nodes remain but no ones with in-degree 0). 
"""

from collections import defaultdict, deque


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_word: bool = False  # True -> end a full word
        self.last_child: str | None = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(
        self,
        word: str,
        adj_list: defaultdict[str, list[str]],
        in_degree: dict[str, int],
        unique_letters: set[str],
    ) -> bool:
        """
        Return False if current word is prefix of a previous word
        (words are actually not sorted lexicographically).
        """
        curr = self.root
        for c in word:
            unique_letters.add(c)

            if curr.last_child and curr.last_child != c:
                # adding directed edge can create cycle if
                # c is already an ancestor of curr.last_child
                # (c is a child that comes before curr.last_child
                #  at current node or any other node)
                # -> allow
                adj_list[curr.last_child].append(c)
                in_degree[c] += 1

            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr.last_child = c
            curr = curr.children[c]

        if curr.children and not curr.is_word:
            # current word is prefix of a previous word
            return False

        curr.is_word = True
        return True


def alien_order(words: list[str]) -> str:
    adj_list: defaultdict[str, list[str]] = defaultdict(list)
    in_degree: defaultdict[str, int] = defaultdict(int)
    unique_letters: set[str] = set()

    trie = Trie()
    for word in words:
        if not trie.insert(word, adj_list, in_degree, unique_letters):
            return ""

    alien_alphabet: list[str] = []

    queue: deque[str] = deque()
    for node in unique_letters:
        if in_degree[node] == 0:
            queue.append(node)

    while queue:
        node = queue.popleft()
        alien_alphabet.append(node)
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(alien_alphabet) != len(unique_letters):
        return ""  # graph contains cycles

    return "".join(alien_alphabet)


"""
Complexity:
- Let n = len(words)
      L = max word length
- Number of nodes (unique letters): V = O(n*L)
  Number of edges: E

1. Time complexity: O(n*L + V + E) = O(n*L + E)
- Insert n words to trie:
  . each insert cost O(L)   (max tree height)
- Find starters for BFS: O(V)
- BFS: O(V + E)
- Produce result (join): O(V)

2. Space complexity: O(V + E) = O(n*L + E)
- trie: O(V)
- adjacency list: O(V + E)
- 'in_degree': O(V) 
- 'unique_letters': O(V)
- BFS queue: O(V)
"""
