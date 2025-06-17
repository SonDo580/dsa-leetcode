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

- When we find a valid answer, we want to search in the lower half to find a smaller one.
- Let's say the correct answer is `x`.
- We must come across that value at some point (since the distance is continuously reduced).
- After doing `is_valid(x)`, we set `right = x - 1`. Now the answer (`x`) is out of the search space.
- Now every call to `is_valid` is going to fail. We will continuously increase `left` until `left = x - 1` (which is `right` right now).
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

- When we find a valid answer, we want to search in the upper half to find a smaller one.
- Let's say the correct answer is `x`.
- We must come across that value at some point (since the distance is continuously reduced).
- After doing `is_valid(x)`, we set `left = x + 1`. Now the answer (`x`) is out of the search space.
- Now every call to `is_valid` is going to fail. We will continuously decrease `right` until `right = x + 1` (which is `left` right now).
- The check fail and we set `right = right - 1 = x`. The loop terminates because `left > right` and `right` is at the answer.
