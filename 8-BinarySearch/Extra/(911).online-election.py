"""
https://leetcode.com/problems/online-election

You are given two integer arrays persons and times.
In an election, the ith vote was cast for persons[i] at time times[i].

For each query at a time t, find the person that was leading the election at time t.
Votes cast at time t will count towards our query.
In the case of a tie, the most recent vote (among tied candidates) wins.

Implement the TopVotedCandidate class:
- TopVotedCandidate(int[] persons, int[] times) Initializes the object with the persons and times arrays.
- int q(int t) Returns the number of the person that was leading the election at time t according to the mentioned rules.
"""

"""
Idea:
- First we need to find the last T in 'times' such that T <= t
  -> find the first T such that T > t then use T' right before T
  -> use bisect right / upper bound
- Next, find the top-voted candidate from t=0 upto that bound.
  We can do this in advance to reduce query time.
  + Use a list to record top-voted candidate upto times[i].
    Use a dictionary to count number of votes for each candidate.
  + Loop through 'persons':
    . Increment number of votes for current person.
    . If current number of votes >= max number of votes,
      update max number of votes and top-voted candidate
      (the most recent vote wins if there's a tie)
"""

import bisect
from collections import defaultdict


class TopVotedCandidate:

    def __init__(self, persons: list[int], times: list[int]):
        self.persons = persons
        self.times = times
        self.top_voted_records = self.__build_top_voted_records()

    def __build_top_voted_records(self) -> list[int]:
        """Record the top-voted candidate at each point in 'times'."""
        top_voted_records: list[int] = []
        votes_count: defaultdict[int, int] = defaultdict(int)
        top_voted = -1  # arbitrary, will be overwrite
        max_votes = 0

        for person in self.persons:
            votes_count[person] += 1
            if votes_count[person] >= max_votes:
                max_votes = votes_count[person]
                top_voted = person
                top_voted_records.append(person)
            else:
                top_voted_records.append(top_voted)

        return top_voted_records

    def q(self, t: int) -> int:
        # Find the first T such that T > t
        idx = bisect.bisect_right(self.times, t)

        # Return the top-voted candidate right before T
        return self.top_voted_records[idx - 1]


"""
Complexity:

1. Time complexity:
- __init__: O(n) to build top_voted_records
- q: O(log(n)) for bisect right

2. Space Complexity: O(n) for top_voted_records
(O(n) for votes_count dictionary, only when building top_voted_records)
"""
