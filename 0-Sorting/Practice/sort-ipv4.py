"""
Given a list of IPv4 addresses, sort them in ascending order.
"""


# ========== Approach 1: Tim sort ==========
# ==========================================
def tim_sort(ips: list[str]) -> None:
    ips.sort(key=ip_to_int)


# ========== Approach 2: Radix sort ==========
# ============================================
"""
Idea:
- Each IPv4 address has format: A.B.C.D (4 bytes)
  where 0 <= A, B, C, D <= 255
- Use radix sort with 4 passes (D -> A),
  each pass uses counting sort with base = 256 
"""


def radix_sort(ips: list[str]) -> None:
    # Convert IPv4 addresses to 32-bit integers
    nums = [ip_to_int(ip) for ip in ips]

    # Sort by each byte (LSB -> MSB)
    for shift in [0, 8, 16, 24]:
        counting_sort_by_byte(nums, shift)

    # Convert 32-bit integers back to IPv4 addresses
    ips[:] = [int_to_ip(x) for x in nums]


def counting_sort_by_byte(nums: list[int], shift: int) -> None:
    # Count frequency for each byte value
    base = 256
    count = [0] * base
    for num in nums:
        byte = (num >> shift) & 255
        count[byte] += 1

    # Compute cumulative count
    for i in range(1, base):
        count[i] += count[i - 1]

    # Build sorted array
    sorted_arr = [0] * len(nums)
    for num in reversed(nums):
        byte = (num >> shift) & 255
        sorted_arr[count[byte] - 1] = num
        count[byte] -= 1

    # Copy sorted array back to original array
    nums[:] = sorted_arr


def parse_ip(ip: str) -> tuple[int, int, int, int]:
    """Parse IPv4 address into 4 integer components."""
    return tuple(map(int, ip.split(".")))


def ip_to_int(ip: str) -> int:
    """Convert IPv4 address to 32-bit integer."""
    a, b, c, d = parse_ip(ip)
    return (a << 24) | (b << 16) | (c << 8) | d


def int_to_ip(x: int) -> str:
    """Convert 32-bit integer back to IPv4 address."""
    return ".".join(
        map(
            str,
            [
                (x >> 24) & 255,
                (x >> 16) & 255,
                (x >> 8) & 255,
                x & 255,
            ],
        )
    )


"""
Complexity:
- Let n = len(ips)
      d = number of passes (4 -> constant)
      b = base (256 -> constant) 
      l = max IPv4 string length (constant)

1. Time complexity:
- Convert IPv4 addresses to integers: O(n * l)
- Counting sort by each byte: O(d * (n + b))
- Convert integers back to IPv4: O(n * l)
=> Overall: O(n * l + d * (n + b)) ~ O(n)

2. Space complexity:
- 'nums': O(n)
- counting sort memory: O(n + b)
- temp array for output conversion: O(n)
=> Overall: O(n + b) ~ O(n)
"""

# ===== Example usage =====
ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1", "8.8.8.8", "255.255.255.0"]
sorted_ips = ["8.8.8.8", "10.0.0.1", "172.16.0.1", "192.168.1.1", "255.255.255.0"]
radix_sort(ips)
assert ips == sorted_ips
