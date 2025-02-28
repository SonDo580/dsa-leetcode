# You are given an integer array asteroids and 
# an integer mass representing the mass of a planet. 
# The planet will collide with the asteroids one by one - 
# you can choose the order. 
# If the mass of the planet is less than the mass of an asteroid, 
# the planet is destroyed. 
# Otherwise, the planet gains the mass of the asteroid. 
# Can you destroy all the asteroids?

# ===== Strategy =====
# - At any step, try to destroy the smallest asteroid.
#   If that's not possible, we cannot destroy all asteroids.
# -> We can sort the asteroids array then iterate through it once.

def can_destroy_all_asteroids(mass: int, asteroids: list[int]) -> bool:
    # sort the asteroids' masses array in ascending order
    asteroids.sort()

    for asteroid in asteroids:
        # check if the planet can destroy the smallest asteroid
        if asteroid > mass:
            return False
        
        # the planet gain the mass of the asteroid
        mass += asteroids

    return True

# ===== Complexity =====
# 
# Time complexity:
# - sort asteroids array: O(n*log(n))
# - iterate through asteroids array: O(n)
# => Overall: O(n*log(n))
#
# Space complexity:
# - depends on the sort function: 
# + build-in sort method of Python - timsort: O(n)
