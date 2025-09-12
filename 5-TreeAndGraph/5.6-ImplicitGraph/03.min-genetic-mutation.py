# A gene string can be represented by an 8-character long string,
# with choices from 'A', 'C', 'G', and 'T'.
#
# Suppose we need to investigate a mutation
# from a gene string startGene to a gene string endGene where one mutation
# is defined as one single character changed in the gene string.
#
# For example, "AACCGGTT" --> "AACCGGTA" is one mutation.
# There is also a gene bank 'bank' that records all the valid gene mutations.
# A gene must be in bank to make it a valid gene string.
#
# Given the two gene strings startGene and endGene and the gene bank 'bank',
# return the minimum number of mutations needed to mutate from startGene to endGene.
# If there is no such a mutation, return -1.

# Note that the starting point is assumed to be valid,
# so it might not be included in the bank.

# Example 1:
# Input: startGene = "AACCGGTT", endGene = "AACCGGTA", bank = ["AACCGGTA"]
# Output: 1

# Example 2:
# Input: startGene = "AACCGGTT", endGene = "AAACGGTA", bank = ["AACCGGTA","AACCGCTA","AAACGGTA"]
# Output: 2

# Constraints:
# 0 <= bank.length <= 10
# startGene.length == endGene.length == bank[i].length == 8
# startGene, endGene, and bank[i] consist of only the characters ['A', 'C', 'G', 'T'].


# ===== Strategy =====
# - Perform a BFS starting from startGene.
#   When we reach endGene that the minimum number of mutations.
# - Treat all possible genes as nodes.
# - Neighbors are genes produced by mutating current gene, and exist in bank

# ===== Implementation notes =====
# - To generate all possible genes by mutating a gene:
#   + Loop through each character and replace it with 1 of the other 3 characters.
#   + If the new string are in bank, that's a valid mutation.
# - Convert 'bank' to a set for faster check

from collections import deque


def min_genetic_mutation(start_gene: str, end_gene: str, bank: list[str]) -> int:
    choices = ["A", "C", "G", "T"]
    bank_set = set(bank)

    def get_mutations(gene: str) -> list[str]:
        mutations: list[str] = []
        for i in range(len(gene)):
            for choice in choices:
                if choice != gene[i]:
                    mutation = f"{gene[:i]}{choice}{gene[i + 1:]}"
                    if mutation in bank_set:
                        mutations.append(mutation)
        return mutations

    seen: set[str] = {start_gene}  # track visited genes
    queue: deque[(str, int)] = deque([(start_gene, 0)])  # gene, number of mutations

    while queue:
        gene, num_mutations = queue.popleft()

        if gene == end_gene:
            return num_mutations

        for next_gene in get_mutations(gene):
            if next_gene not in seen:
                seen.add(next_gene)
                queue.append((next_gene, num_mutations + 1))

    return -1
