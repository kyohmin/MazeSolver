import random

class Room:
    def __init__(self, r, c):
        self.r, self.c = r, c
        self.visit = 0
        self.prev = None
        self.drct = [(r+1, c), (r,c+1), (r-1,c), (r, c-1)]
        random.shuffle(self.drct)