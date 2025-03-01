# You are given a 0-indexed 2D integer array questions 
# where questions[i] = [points_i, brainpower_i].

# The array describes the questions of an exam, 
# where you have to process the questions in order 
# (i.e., starting from question 0) and make a decision 
# whether to solve or skip each question. 

# Solving question i will earn you points_i points 
# but you will be unable to solve each of the next brainpower_i questions. 
# If you skip question i, you get to make the decision on the next question.

# For example, given questions = [[3, 2], [4, 3], [4, 4], [2, 5]]:
# If question 0 is solved, you will earn 3 points 
# but you will be unable to solve questions 1 and 2.
# If instead, question 0 is skipped and question 1 is solved, 
# you will earn 4 points but you will be unable to solve questions 2 and 3.
# Return the maximum points you can earn for the exam.
 
# Example 1:
# Input: questions = [[3,2],[4,3],[4,4],[2,5]]
# Output: 5
# Explanation: The maximum points can be earned by solving questions 0 and 3.
# - Solve question 0: Earn 3 points, will be unable to solve the next 2 questions
# - Unable to solve questions 1 and 2
# - Solve question 3: Earn 2 points
# Total points earned: 3 + 2 = 5. There is no other way to earn 5 or more points.

# Example 2:
# Input: questions = [[1,1],[2,2],[3,3],[4,4],[5,5]]
# Output: 7
# Explanation: The maximum points can be earned by solving questions 1 and 4.
# - Skip question 0
# - Solve question 1: Earn 2 points, will be unable to solve the next 2 questions
# - Unable to solve questions 2 and 3
# - Solve question 4: Earn 5 points
# Total points earned: 2 + 5 = 7. There is no other way to earn 7 or more points.

# Constraints:
# 1 <= questions.length <= 10^5
# questions[i].length == 2
# 1 <= points_i, brainpower_i <= 10^5


# ===== Identify DP problem =====
# - asking for maximum points
# - local decision (take or skip question) affect future decisions.

# ===== Analyze =====
# - dp(i): return the maximum points achievable from question i
#   (not maximum points upto question i)
# 
# - At question[i], we have 2 options:
# + solve it: gain question[i][0] points, but can not solve the next
#   question[i][1] questions
#   -> next question index: j = i + question[i][1] + 1
#   -> total scores: question[i][0] + dp(j)
# + skip it -> total scores: dp(i + 1)
# 
# => Recurrence relation: dp(i) = max(questions[i][0] + dp(j), dp(i + 1))
#    where j = i + i + question[i][1] + 1
# 
# - When i >= questions.length, we cannot get any more points
# => Base case: dp(i) = 0
#    where i >= questions.length


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


# ===== Bottom-up =====
def most_points(questions: list[list[int]]) -> int:
    n = len(questions)
    
    dp = [0] * (n + 1) 
    # dp[n] is always 0, representing the base case (no questions remain)
    # to avoid out of bound error 
    
    for i in range(n - 1, -1, -1):
        j = min(i + questions[i][1] + 1, n)
        dp[i] = max(questions[i][0] + dp[j], dp[i + 1])

    return dp[0]


# ===== Complexity =====
# Time complexity: O(n)
# Space complexity: O(n) 
# 
# - There are O(n) states (n = questions.length), each costs O(1) to compute.
# - We cannot improve space complexity because the recurrence relation is not static.
#   (depends on questions[i][1])