# Python Daily Usage Cheat Sheet

This document compiles essential Python code blocks, methods, and built-in syntax blocks frequently used in daily software development.

---

## 📋 Table of Contents
1.  [Core Collections & List Manipulation](#1-core-collections--list-manipulation)
2.  [Dictionary Operations](#2-dictionary-operations)
3.  [String Formatting & Operations](#3-string-formatting--operations)
4.  [File I/O & File Operations](#4-file-io--file-operations)
5.  [Exception Handling Patterns](#5-exception-handling-patterns)
6.  [Iterators, Zip & Enumerate](#6-iterators-zip--enumerate)
7.  [Date, Time & Timing Execution](#7-date-time--timing-execution)
8.  [Environment & Virtualenv Setup](#8-environment--virtualenv-setup)

---

## 1. Core Collections & List Manipulation

### Slicing & Reversing
Extract portions of a list or reverse it:
```python
items = [10, 20, 30, 40, 50]

# Get first three items: [10, 20, 30]
first_three = items[:3]

# Get last two items: [40, 50]
last_two = items[-2:]

# Reverse the list: [50, 40, 30, 20, 10]
reversed_items = items[::-1]
```

### List Comprehensions
Create lists concisely with inline loops and filters:
```python
# Simple mapping: [0, 1, 4, 9, 16]
squares = [x**2 for x in range(5)]

# Mapping with conditional filter: [0, 4, 16]
even_squares = [x**2 for x in range(5) if x % 2 == 0]
```

### Removing Duplicates
Convert to a set and back to remove duplicates while losing order:
```python
duplicates = [1, 2, 2, 3, 3, 3]
unique_items = list(set(duplicates))  # [1, 2, 3]
```

---

## 2. Dictionary Operations

### Safe Access with Defaults
Avoid `KeyError` crashes:
```python
user = {"name": "Alice", "role": "admin"}

# Returns 'admin'
role = user.get("role", "guest")

# Returns 'guest' (default fallback value)
status = user.get("status", "guest")
```

### Merging Dictionaries (Python 3.9+)
Use the merge union operator `|`:
```python
defaults = {"theme": "light", "notifications": True}
user_settings = {"theme": "dark"}

# Merged: {'theme': 'dark', 'notifications': True}
settings = defaults | user_settings
```

### Dictionary Comprehensions
Build mappings efficiently:
```python
# Key-to-Square mapping: {1: 1, 2: 4, 3: 9}
square_map = {x: x**2 for x in range(1, 4)}
```

### Default Dictionaries
Set defaults automatically for missing keys:
```python
from collections import defaultdict

# Missing keys automatically default to an empty list
user_groups = defaultdict(list)
user_groups["admins"].append("Alice")
```

---

## 3. String Formatting & Operations

### F-Strings (Python 3.6+)
Embed variables directly in strings:
```python
name = "Alice"
age = 30
# Output: "Alice is 30 years old."
message = f"{name} is {age} years old."
```

### Joining list of strings
Fastest way to concatenate strings:
```python
words = ["Python", "is", "awesome"]
sentence = " ".join(words)  # "Python is awesome"
```

### Stripping & Cleaning Strings
Remove whitespace, carriage returns, or specific characters:
```python
raw_input = "  data value \n"
clean_input = raw_input.strip()  # "data value"
```

---

## 4. File I/O & File Operations

### Context Managers (`with`)
Guarantees file descriptors are closed safely, even if an exception occurs:
```python
# Reading a file
with open("app.log", "r") as file:
    content = file.read()

# Writing a file
with open("output.txt", "w") as file:
    file.write("Completed task execution.\n")
```

---

## 5. Exception Handling Patterns

### Clean Catching & Error Logging
```python
try:
    value = 10 / 0
except ZeroDivisionError as error:
    print(f"Error division: {error}")
else:
    print("Execution completed without errors.")
finally:
    print("Always executed cleanup steps.")
```

---

## 6. Iterators, Zip & Enumerate

### Enumerate
Access both the index count and target value in a loop:
```python
tasks = ["plan", "code", "test"]
for index, task in enumerate(tasks):
    print(f"Task {index}: {task}")
```

### Zip
Iterate over multiple sequences concurrently:
```python
keys = ["name", "age"]
values = ["Alice", 30]

# Dict: {'name': 'Alice', 'age': 30}
user_profile = dict(zip(keys, values))
```

---

## 7. Date, Time & Timing Execution

### Getting Current Datetime
```python
from datetime import datetime, timezone

# Get timezone-aware UTC timestamp
now = datetime.now(timezone.utc)
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S %Z")
```

### Measuring Code Execution Duration
```python
import time

start_time = time.perf_counter()

# Run target process
time.sleep(0.5)

end_time = time.perf_counter()
duration = end_time - start_time
print(f"Completed in {duration:.4f} seconds.")
```

---

## 8. Environment & Virtualenv Setup

### Create and Activate venv
```bash
# 1. Create a virtual environment named 'venv'
python3 -m venv venv

# 2. Activate the virtual environment
source venv/bin/activate

# 3. Deactivate when finished
deactivate
```

### Package Management with Pip
```bash
# Install dependencies listed in a file
pip install -r requirements.txt

# Save currently installed packages
pip freeze > requirements.txt
```
