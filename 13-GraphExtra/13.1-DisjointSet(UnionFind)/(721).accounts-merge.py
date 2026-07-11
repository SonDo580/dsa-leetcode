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
  Number of (reduced) edges: E = k * (l - 2) = O(k*l) = O(N)

1. Time complexity: O(N + E + N*log(N)) = O(N*log(N))
- Build adjacency list: O(E)
- DFS across k iterations: O(N + E)
  . visit each node once, each edge twice.
- Sorting: O(N*log(N))

2. Space complexity: O(k + N + E) = O(N)
- 'graph': O(k + E)
- 'email_to_name': O(k)
- 'visited': O(N)
- sorting: O(N)
- DFS recursion stack: O(N)

=== Sorting worst case: when all emails are by the same person ===
Proof: n1 + n2 = n -> n1*log(n1) + n2*log(n2) < n*log(n)
. Divide both sides by log(n):
  n1*(log(n1)/log(n)) + n2*(log(n2)/log(n)) < n
. n1 < n, n2 < n -> log(n1)/log(n) < 1, log(n2)/log(n) < 1
  -> n1*(log(n1)/log(n)) + n2*(log(n2)/log(n)) < n1 + n2 = n
"""
