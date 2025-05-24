from collections import deque

class SlidingWindow:
    def __init__(self, size):
        self.size = size
        self.window = deque()
        self.unique_numbers = set()

    def add_numbers(self, numbers):
        prev_state = list(self.window)

        for num in numbers:
            if num in self.unique_numbers:
                continue
            if len(self.window) >= self.size:
                removed = self.window.popleft()
                self.unique_numbers.remove(removed)
            self.window.append(num)
            self.unique_numbers.add(num)

        return prev_state, list(self.window)

    def get_average(self):
        if not self.window:
            return 0.0
        return round(sum(self.window) / len(self.window), 2)
