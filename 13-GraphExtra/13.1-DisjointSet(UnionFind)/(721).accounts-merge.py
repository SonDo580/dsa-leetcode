"""
https://leetcode.com/problems/accounts-merge/

Given a list of accounts where each element accounts[i] is a list of strings,
where the first element accounts[i][0] is a name,
and the rest of the elements are emails representing emails of the account.

Now, we would like to merge these accounts.
Two accounts definitely belong to the same person if there is some common email to both accounts.
Note that even if two accounts have the same name,
they may belong to different people as people could have the same name.
A person can have any number of accounts initially,
but all of their accounts definitely have the same name.

After merging the accounts,
return the accounts in the following format:
the first element of each account is the name,
and the rest of the elements are emails in sorted order.
The accounts themselves can be returned in any order.

Example:
- Input: accounts = [
["John","johnsmith@mail.com","john_newyork@mail.com"],
["John","johnsmith@mail.com","john00@mail.com"],
["Mary","mary@mail.com"],
["John","johnnybravo@mail.com"]]

- Output: [
["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],
["Mary","mary@mail.com"],
["John","johnnybravo@mail.com"]]
"""

# === Approach 1: BFS/DFS ===
"""
Idea:
- Emails are nodes in an undirected graph.
  Each email has neighbors as all other emails in the same account entry.
  -> Emails of the same person (across account entries) form a connected component.  

Implement:
- Build adjacency list.
- Perform DFS/BFS from each node.
  Record person name and visited nodes for the connected component.
  Sort the visited emails at the end.
- To find person name for a connected component,
  choose at least 1 email in it to map person name.
  -> Use the 1st email in each account entry.
     (Other emails in the same account entry don't need mappings,
      since they will be in the same connected component).
- Start a new connected component if a node hasn't been visited in previous traversals.
- Choosing start node: Use 1st email of each entry, 
  since we map that email to person name for the whole component)
- Optimize:
  We don't need all edges between emails of the same account entry,
  just enough edges so all nodes can reach each other.
  -> Only record edges from 1st email to other emails.
     Don't need edges between other emails.
"""

from collections import defaultdict


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    # - build adjacency list
    # - record person name for each connected component
    graph: defaultdict[str, list[str]] = defaultdict(list)
    email_to_name: dict[str, str] = {}
    for account in accounts:
        # use 1st email of each account entry
        # (guarantee at least 1 representative node for each component)
        first_email = account[1]
        name = account[0]
        email_to_name[first_email] = name

        # only record bidirectional edges from 1st email to other emails
        # (don't need edges between other emails)
        for i in range(2, len(account)):
            graph[first_email].append(account[i])
            graph[account[i]].append(first_email)

    merged_accounts: list[list[str]] = []
    visited: set[str] = set()  # track visited node across traversals

    def _dfs_recur(email: str, merged_emails: list[str]) -> None:
        for neighbor in graph[email]:
            if neighbor not in visited:
                merged_emails.append(neighbor)
                visited.add(neighbor)
                _dfs_recur(neighbor, merged_emails)

    for account in accounts:
        first_email = account[1]
        if first_email not in visited:
            # start a new connected component (merged account)
            merged_emails: list[str] = [first_email]
            visited.add(first_email)
            _dfs_recur(first_email, merged_emails)

            name = email_to_name[first_email]
            merged_emails.sort()
            merged_accounts.append([name] + merged_emails)

    return merged_accounts


"""
Complexity:
- Let k = len(accounts), l = average len(account[i])
- Number of nodes: N = number of unique emails = O(k*l)
  Number of (reduced) edges: E = k * (l - 2) = O(k*l)

1. Time complexity: O(N + E + N*log(N)) = O(k*l*log(k*l))
- Build adjacency list: O(E)
- DFS across k iterations: O(N + E)
  . visit each node once, each edge twice.
- Sorting + array concatenation: O(N*log(N) + N) = O(N*log(N))

2. Space complexity: O(k + N + E) = O(k*l)
- 'graph': O(k + E)
- 'email_to_name': O(k)
- 'visited': O(N)
- Sorting: O(N) (timsort)
- DFS recursion stack: O(N)

=== Sorting worst case: when all emails are by the same person ===
Proof: n1 + n2 = n -> n1*log(n1) + n2*log(n2) < n*log(n)
. Divide both sides by log(n):
  n1*(log(n1)/log(n)) + n2*(log(n2)/log(n)) < n
. n1 < n, n2 < n -> log(n1)/log(n) < 1, log(n2)/log(n) < 1
  -> n1*(log(n1)/log(n)) + n2*(log(n2)/log(n)) < n1 + n2 = n
"""


