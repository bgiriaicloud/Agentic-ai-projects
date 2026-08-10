# Python 100 Interview Programs - Part 2 (Programs 51 - 100)

This document is Part 2 of the essential interview preparation programs in Python, providing code templates for advanced data structures, searching/sorting algorithms, and programming patterns.

---

## 📋 Table of Contents
*   [Data Structures & OOP Implementations (Programs 51 - 70)](#data-structures--oop-implementations-programs-51---70)
*   [Searching & Sorting Algorithms (Programs 71 - 85)](#searching--sorting-algorithms-programs-71---85)
*   [Advanced Utilities & Algorithms (Programs 86 - 100)](#advanced-utilities--algorithms-programs-86---100)

---

## Data Structures & OOP Implementations (Programs 51 - 70)

### 51. Custom Stack Class (LIFO)
```python
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop() if not self.is_empty() else None
    def is_empty(self):
        return len(self.items) == 0
    def peek(self):
        return self.items[-1] if not self.is_empty() else None

s = Stack()
s.push(10)
s.push(20)
print(s.pop())  # 20
```

### 52. Custom Queue Class (FIFO)
```python
class Queue:
    def __init__(self):
        self.items = []
    def enqueue(self, item):
        self.items.append(item)
    def dequeue(self):
        return self.items.pop(0) if not self.is_empty() else None
    def is_empty(self):
        return len(self.items) == 0

q = Queue()
q.enqueue(10)
q.enqueue(20)
print(q.dequeue())  # 10
```

### 53. Node Class for a Singly Linked List
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

### 54. Singly Linked List Implementation with Append & Display
```python
class LinkedList:
    def __init__(self):
        self.head = None
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node
    def display(self):
        elems = []
        cur = self.head
        while cur:
            elems.append(str(cur.data))
            cur = cur.next
        return " -> ".join(elems)

ll = LinkedList()
ll.append(1)
ll.append(2)
print(ll.display())  # "1 -> 2"
```

### 55. Reverse a Singly Linked List
```python
def reverse_linked_list(ll):
    prev = None
    current = ll.head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    ll.head = prev
    return ll
```

### 56. Detect a Cycle in a Linked List (Floyd's Cycle-Finding Algorithm)
```python
def has_cycle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False
```

### 57. Find the Middle Node of a Linked List
```python
def find_middle(head):
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow.data if slow else None
```

### 58. Custom Binary Search Tree (BST) Node and Insert
```python
class BSTNode:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key

def insert_bst(root, key):
    if root is None:
        return BSTNode(key)
    if key < root.val:
        root.left = insert_bst(root.left, key)
    else:
        root.right = insert_bst(root.right, key)
    return root
```

### 59. In-Order Traversal of a Binary Tree (LVR)
```python
def inorder(root):
    res = []
    if root:
        res.extend(inorder(root.left))
        res.append(root.val)
        res.extend(inorder(root.right))
    return res
```

### 60. Pre-Order Traversal of a Binary Tree (VLR)
```python
def preorder(root):
    res = []
    if root:
        res.append(root.val)
        res.extend(preorder(root.left))
        res.extend(preorder(root.right))
    return res
```

### 61. Post-Order Traversal of a Binary Tree (LRV)
```python
def postorder(root):
    res = []
    if root:
        res.extend(postorder(root.left))
        res.extend(postorder(root.right))
        res.append(root.val)
    return res
```

### 62. Find the Maximum Depth (Height) of a Binary Tree
```python
def max_depth(root):
    if root is None:
        return 0
    return max(max_depth(root.left), max_depth(root.right)) + 1
```

### 63. Check if Two Binary Trees are Identical
```python
def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return p.val == q.val and is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
```

### 64. Custom Graph Class with Adjacency List
```python
class Graph:
    def __init__(self):
        self.adj = {}
    def add_edge(self, u, v):
        self.adj.setdefault(u, []).append(v)
        self.adj.setdefault(v, []).append(u)
```

### 65. Breadth-First Search (BFS) in a Graph
```python
def bfs(graph, start):
    visited = set([start])
    queue = [start]
    res = []
    while queue:
        vertex = queue.pop(0)
        res.append(vertex)
        for neighbor in graph.adj.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return res
```

### 66. Depth-First Search (DFS) in a Graph
```python
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()
    visited.add(start)
    res = [start]
    for neighbor in graph.adj.get(start, []):
        if neighbor not in visited:
            res.extend(dfs(graph, neighbor, visited))
    return res
```

### 67. Simple Custom Exception Class
```python
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        super().__init__(f"Attempted to withdraw ${amount} with balance of ${balance}")
        self.balance = balance
        self.amount = amount
```

### 68. Singleton Pattern Implementation using Metaclass
```python
class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    pass
```

### 69. Factory Design Pattern Example
```python
class Dog:
    def speak(self): return "Woof"
class Cat:
    def speak(self): return "Meow"

class PetFactory:
    @staticmethod
    def get_pet(pet_type):
        pets = {"dog": Dog, "cat": Cat}
        return pets.get(pet_type.lower(), Dog)()

pet = PetFactory.get_pet("cat")
print(pet.speak())  # "Meow"
```

### 70. Custom Iterator Class yielding Even Numbers
```python
class Evens:
    def __init__(self, limit):
        self.limit = limit
        self.val = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self.val >= self.limit:
            raise StopIteration
        result = self.val
        self.val += 2
        return result

print(list(Evens(6)))  # [0, 2, 4]
```

---

## Searching & Sorting Algorithms (Programs 71 - 85)

### 71. Linear Search
```python
def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1

print(linear_search([10, 20, 30], 20))  # 1
```

### 72. Binary Search (Iterative)
```python
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

print(binary_search([10, 20, 30, 40], 30))  # 2
```

### 73. Binary Search (Recursive)
```python
def binary_search_rec(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_rec(arr, target, mid + 1, high)
    else:
        return binary_search_rec(arr, target, low, mid - 1)
```

### 74. Bubble Sort
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

print(bubble_sort([64, 34, 25, 12]))  # [12, 25, 34, 64]
```

### 75. Selection Sort
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

print(selection_sort([64, 25, 12, 22]))  # [12, 22, 25, 64]
```

### 76. Insertion Sort
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

print(insertion_sort([12, 11, 13, 5]))  # [5, 11, 12, 13]
```

### 77. Merge Sort
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    # Merge step
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i]); i += 1
        else:
            res.append(right[j]); j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

print(merge_sort([38, 27, 43, 3]))  # [3, 27, 38, 43]
```

### 78. Quick Sort (Divide and Conquer)
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print(quick_sort([10, 7, 8, 9, 1]))  # [1, 7, 8, 9, 10]
```

### 79. Heap Sort
```python
def heapify(arr, n, i):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[i] < arr[left]:
        largest = left
    if right < n and arr[largest] < arr[right]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr
```

### 80. Shell Sort
```python
def shell_sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr
```

### 81. Counting Sort (For positive integer ranges)
```python
def counting_sort(arr):
    if not arr: return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for x in arr:
        count[x] += 1
    res = []
    for i, occurrences in enumerate(count):
        res.extend([i] * occurrences)
    return res
```

### 82. Radix Sort
```python
def counting_sort_for_radix(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
    for i in range(n):
        arr[i] = output[i]

def radix_sort(arr):
    if not arr: return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_for_radix(arr, exp)
        exp *= 10
    return arr
```

### 83. Bucket Sort
```python
def bucket_sort(arr):
    if not arr: return arr
    bucket_count = len(arr)
    max_val, min_val = max(arr), min(arr)
    val_range = (max_val - min_val) / bucket_count
    
    buckets = [[] for _ in range(bucket_count)]
    for x in arr:
        diff = (x - min_val) / val_range
        idx = int(diff)
        if idx == bucket_count:
            idx -= 1
        buckets[idx].append(x)
    
    for bucket in buckets:
        bucket.sort()
    
    res = []
    for bucket in buckets:
        res.extend(bucket)
    return res
```

### 84. Two-Sum Problem (Find indices of two numbers that add up to target)
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

### 85. Check if a String has Valid Matching Parentheses
```python
def is_valid_parentheses(s):
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top_elem = stack.pop() if stack else '#'
            if mapping[char] != top_elem:
                return False
        else:
            stack.append(char)
    return len(stack) == 0

print(is_valid_parentheses("({[]})"))  # True
print(is_valid_parentheses("({[})"))   # False
```

---

## Advanced Utilities & Algorithms (Programs 86 - 100)

### 86. Custom Timing Decorator
```python
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        res = func(*args, **kwargs)
        t2 = time.perf_counter()
        print(f"Elapsed: {t2 - t1:.5f}s")
        return res
    return wrapper
```

### 87. Generate All Permutations of a List (Recursion)
```python
def get_permutations(arr):
    if len(arr) <= 1:
        return [arr]
    res = []
    for i in range(len(arr)):
        current = arr[i]
        remaining = arr[:i] + arr[i+1:]
        for p in get_permutations(remaining):
            res.append([current] + p)
    return res

print(get_permutations([1, 2]))  # [[1, 2], [2, 1]]
```

### 88. Generate All Subsets (Power Set) of a List
```python
def get_subsets(arr):
    subsets = [[]]
    for element in arr:
        subsets += [current + [element] for current in subsets]
    return subsets

print(get_subsets([1, 2]))  # [[], [1], [2], [1, 2]]
```

### 89. Rotate a 2D Matrix by 90 Degrees Clockwise In-Place
```python
def rotate_matrix(matrix):
    n = len(matrix)
    # Transpose matrix
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    # Reverse rows
    for i in range(n):
        matrix[i].reverse()
    return matrix

print(rotate_matrix([[1, 2], [3, 4]]))  # [[3, 1], [4, 2]]
```

### 90. Find the Longest Common Subsequence (LCS) Length (DP)
```python
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

print(lcs("abcde", "ace"))  # 3 ("ace")
```

### 91. 0/1 Knapsack Problem (Dynamic Programming)
```python
def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]
```

### 92. Merge Overlapping Intervals
```python
def merge_intervals(intervals):
    if not intervals: return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
    return merged

print(merge_intervals([[1, 3], [2, 6], [8, 10]]))  # [[1, 6], [8, 10]]
```

### 93. Implement LRU Cache (Least Recently Used) using OrderedDict
```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

### 94. Simple Thread Worker Example
```python
import threading

def worker(num):
    print(f"Worker {num} starting")

threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()
```

### 95. Async Coroutine Producer-Consumer
```python
import asyncio

async def produce(queue):
    for i in range(3):
        await queue.put(i)
        await asyncio.sleep(0.1)

async def consume(queue):
    while not queue.empty():
        item = await queue.get()
        print(f"Consumed {item}")
```

### 96. Safe File Line Reader with Custom Iterator
```python
class LineReader:
    def __init__(self, filepath):
        self.filepath = filepath
    def __iter__(self):
        self.file = open(self.filepath, 'r')
        return self
    def __next__(self):
        line = self.file.readline()
        if not line:
            self.file.close()
            raise StopIteration
        return line.strip()
```

### 97. Find the Longest Palindromic Substring Length (Expand Around Center)
```python
def longest_palindrome_substr(s):
    if not s: return 0
    start, end = 0, 0
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    for i in range(len(s)):
        len1 = expand(i, i)
        len2 = expand(i, i + 1)
        max_len = max(len1, len2)
        if max_len > (end - start):
            start = i - (max_len - 1) // 2
            end = i + max_len // 2
    return end - start + 1
```

### 98. Check if a String is a Valid IPv4 Address
```python
def is_valid_ipv4(ip):
    parts = ip.split(".")
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit():
            return False
        num = int(part)
        if num < 0 or num > 255:
            return False
        if len(part) > 1 and part[0] == "0":
            return False
    return True

print(is_valid_ipv4("192.168.1.1"))  # True
print(is_valid_ipv4("256.0.0.1"))    # False
```

### 99. Flatten a Deeply Nested List (Recursive)
```python
def flatten_deep(arr):
    res = []
    for item in arr:
        if isinstance(item, list):
            res.extend(flatten_deep(item))
        else:
            res.append(item)
    return res

print(flatten_deep([1, [2, [3, 4]]]))  # [1, 2, 3, 4]
```

### 100. Read environment configurations safely using os.getenv
```python
import os

def get_db_url():
    # Returns default if environment variable is missing
    return os.getenv("DATABASE_URL", "sqlite:///default.db")

print(get_db_url())
```
