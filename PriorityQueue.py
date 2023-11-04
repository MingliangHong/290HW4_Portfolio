
import heapq

class PriorityQueue:
    def __init__(self):
        # Initialize the priority queue (heap)
        self.pq = []
        # Dictionary to map node names to their keys/priorities
        self.keys = {}
        
    def is_empty(self):
        return len(self.pq) == 0

    def extract_min(self):
        if self.is_empty():
            raise ValueError("Heap is empty!")
        _, min_name = heapq.heappop(self.pq)
        del self.keys[min_name]
        return min_name
    
    def insert(self, name, key):
        # If the name already exists in the priority queue, remove it first
        if name in self.keys:
            self.delete(name)
        # Add the new (key, name) pair to the priority queue
        heapq.heappush(self.pq, (key, name))
        self.keys[name] = key
        
    def decrease_key(self, name, key):
        # If the name already exists in the priority queue, remove it first
        if name in self.keys:
            self.delete(name)
        # Add the new (key, name) pair to the priority queue
        heapq.heappush(self.pq, (key, name))
        self.keys[name] = key
        
    def delete(self, name):
        # Set the key of the name to a very large negative number to ensure it's the minimum
        self.keys[name] = float('-inf')
        # Extract the minimum (which will be the name we're trying to delete)
        self.extract_min()
        
    def contains(self, name):
        return name in self.keys
