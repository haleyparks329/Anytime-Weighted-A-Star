# OpenList.py
# Definitions for PriorityQueue and Stack to be used in search.py
import heapq
import itertools

'''
This file contains implementations for a binary heap-based PriorityQueue as well as a Stack.
The PriorityQueue implementation allows you to update the priority of a state that is already
in the Queue, keeping whichever entry has a lower accumulated cost.  Adding a state is still
acheived in constant time.
'''


# Implementation from https://docs.python.org/3.6/library/heapq.html#priority-queue-implementation-notes
class PriorityQueue:
    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of states to entries
        self.REMOVED = '<removed-state>'  # placeholder for a removed state
        self.counter = itertools.count(0, -1)  # unique sequence count

    def add_state(self, state):  # Add a new state or update the priority of an existing state
        count = next(self.counter)
        entry = [state.c + state.wh, state.wh, count, state]
        try:
            if self.entry_finder[state][-1].c <= state.c:
                return
            self.remove_state(state)
        except KeyError:
            pass
        self.entry_finder[state] = entry
        heapq.heappush(self.pq, entry)

    # Mark an existing state as REMOVED.  Raise KeyError if not found.
    def remove_state(self, state):
        entry = self.entry_finder.pop(state)
        entry[-1] = self.REMOVED

    # Remove and return the lowest priority state. Raise KeyError if empty.
    def pop_state(self):
        while self.pq:
            f, h, count, state = heapq.heappop(self.pq)
            if state is not self.REMOVED:
                del self.entry_finder[state]
                return state
        raise KeyError('pop from an empty priority queue')

    def __len__(self):
        return len(self.entry_finder)


class Stack:
    def __init__(self):
        self.stack = []  # list of entries arranged in a heap

    def add_state(self, state):  # Add a new state
        self.stack.append(state)

    def pop_state(self):  # Pop last added state. Raise KeyError if empty.
        while self.stack:
            return self.stack.pop(-1)
        raise KeyError('pop from an empty priority queue')

    def __len__(self):
        return len(self.stack)
