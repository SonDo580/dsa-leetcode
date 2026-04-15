# String building

## Concatenation
- In most languages, strings are immutable -> concatenate a single character takes O(n) _(the original characters are copied to a new string)._
- Let say the final string has length `n` and we build it 1 character at a time by concatenation. Time complexity is:

```
1 + 2 + ... + n = n * (n + 1) / 2
-> O(n^2)
```

- Example:

```python
def build_string():
    final_str = ""
    for i in range(n):
        # Creates a NEW string copy every single time
        final_str += str(i)
    return final_str
```

## Better ways

```python
def build_string() -> str:
    parts: list[str] = []
    for i in range(n):
        # append is amortized O(1)
        parts.append(str(i)) 
    return "".join(parts)
```

- Time complexity: O(n)

```
- Append characters to `arr`: O(n)
- Convert `arr` to string: O(n)
=> Total: O(2*n) = O(n)
```

# Sub-array/sub-string, subsequence, subset

- Sub-array/sub-string: a contiguous section of the array/string.
- Subsequence: a set of elements of the array/string that keep the relative order but doesn't need to be contiguous.
- Subset: any set of elements from the array/string (subsets contain the same elements are considered the same, order doesn't matter).
