## Why return left when looking for minimum answer

```python
left = lower_bound
right = upper_bound

while left <= right:
    mid = (left + right) // 2
    if is_valid(mid):
        right = mid - 1
    else:
        left = mid + 1

return left
```

- When we find a valid value, we want to search in the lower half to find a smaller valid one.
- Since the distance is continuously reduced, we must come across the minimum valid value `x` at some point.
- After checking `is_valid(x)`, we set `right = x - 1`. Now `x` is out of the search space.
- All subsequent calls to `is_valid` will fail. We will continuously increase `left` until `left = x - 1` (which is `right` right now).
- The check fail and we set `left = left + 1 = x`. The loop terminates because `left > right` and `left` is at the answer.

## Why return right when looking for maximum answer

```python
left = lower_bound
right = upper_bound

while left <= right:
    mid = (left + right) // 2
    if is_valid(mid):
        left = mid + 1
    else:
        right = mid - 1

return right
```

**_(The reasoning is similar)_**

- When we find a valid answer, we want to search in the upper half to find a greater valid one.
- Let's say the correct answer is `x`.
- Since the distance is continuously reduced, we must come across the maximum valid value `x` at some point.
- After checking `is_valid(x)`, we set `left = x + 1`. Now `x` is out of the search space.
- All subsequent call to `is_valid` will fail. We will continuously decrease `right` until `right = x + 1` (which is `left` right now).
- The check fail and we set `right = right - 1 = x`. The loop terminates because `left > right` and `right` is at the answer.

# Avoid confusion: Use a separate variable to track best answer

## Find minimum answer

```python
left = lower_bound
right = upper_bound
ans = right

while left <= right:
    mid = (left + right) // 2
    if is_valid(mid):
        ans = mid # update best answer so far
        right = mid - 1 # search better answer in the lower half
    else:
        left = mid + 1 # search valid answer in the upper half

return ans
```


## Find maximum answer

```python
left = lower_bound
right = upper_bound
ans = left

while left <= right:
    mid = (left + right) // 2
    if is_valid(mid):
        ans = mid # update best answer so far
        left = mid + 1 # search better answer in the upper half
    else:
        right = mid - 1 # search valid answer in the lower half

return ans
```