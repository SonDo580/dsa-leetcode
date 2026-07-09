"""
https://leetcode.com/problems/minimum-genetic-mutation/

A gene string can be represented by an 8-character long string,
with choices from 'A', 'C', 'G', and 'T'.

Suppose we need to investigate a mutation
from a gene string 'startGene' to a gene string 'endGene' where one mutation
is defined as one single character changed in the gene string.

For example, "AACCGGTT" --> "AACCGGTA" is one mutation.
There is also a gene bank 'bank' that records all the valid gene mutations.
A gene must be in bank to make it a valid gene string.

Given the two gene strings 'startGene' and 'endGene' and the gene bank 'bank',
return the minimum number of mutations needed to mutate from 'startGene' to 'endGene'.
If there is no such a mutation, return -1.

Note that the starting point is assumed to be valid,
so it might not be included in the bank.
"""

"""
Idea:
- Nodes are all valid genes: {'startGene'} | {genes in 'bank'}.
  Neighbors are mutations of current gene that exist in 'bank'.
- To generate all possible genes by mutating a gene:
  . Loop through each character and replace it with 1 of the other 3 characters.
  . If the new string are in bank, that's a valid mutation.
    -> Convert 'bank' to a set for faster check.
- Perform BFS from 'startGene'.
  When we reach 'endGene', return the minimum number of mutations.
"""

from collections import deque


def min_genetic_mutation(start_gene: str, end_gene: str, bank: list[str]) -> int:
    choices = ["A", "C", "G", "T"]
    bank_set = set(bank)

    def get_mutations(gene: str) -> list[str]:
        mutations: list[str] = []
        for i in range(len(gene)):
            for choice in choices:
                if choice == gene[i]:
                    continue
                mutation = f"{gene[:i]}{choice}{gene[i + 1:]}"
                if mutation in bank_set:
                    mutations.append(mutation)
        return mutations

    seen: set[str] = {start_gene}  # track visited genes
    
    # (gene, number of mutations so far)
    queue: deque[(str, int)] = deque([(start_gene, 0)])  

    while queue:
        gene, num_mutations = queue.popleft()
        if gene == end_gene:
            return num_mutations

        for next_gene in get_mutations(gene):
            if next_gene not in seen:
                seen.add(next_gene)
                queue.append((next_gene, num_mutations + 1))

    return -1


"""
Complexity:
- Number of characters in each gene string: n = 8
  Number of choices for each character: m = 4
  -> Number of possible genes: m^n
- Number of valid genes (number of nodes): 
  . N = len(bank) + (0 if start_gene in bank else 1)
      <= m^n

1. Time complexity: O(N + N*m*n^2) = O(N*m*n^2)
- Convert 'bank' to set: O(N)
- BFS:
  - Compute neighbors for each node: O(n*(m-1)*n) = O(m*n^2)
    . Loop through n characters.
      Try (m-1) other choices for each character.
      String concatenation to compute 1 neighbor: O(n)
  - Visit all edges of each node: O(m*n) 
    . each node has at most (m-1)*n neighbors.
  -> For all nodes: O(N * (m*n^2 + m*n)) = O(N*m*n^2)

2. Space complexity: O(N + m*n)
- 'seen': O(N)
- 'bank_set': O(N)
- queue: O(N') where N' < N (don't hold all nodes at once)
- neighbors: O(m*n) (each node has at most (m-1)*n neighbors)
"""
