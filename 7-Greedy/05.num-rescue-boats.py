# You are given an array people where people[i] is the weight of the ith person,
# and an infinite number of boats where each boat can carry a maximum weight of limit.
# Each boat carries at most two people at the same time,
# provided the sum of the weight of those people is at most limit.
# Return the minimum number of boats to carry every given person.

# Example 1:
# Input: people = [1,2], limit = 3
# Output: 1
# Explanation: 1 boat (1, 2)

# Example 2:
# Input: people = [3,2,2,1], limit = 3
# Output: 3
# Explanation: 3 boats (1, 2), (2) and (3)

# Example 3:
# Input: people = [3,5,3,4], limit = 5
# Output: 4
# Explanation: 4 boats (3), (3), (4), (5)

# Constraints:
# 1 <= people.length <= 5 * 10^4
# 1 <= people[i] <= limit <= 3 * 10^4


# ===== Analyze =====
# Let x denote the heaviest person, y denote the lightest person at any step.
# There are 2 cases:
#
# 1. x + y > limit
# - This means x can not pair with anyone (consume 1 boat),
#   since y is already the lightest person.
#
# 2. x + y <= limit
# - This means y could pair with anyone, since x is already the heaviest person.
# - To maximize "boats efficiency", we should pair y with the heaviest person, which is x.

# ===== A more robust reasoning =====
# - Consider case: x + y <= limit
#   This means y can be paired with anyone, since x is heaviest.
# - Let z denote 1 of the remaining people.
#       R denote the set of remaining people without z.
# - Then Total_boat = R_boat U z_boat U x_boat U y_boat
#   (I'm using U to indicate that the boats may overlap)
# - y (lightest person) sits in 1 board. We have to decide whether y
#   should sit alone, pair with x, or pair with z.

# Consider 3 cases:
# + Let y sits alone:
#   Total_boat = (R_boat U z_boat U x_boat) + y_boat
#              = (R_boat U z_boat U x_boat) + 1
#             >= (R_boat U z_boat U x_boat) U y_boat
# => This can only increase the number of boats needed

# + Pair y with z:
#   Total_boat = R_boat U x_boat + z_boat
#              =  R_boat U x_boat + 1

# + Pair y with x:
#   Total_boat = R_boat U z_boat + x_boat
#              =  R_boat U z_boat + 1

# - Let's compare R_boat U x_boat and R_boat U z_boat
# + If we cannot merge z_boat into R_boat,
#   we also cannot merge x_boat into R_boat, since x is heavier than z
#   -> R_boat U x_boat = R_boat U z_boat = R_boat + 1
# + If we can merge z_boat into R_boat,
#   we may or may not be able to merge x_boat into R_boat
#   -> R_boat U x_boat >= R_boat U z_boat
# => In general: R_boat U x_boat >= R_boat U z_boat

# => We should always pair y with x

# ===== Implementation =====
# - To keep track of the lightest and heaviest person at any time,
#   sort the input and use 2 pointers from both ends.


def num_rescue_boats(people: list[int], limit: int) -> int:
    num_boats = 0
    i = 0
    j = len(people) - 1

    people.sort()

    while i <= j:
        # Put the lightest person on the same boat if possible
        if people[i] + people[j] <= limit:
            i += 1

        # Always put the heaviest person on a boat
        j -= 1

        num_boats += 1

    return num_boats


# ===== Complexity =====
# 1. Time complexity:
# - Sort 'people': O(n*log(n))
# - Iterate through 'people' with 2 pointers: O(n)
# => Overall: O(n*log(n))
#
# 2. Space complexity: depends on the sort function
# - built-in sort method of Python (timsort): O(n)

