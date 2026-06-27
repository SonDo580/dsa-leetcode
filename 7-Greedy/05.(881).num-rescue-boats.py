"""
https://leetcode.com/problems/boats-to-save-people/

You are given an array 'people' where people[i] is the weight of the ith person,
and an infinite number of boats where each boat can carry a maximum weight of 'limit'.
Each boat carries at most two people at the same time,
provided the sum of the weight of those people is at most 'limit'.
Return the minimum number of boats to carry every given person.
"""

"""
Analysis:
- Let x denote the heaviest person, y denote the lightest person at any step.
- 2 cases:
  . x + y > limit:
    This means x can not pair with anyone (consume 1 boat),
    since y is already the lightest person.
  . x + y <= limit:
    This means y could pair with anyone, since x is already the heaviest person.
    To maximize "boats efficiency", we should pair y with the heaviest person, which is x.
    
Implementation:
- To keep track of the lightest and heaviest person at any time,
  sort the input and use 2 pointers from both ends.
"""


def num_rescue_boats(people: list[int], limit: int) -> int:
    num_boats = 0
    i = 0
    j = len(people) - 1

    people.sort()

    while i <= j:
        # Put the lightest person on the same boat
        # as the heaviest person if possible
        if people[i] + people[j] <= limit:
            i += 1

        # Put the heaviest person on a boat
        j -= 1

        num_boats += 1

    return num_boats


"""
Complexity:
- Let n = len(people)

1. Time complexity:
- Sort 'people': O(n*log(n))
- Iterate through 'people' with 2 pointers: O(n)
=> Overall: O(n*log(n))

2. Space complexity: O(n) for sorting (timsort).
"""


# === More detailed reasoning for x + y <= limit case ===
"""
- Number of boats to carry remaining people = R_boats
  Number of boats to carry all people = R_boats + 1
- Let try to pair y with another person rather than x.
- If x cannot be paired with anyone rather than y,
  -> x takes 1 boat alone.
- To keep the number of boats the same,
  we need an empty slot for y in remaining boats. 
  -> need a boat with 1 person, since y can be paired with anyone.
- [bad case] If all remaining boats are full (2 people on 1 boat),
  there's no empty slot for y (or a person must be out to let y in).
  -> next 1 extra boat.

=> Trying to pair y with another person rather than x
   may increase the number of boats required.
"""
