"""
https://leetcode.com/problems/24-game/

You are given an integer array cards of length 4.
You have four cards, each containing a number in the range [1, 9].
You should arrange the numbers on these cards in a mathematical expression
using the operators ['+', '-', '*', '/']
and the parentheses '(' and ')' to get the value 24.

You are restricted with the following rules:
- The division operator '/' represents real division, not integer division.
  . For example, 4 / (1 - 2 / 3) = 4 / (1 / 3) = 12.
- Every operation done is between two numbers.
  In particular, we cannot use '-' as a unary operator.
  . For example, if cards = [1, 1, 1, 1], the expression "-1 - 1 - 1 - 1" is not allowed.
- You cannot concatenate numbers together
  . For example, if cards = [1, 2, 1, 2], the expression "12 + 12" is not valid.

Return true if you can get such expression that evaluates to 24, and false otherwise.
"""

"""
Idea:
- Combine the ideas of '(46).permutations' and '(241).ways-to-add-parens'.
- Backtracking 1: Generate all possible permutations of cards
- Backtracking 2:
  . Try splitting each permutation with a root operator.
  . Recurse on the left/right part to generate the list of first/second operands.
  . Compute results for all operand pairs. Return True if can achieve 24.
  . Use a set for unique results since we just need to check, not generate all.
"""

from typing import Callable

OPERATIONS: dict[str, Callable[[int, int], int]] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,  # avoid division by 0 when grouping
}


def _bin_op(op: str, a: int, b: int) -> float:
    assert op in OPERATIONS
    return OPERATIONS[op](a, b)


def _permute(cards: list[int]) -> list[list[int]]:
    """Generate all possible permutations of cards."""
    n = len(cards)
    ans: list[list[int]] = []

    def _build(curr: list[int], used: list[bool]) -> None:
        if len(curr) == n:
            ans.append(curr[:])
            return

        for i in range(n):
            if not used[i]:
                curr.append(cards[i])
                used[i] = True
                _build(curr, used)
                curr.pop()
                used[i] = False

    _build(curr=[], used=[False] * n)
    return ans


def judge_point_24(cards: list[int]) -> bool:
    def _group(cards: list[int], left: int, right: int) -> set[float]:
        """Compute results for different groupings of cards[left..right]."""
        if left == right:  # 1 number remaining
            return set([cards[left]])

        results: set[float] = set()
        for i in range(left, right):
            # Try each operator as root between cards[..i] and cards[i+1..]
            for op in OPERATIONS.keys():
                # Recurse to generate all possible operands
                a_set = _group(cards, left, i)
                b_set = _group(cards, i + 1, right)

                # Try all operand pairs
                for b in b_set:
                    # Avoid division by 0
                    if op == "/" and b == 0:
                        continue

                    for a in a_set:
                        results.add(_bin_op(op, a, b))

        return results

    permutations = _permute(cards)
    for p in permutations:
        results = _group(p, left=0, right=len(p) - 1)
        for r in results:
            if abs(r - 24) < 1e-6:
                # allow small rounding error
                return True

    return False


"""
Complexity: TODO
"""


# === Avoid rounding issue: division as fraction ===
"""
- This approach is more verbose.
- Use an object/tuple to represent numerator and denominator.
- Check equal to 24:
  . integer result: x == 24
  . fraction result: numerator = 24 * denominator
"""

Fraction = tuple[int, int]
Operand = int | Fraction


class Ops:
    """Handle both integer and fraction operations."""

    @staticmethod
    def _extract_components(x: Operand) -> tuple[int, int]:
        """Extract numerator and denominator."""
        if isinstance(x, int):
            return (x, 1)
        return x

    @staticmethod
    def _normalize(numerator: int, denominator: int) -> Operand:
        """Reduce fraction to integer if possible."""
        assert denominator != 0
        if denominator == 1:
            return numerator
        if numerator == 0:
            return 0
        if numerator % denominator == 0:
            return numerator // denominator
        return (numerator, denominator)

    @staticmethod
    def add(a: Operand, b: Operand) -> Operand:
        """Perform addition between integers/fractions."""
        if isinstance(a, int) and isinstance(b, int):
            return a + b

        na, da = Ops._extract_components(a)
        nb, db = Ops._extract_components(b)
        n = (na * db) + (nb * da)
        d = da * db
        return Ops._normalize(n, d)

    @staticmethod
    def subtract(a: Operand, b: Operand) -> Operand:
        """Perform subtraction between integers/fractions."""
        if isinstance(a, int) and isinstance(b, int):
            return a - b

        na, da = Ops._extract_components(a)
        nb, db = Ops._extract_components(b)
        n = (na * db) - (nb * da)
        d = da * db
        return Ops._normalize(n, d)

    @staticmethod
    def multiply(a: Operand, b: Operand) -> Operand:
        """Perform multiplication between integers/fractions."""
        if isinstance(a, int) and isinstance(b, int):
            return a * b

        na, da = Ops._extract_components(a)
        nb, db = Ops._extract_components(b)
        n = na * nb
        d = da * db
        return Ops._normalize(n, d)

    @staticmethod
    def divide(a: Operand, b: Operand) -> Operand:
        """Perform division between integers/fractions."""
        if b == 0:
            raise ValueError("division by 0")

        na, da = Ops._extract_components(a)
        nb, db = Ops._extract_components(b)
        n = na * db
        d = da * nb
        return Ops._normalize(n, d)


OPERATIONS: dict[str, Callable[[Operand, Operand], Operand]] = {
    "+": Ops.add,
    "-": Ops.subtract,
    "*": Ops.multiply,
    "/": Ops.divide,
}


def _bin_op(op: str, a: Operand, b: Operand) -> Operand:
    assert op in OPERATIONS
    return OPERATIONS[op](a, b)


def judge_point_24(cards: list[int]) -> bool:
    def _group(cards: list[int], left: int, right: int) -> set[Operand]:
        """Compute results for all different grouping of cards[left..right]."""
        if left == right:  # 1 number remaining
            return set([cards[left]])

        results: set[Operand] = set()
        for i in range(left, right):
            # Try each operator as root between cards[..i] and cards[i+1..]
            for op in OPERATIONS.keys():
                # Recurse to generate possible operands
                a_set = _group(cards, left, i)
                b_set = _group(cards, i + 1, right)

                # Try all operand pairs
                for b in b_set:
                    # Avoid division by 0
                    if op == "/" and b == 0:
                        continue

                    for a in a_set:
                        results.add(_bin_op(op, a, b))

        return results

    permutations = _permute(cards)
    for p in permutations:
        results = _group(p, left=0, right=len(p) - 1)

        # Quick check for integers
        if 24 in results:
            return True

        # Check fractions
        for result in results:
            if isinstance(result, tuple) and result[0] == 24 * result[1]:
                return True

    return False


"""
Complexity: TODO
"""