# === Approach 2: UnionFind ===
"""
Idea:
- Similar to approach 1, only consider the reduced set of edges
  (for each account entry: 1 edge from 1st email to each other email).
- Implementation note:
  . Use hashmap for internal data structures of UnionFind.
- Iterate through edges and and perform union operations.
- Group emails at the end:
  . Iterate through each entry of uf.ancestor.
  . Perform find(key) to get correct root (can be stale after an union).
  . Keys (emails) with the same root form a connected component.
- To find name for each connected component,
  choose the root in each component tree to map name to.
  -> For a root to be the 1st email of 1 account entry,
     when performing union:
     . If height[x] == height[y], must choose x to be the root.
       Since for the same account entry: x is 1st email, y is another email.
     . It doesn't matter when merging 2 different account entries (height[x] == height[y]),
       since the root will be among the 2 1st emails -> use the same logic.
- For account entry with 1 email, there're no edges to add.
  But we still need the node to exists in uf.ancestor
  -> Perform union for the 1st email with itself.
"""


class UnionFind:
    """Implement path compression and union by rank."""

    def __init__(self):
        # root of component tree each node is in
        # (can become stale after an union)
        self.ancestor: dict[str, str] = {}

        # height of each subtree
        self.height: dict[str, int] = {}

    def find(self, x: str) -> str:
        """Find root of connected component tree that x is in."""
        if x != self.ancestor[x]:
            # record roots for ancestor on the chain
            # when recursion stack unwinds
            self.ancestor[x] = self.find(self.ancestor[x])
        return self.ancestor[x]

    def union(self, x: str, y: str) -> None:
        """Add edge (x, y). May merge 2 connected components."""
        if x not in self.ancestor:
            self.ancestor[x] = x
            self.height[x] = 0
        if y not in self.ancestor:
            self.ancestor[y] = y
            self.height[y] = 0

        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return

        if self.height[root_x] > self.height[root_y]:
            self.ancestor[root_y] = root_x
        elif self.height[root_x] < self.height[root_y]:
            self.ancestor[root_x] = root_y
        else:
            # Important: must choose root_x as new root
            self.ancestor[root_y] = root_x
            self.height[root_x] += 1


def accounts_merge(accounts: list[list[str]]) -> list[list[str]]:
    uf = UnionFind()

    # map 1st email of each account entry to person name
    email_to_name: dict[str, str] = {}

    for account in accounts:
        name = account[0]
        first_email = account[1]
        email_to_name[first_email] = name

        # include first_email itself
        for i in range(1, len(account)):
            uf.union(first_email, account[i])

    # group emails with the same root
    components: defaultdict[str, list[str]] = defaultdict(list)
    for email in uf.ancestor:
        root = uf.find(email)  # fix possibly stale root
        components[root].append(email)

    # sort emails in each group and produce result
    merged_accounts: list[list[str]] = []
    for root in components:
        name = email_to_name[root] # root is a 1st email
        components[root].sort()
        merged_accounts.append([name] + components[root])

    return merged_accounts


"""
Complexity:
- Let k = len(accounts), l = average len(account[i])
- Number of nodes: N = number of unique emails = O(k*l)
  Number of (reduced) edges: E = O(k*l)

1. Time complexity: O(E + N + N*log(N)) = O(k*l*log(k*l))
- Iterate through E edges (nested loop): O(E)
  . each union(): ~~O(1)
- Iterate through uf.ancestor to group emails: O(N)
  . each find(): ~~O(1)
- Sorting + array concatenation: O(N*log(N) + N) = O(N*log(N))
  . worst case: all emails are of the same person

2. Space complexity: O(N + k) = O(k*l)
- 'uf': O(N)
- 'email_to_name': O(k)
- 'components': O(N) 
- Sorting: O(N) (timsort)
"""