# Dynamic array

- Start with an initial size, then double the size each time we route out of space.
- Doubling process: Allocate a new array with size 2n, copy the contents of the old array to the lower half of the new one, and free space used by the old array _(`realloc` can reduce copying by expanding the current block if there's enough space)_

## Time complexity analysis

- Assume that the initial size is 1.
- It takes `log2(n)` doublings for the array to have n positions.
- After the last doubling (size=n/2 to size=n):
  - elements [n/4..n/2] (count=n/2) has been moved 1 time.
  - elements [n/8..n/4] (count=n/4) has been moved 2 times.
  - elements [n/16..n/8] (count=n/8) has been moved 3 times.
  - ...

- Number of items that has been moved: n / 2
- Total number of movements:

```
M = sum(i * (n / 2^i) for i in [1..log2(n)])
  = n * sum(i / 2^i for i in [1..log2(n)])
  < n * sum(i / 2^i for i in [1..inf])
  = n * 2
```

- On average, each item is moved:

```
m < (n * 2) / (n / 2)
  = 4 times
```

-> `push` is amortized O(1)

### Related proof 1:

`sum(i / 2^i for i in [1..inf]) = 2`

```
sum(i / 2^i for i in [1..inf])
= 1/2 + 2/4 + 3/8 + 4/16 + ...

- Break each term into sum of 1/2^i:
. 1/2 = 1/2
. 2/4 = 1/4 + 1/4
. 3/8 = 1/8 + 1/8 + 1/8
. 4/16 = 1/16 + 1/16 + 1/16 + 1/16
. ...

- Sum the columns:
. column 1: 1/2 + 1/4 + 1/8 + 1/16 + ... = 1
. column 2: 1/4 + 1/8 + 1/16 + ... = 1/2
. column 3: 1/8 + 1/16 + ... = 1/4
. ...

- Each column is a geometric series. Sum the results of columns:
. 1 + 1/2 + 1/4 + ... = 2
```

### Related proof 2:

Sum the first n items of geometric series: `a*r^i`

```
S = a + a*r + a*r^2 + ... + a*r^(n-1)
S*r = a*r + a*r^2 + a*r^3 ... + a*r^n
=> S*(r-1) = a*(r^n - 1)
=> S = a*(r^n - 1) / (r - 1)

If 0 < r < 1:
. r^n -> 0 when n -> inf
=> S = a / (1 - r)
```

- For our case:

```
. column 1: 1/2 + 1/4 + 1/8 + 1/16 + ...
=> a = 1/2, r = 1/2
=> S = 1/2 / (1 - 1/2) = 1

. column 2: 1/4 + 1/8 + 1/16 + ...
=> a = 1/4, r = 1/2
=> S = 1/4 / (1 - 1/2) = 1/2
```
