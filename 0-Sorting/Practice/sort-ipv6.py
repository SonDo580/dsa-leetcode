"""
Given a list of IPv6 addresses, sort them in ascending order.
"""

"""
Idea:
- Use byte-wise radix sort similar to IPv4 sorting,
  but need 16 passes instead of 4 (128 bits vs. 32 bits).
- Parsing attention: compressed IPv6 (::), leading 0's, ...
  -> Use 'ipaddress' library
"""

import ipaddress


def ip_to_int(ip: str) -> int:
    """Convert IPv6 address to 128-bit integer."""
    return int(ipaddress.IPv6Address(ip))


def int_to_ip(x: int) -> str:
    """Convert 128-bit integer to IPv6 address (canonical compressed form)."""
    return str(ipaddress.IPv6Address(x))


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


def radix_sort(ips: list[str]) -> None:
    # Convert IPv66 addresses to 128-bit integers
    nums = [ip_to_int(ip) for ip in ips]

    # Sort by each byte (LSB to MSB, 16 bytes)
    for shift in range(0, 128, 8):
        counting_sort_by_byte(nums, shift)

    # Convert 128-bit integers back to IPv6 addresses
    ips[:] = [int_to_ip(x) for x in nums]


"""
Complexity: (same as sorting IPv4)

Note: The above implementation can change the input string.
      All outputs are normalized to IPv6 canonical compressed format. 
"""


# ===== Example usage =====
ips = [
    "::",
    "2001:db8::1",
    "2001:0db8:0000:0000:0000:0000:0000:0001",
    "fe80::1",
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
    "2001:db8:85a3::8a2e:370:7334",
    "::1",
    "2001:4860:4860::8888",
]

expected = [
    "::",
    "::1",
    "2001:db8::1",
    "2001:db8::1",  # compressed 2001:0db8:0000:0000:0000:0000:0000:0001
    "2001:db8:85a3::8a2e:370:7334",
    "2001:4860:4860::8888",
    "fe80::1",
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
]

radix_sort(ips)
assert ips == expected


# ======== PRESERVE ORIGINAL STRINGS ==========
"""
Idea: 
- Keep the original string attached to its integer value.
- Sort by the integer values.
- Extract the strings after sorting.
"""


def counting_sort_by_byte(pairs: list[tuple[int, str]], shift: int) -> None:
    # Count frequency for each byte value
    base = 256
    count = [0] * base
    for num, _ in pairs:
        byte = (num >> shift) & 255
        count[byte] += 1

    # Compute cumulative count
    for i in range(1, base):
        count[i] += count[i - 1]

    # Build sorted array
    sorted_arr = [None] * len(pairs)
    for num, addr in reversed(pairs):
        byte = (num >> shift) & 255
        sorted_arr[count[byte] - 1] = (num, addr)
        count[byte] -= 1

    # Copy sorted array back to original array
    pairs[:] = sorted_arr


def radix_sort(ips: list[str]) -> None:
    # Decorate: attach numeric key, keep original string
    pairs = [(ip_to_int(ip), ip) for ip in ips]

    # Sort by numeric key
    for shift in range(0, 128, 8):
        counting_sort_by_byte(pairs, shift)

    # Extract original strings
    ips[:] = [addr for _, addr in pairs]


# ===== Example usage =====
ips = [
    "::",
    "2001:db8::1",
    "2001:0db8:0000:0000:0000:0000:0000:0001",
    "fe80::1",
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
    "2001:db8:85a3::8a2e:370:7334",
    "::1",
    "2001:4860:4860::8888",
]

expected = [
    "::",
    "::1",
    "2001:db8::1",
    "2001:0db8:0000:0000:0000:0000:0000:0001",  # original string
    "2001:db8:85a3::8a2e:370:7334",
    "2001:4860:4860::8888",
    "fe80::1",
    "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff",
]

radix_sort(ips)
assert ips == expected
