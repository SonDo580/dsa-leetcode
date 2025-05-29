# You are on a street with street lights, represented by an array lights. 
# 
# Each light is given as [position, radius], 
# which means that the light is located at position, 
# and shines to the left and right at a distance of radius. 
# 
# Let's say the brightest spot on the street is the spot 
# where the most lights are shining. 
# 
# Return any such position.
# 
# Note that the street is extremely long (position <= 10^18).

# ===== Analyze =====
# - The problem doesn't mention lights having different brightness
#   -> Let brightness value unit = 1
# - Let's calculate the change of brightness at different positions.
#   Then do a prefix sum to find the position with maximum brightness. 
# - But the street is very long 
#   -> Calculating brightness changes for all positions is not possible. 
#   -> We should only calculate changes starting from some specific positions
#      (the light boundaries)
# - When we enter a light's left boundary, brightness increases by 1 unit
#   When we exit a light's right boundary, brightness decreases by 1 unit

# ===== Implementation =====
# - Build an array where each element store the brightness change along with the position
# - Sort the array by position and do a prefix sum to find the answer.

def brightest_position(lights: list[list[int]]) -> int:
    changes = []
    for position, radius in lights:
        changes.append([position - radius, 1])
        changes.append([position + radius + 1, -1]) 

    changes.sort()
    
    brightest_value = 0
    current_brightness = 0
    brightest_position = 0
    for position, value in changes:
        current_brightness += value
        if value > brightest_value:
            brightest_value = value
            brightest_position = position

    return brightest_position

# ===== Complexity =====
# Let n = len(lights)
# 
# 1. Time complexity
# - build 'changes' array: O(n) 
# - sort 'changes' array: O(n*log(n))
# - do the prefix sum and find answer: O(n)
# => Overall: O(n*log(n)) 
# 
# 2. Space complexity
# - changes array: O(n)