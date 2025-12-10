"""
https://leetcode.com/problems/online-stock-span/

Design an algorithm that collects daily price quotes for some stock
and returns the span of that stock's price for the current day.

The span of the stock's price in one day is the maximum number of consecutive days
(starting from that day and going backward) for which the stock price was less than or equal to the price of that day.

For example, if the prices of the stock in the last four days is [7,2,1,2] and the price of the stock today is 2,
then the span of today is 4 because starting from today,
the price of the stock was less than or equal 2 for 4 consecutive days.

Also, if the prices of the stock in the last four days is [7,34,1,2] and the price of the stock today is 8,
then the span of today is 3 because starting from today,
the price of the stock was less than or equal 8 for 3 consecutive days.

Implement the StockSpanner class:
StockSpanner() Initializes the object of the class.
int next(int price) Returns the span of the stock's price given that today's price is price.
"""

"""
First attempt (failed):
- Use a monotonically decreasing stack and push price onto it.
- Initialize each new price with a span of 1
- Pop stack elements that are less than or equal to current price.
  Increment the span every time we pop an element off.
-> If the next price is greater than or equal to the current price,
   this will produce the wrong answer, since some elements 
   may have been popped off by current price.

=> Strategy:
- Use a monotonically decreasing stack to store (prices & their spans).
- For each new price:
  - Initialize each new price with a span of 1 (for itself)
  - While the stack is not empty and the price at the top is less than or equal to the current price,
    pop the top element and add its span to the current span.
  - Push the current price and its span onto the stack
  - Return the span of the current price
"""

class StockSpanner:
    def __init__(self):
        # A monotonically-decreasing stack of price with its span
        self.stack: list[tuple[int, int]] = []

    def next(self, price: int) -> int:
        # Initialize span for the current price
        span: int = 1

        # Keep popping element with price <= current price
        # Add the spans of popped elements to current span
        while len(self.stack) > 0 and self.stack[-1][0] <= price:
            span += self.stack[-1][1]
            self.stack.pop()

        # Append current price and its span to the stack
        self.stack.append((price, span))
        return span


"""
Complexity:
- Let n be the number of next() calls

1. Time complexity:
- next() (arbitrary): O(n)
- next() (amortized): O(1)
  . each price is pushed once and popped at most once

2. Space complexity: O(n) for the stack
(the stack can grow to n elements if the prices only decrease)
"""