"""
https://leetcode.com/problems/solving-questions-with-brainpower/

You are given a 0-indexed 2D integer array questions
where questions[i] = [points_i, brainpower_i].

The array describes the questions of an exam,
where you have to process the questions in order
(i.e., starting from question 0) and make a decision
whether to solve or skip each question.

Solving question i will earn you points_i points
but you will be unable to solve each of the next brainpower_i questions.
If you skip question i, you get to make the decision on the next question.

For example, given questions = [[3, 2], [4, 3], [4, 4], [2, 5]]:
If question 0 is solved, you will earn 3 points
but you will be unable to solve questions 1 and 2.
If instead, question 0 is skipped and question 1 is solved,
you will earn 4 points but you will be unable to solve questions 2 and 3.

Return the maximum points you can earn for the exam.
"""

"""
Identify DP problem:
- asking for maximum points
- local decision (take or skip question) affect future decisions.

Analysis:
- dp(i): return the maximum points achievable from question i onward
  (not maximum points upto question i)
  -> dp(0) give max points achievable for the whole exam
- At question[i], we have 2 options:
  . solve it: gain question[i][0] points, but can not solve the next
    question[i][1] questions
    -> next question index: j = i + question[i][1] + 1
    -> max points from i: question[i][0] + dp(j)
  . skip it -> max points from i: dp(i + 1)
  => Recurrence relation:
     . dp(i) = max(questions[i][0] + dp(j), dp(i + 1))
       where j = i + question[i][1] + 1
- When i >= questions.length, we cannot get any more points
  -> Base case: dp(i) = 0 where i >= questions.length
"""


# ===== Top-down =====
def most_points(questions: list[list[int]]) -> int:
    def dp(i: int) -> int:
        if i >= len(questions):
            return 0

        if i in memo:
            return memo[i]

        j = i + questions[i][1] + 1
        memo[i] = max(questions[i][0] + dp(j), dp(i + 1))
        return memo[i]

    memo: dict[int, int] = {}
    return dp(0)


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n) for memoization and recursion stack
"""


# ===== Bottom-up =====
def most_points(questions: list[list[int]]) -> int:
    n = len(questions)

    dp = [0] * (n + 1)
    # dp[n] is always 0, representing the base case (no questions remain)

    for i in range(n - 1, -1, -1):
        j = min(i + questions[i][1] + 1, n)  # avoid out of bound error
        dp[i] = max(questions[i][0] + dp[j], dp[i + 1])

    return dp[0]


"""
Complexity:
1. Time complexity: O(n)
2. Space complexity: O(n) for 'dp' array
   . cannot be improved because the recurrence relation is not static
     (j depends on questions[i][1]).
"""


# === INEFFICIENT: dp(i) as max points achievable upto question i ===
"""
- dp(n-1) give max points achievable for the whole exam
- Base cases:
  . dp(0) = question[0][0] (only 1 question to answer)
  . dp(1) = max(question[0][0], question[1][0])
    (pick the one with more scores)
- At question[i]:
  . skip it -> max points upto i: dp(i) = dp(i - 1)
  . solve it: dp(i) = max(dp(k))
    where k < i and question[k] doesn't lock question[i]
    (k + question[k][1] < i)
    -> O(n^2) to process all questions
"""
