# Python 250 Interview Questions & Answers - Part 1 (Q1 - Q90)

This document is Part 1 of the comprehensive Python interview questions series, covering Python foundations, core data types, scoping rules, and basic syntax structures.

---

## 📋 Table of Contents
*   [Language Foundations & Syntax (Q1 - Q30)](#language-foundations--syntax-q1---q30)
*   [Core Data Structures (Q31 - Q60)](#core-data-structures-q31---q60)
*   [Functions & Scoping (Q61 - Q90)](#functions--scoping-q61---q90)

---

## Language Foundations & Syntax (Q1 - Q30)

#### Q1: What is Python?
**Answer:** An interpreted, high-level, general-purpose programming language that supports multiple programming paradigms, including structured, object-oriented, and functional programming.

#### Q2: What does it mean that Python is a "dynamically typed" language?
**Answer:** You don't need to state variable types explicitly when writing code. Type checking is performed at runtime rather than compile-time.

#### Q3: Is Python compiled or interpreted?
**Answer:** It is both. Python code is first compiled into intermediate bytecode (`.pyc` files) and then interpreted by the Python Virtual Machine (PVM).

#### Q4: What is PEP 8?
**Answer:** Python Enhancement Proposal 8. It is the official style guide for writing clean, consistent, and readable Python code.

#### Q5: Explain the difference between Python 2 and Python 3.
**Answer:** Python 3 is the modern standard (Python 2 was deprecated in 2020). Python 3 uses Unicode by default for strings, prints with parentheses as a function rather than a statement, and handles integer division by returning floats.

#### Q6: What is the significance of indentation in Python?
**Answer:** Python uses indentation (usually 4 spaces) instead of curly braces or keywords to define block structures, nested statements, and functions.

#### Q7: What are keywords in Python?
**Answer:** Reserved words that have special syntactic meaning (e.g., `if`, `def`, `class`, `import`, `return`) and cannot be used as variable identifiers.

#### Q8: What is a Namespace in Python?
**Answer:** A naming system used to ensure that all names in a program are unique and can be resolved without conflicts. Examples include Local, Global, and Built-in namespaces.

#### Q9: How do you declare a multi-line string?
**Answer:** Using triple quotes, either triple single-quotes `'''` or triple double-quotes `"""`.

#### Q10: What is the purpose of the `pass` statement?
**Answer:** A null statement that acts as a placeholder when syntactical structure requires a block of code but no action is needed.

#### Q11: Explain the difference between `/` and `//` division operators.
**Answer:** 
*   `/`: Performs standard division, always returning a float (e.g., `5 / 2 = 2.5`).
*   `//`: Performs floor division, rounding down to the nearest integer (e.g., `5 // 2 = 2`).

#### Q12: What does the `**` operator do?
**Answer:** Power/exponentiation operator (e.g., `2 ** 3 = 8`).

#### Q13: Explain the difference between `is` and `==` operators.
**Answer:** 
*   `==`: Checks if the values of two objects are equal (value equality).
*   `is`: Checks if two variables point to the exact same object in memory (identity equality).

#### Q14: What is the ternary operator equivalent in Python?
**Answer:** The conditional expression: `x if condition else y`.

#### Q15: Explain the difference between mutable and immutable objects.
**Answer:** 
*   **Mutable**: The object's state or contents can be modified after creation (e.g., lists, dictionaries, sets).
*   **Immutable**: The object's state cannot be changed after creation (e.g., strings, numbers, tuples).

#### Q16: What is a Docstring?
**Answer:** A string literal written as the first statement in a class, function, or module, used to document code interfaces. It is accessed via `__doc__`.

#### Q17: What does the `len()` function do?
**Answer:** Returns the number of items (length) of an object (e.g., list, string, tuple).

#### Q18: What is the difference between `range()` and `xrange()`?
**Answer:** `xrange()` was used in Python 2 to generate numbers lazily using a generator. In Python 3, `range()` behaves like `xrange()`, and the original `xrange()` was removed.

#### Q19: Explain the `in` operator.
**Answer:** A membership test operator that returns `True` if a value is found in a sequence (like lists, strings, tuples, or dict keys).

#### Q20: What are comments in Python?
**Answer:** Notes in the code ignored by the interpreter, started with the `#` symbol.

#### Q21: What is the difference between static and dynamic typing?
**Answer:** Static typing checks variable types during compilation, while dynamic typing checks types dynamically at runtime.

#### Q22: What are literals?
**Answer:** Raw data values assigned to variables directly in code (e.g., `"Hello"`, `42`, `3.14`, `True`).

#### Q23: Explain the `break` statement in loops.
**Answer:** Immediately terminates the loop block, resuming execution at the next statement after the loop.

#### Q24: Explain the `continue` statement in loops.
**Answer:** Skips the rest of the code in the current iteration of the loop and jumps directly to the next iteration.

#### Q25: Explain the loop `else` clause in Python.
**Answer:** A block of code that executes when a loop terminates normally (i.e., without encountering a `break` statement).

#### Q26: What is the type of `None` in Python?
**Answer:** `NoneType`. It represents the absence of a value or a null value.

#### Q27: How do you check the type of an object?
**Answer:** Using the built-in `type()` function (e.g., `type(10)` returns `<class 'int'>`) or `isinstance()`.

#### Q28: Why is `isinstance()` preferred over `type()` for type checking?
**Answer:** `isinstance()` accounts for inheritance, returning `True` if the object is an instance of a subclass, whereas `type()` checks exact class matching.

#### Q29: What is the boolean value of empty collections?
**Answer:** Falsy. Empty lists `[]`, dictionaries `{}`, sets `set()`, tuples `()`, empty strings `""`, and numbers equal to `0` evaluate to `False` in boolean contexts.

#### Q30: Explain type casting.
**Answer:** Converting a variable from one data type to another using constructor functions like `int()`, `str()`, `float()`, or `list()`.

---

## Core Data Structures (Q31 - Q60)

#### Q31: What is a list?
**Answer:** An ordered, mutable sequence of elements, declared using square brackets: `my_list = [1, "two", 3.0]`.

#### Q32: What is a tuple?
**Answer:** An ordered, immutable sequence of elements, declared using parentheses: `my_tuple = (1, "two", 3.0)`.

#### Q33: Why would you use a tuple instead of a list?
**Answer:** 
*   Tuples are immutable, making them safer for read-only data.
*   Tuples are hashable (can be used as dictionary keys), whereas lists are not.
*   Tuples are slightly faster and consume less memory.

#### Q34: What is a dictionary?
**Answer:** An unordered (ordered by insertion since Python 3.7), mutable mapping of unique keys to values, declared using curly braces: `my_dict = {"name": "Alice", "age": 30}`.

#### Q35: What is a set?
**Answer:** An unordered collection of unique, mutable, hashable elements, declared using curly braces or the constructor: `my_set = {1, 2, 3}` or `set()`.

#### Q36: What is the difference between `list.append()` and `list.extend()`?
**Answer:** 
*   `append()`: Adds its argument as a single element to the end of the list.
*   `extend()`: Iterates over its argument and adds each element to the list, expanding it.

#### Q37: What is the difference between `list.remove()` and `list.pop()`?
**Answer:** 
*   `remove()`: Deletes the first occurrence of a specific value from the list, returning `None`.
*   `pop()`: Removes and returns the element at a given index (defaults to the last item).

#### Q38: How do you sort a list in-place, and how is it different from `sorted()`?
**Answer:** 
*   `list.sort()`: Sorts the list in-place, modifying the original list.
*   `sorted(list)`: Returns a new sorted list, leaving the original list unchanged.

#### Q39: What is list slicing?
**Answer:** A syntax to extract a sub-segment of a list: `list[start:stop:step]`.

#### Q40: What does `my_list[::-1]` do?
**Answer:** Returns a reversed copy of the list.

#### Q41: How do you copy a list to prevent modifying the original?
**Answer:** Using the slice copy `new_list = old_list[:]`, the `list.copy()` method, or by importing the `copy` module (`copy.copy(list)`).

#### Q42: What is the difference between a shallow copy and a deep copy?
**Answer:** 
*   **Shallow Copy**: Creates a new object container but copies references to the nested objects. Modifying nested lists affects both copies.
*   **Deep Copy**: Recursively copies all nested objects, creating completely independent data spaces.

#### Q43: How do you check if a key exists in a dictionary?
**Answer:** Using the `in` operator: `if "key" in my_dict:`.

#### Q44: What is the difference between `dict["key"]` and `dict.get("key")`?
**Answer:** 
*   `dict["key"]`: Raises a `KeyError` if the key does not exist.
*   `dict.get("key")`: Returns `None` (or a default fallback value) if the key is missing.

#### Q45: Explain the `update()` method in dictionaries.
**Answer:** Merges key-value pairs from another dictionary or iterable of key-values into the target dictionary, overwriting duplicate keys.

#### Q46: How do you extract keys and values from a dictionary?
**Answer:** Using `dict.keys()`, `dict.values()`, and `dict.items()`.

#### Q47: What are dictionary views?
**Answer:** Objects returned by `keys()`, `values()`, and `items()` that provide a dynamic view of the dictionary's keys and values, updating automatically when the dictionary changes.

#### Q48: How do you create an empty set?
**Answer:** You must use `set()`. Using empty curly braces `{}` creates an empty dictionary.

#### Q49: What is the difference between `set.discard()` and `set.remove()`?
**Answer:** 
*   `remove()`: Raises a `KeyError` if the element is not found.
*   `discard()`: Removes the element if present, doing nothing if it is missing.

#### Q50: Explain set operations.
**Answer:** 
*   `union` (`|`): Combines elements from both sets.
*   `intersection` (`&`): Isolates common elements.
*   `difference` (`-`): Isolates elements unique to the first set.

#### Q51: What is a frozenset?
**Answer:** An immutable version of a set, which is hashable and can be used as a dictionary key or as an element in another set.

#### Q52: What is the time complexity of searching in a list vs. a dictionary?
**Answer:** 
*   List search: $O(N)$ linear time.
*   Dictionary search: $O(1)$ constant time on average (using hash lookups).

#### Q53: How do you handle duplicate elements in a list?
**Answer:** Convert it to a set: `list(set(my_list))`, which removes duplicates.

#### Q54: What does the `zip()` function do?
**Answer:** Combines elements from multiple iterables into tuples based on index matching: `zip([1, 2], ['a', 'b'])` yields `(1, 'a'), (2, 'b')`.

#### Q55: What does the `enumerate()` function do?
**Answer:** Takes a collection and returns an enumerate object yielding tuples containing index counts and values: `(0, value_0), (1, value_1)`.

#### Q56: How do you verify if all elements in an iterable are truthy?
**Answer:** Using the `all()` function.

#### Q57: How do you verify if at least one element in an iterable is truthy?
**Answer:** Using the `any()` function.

#### Q58: Explain the `collections.defaultdict` class.
**Answer:** A dictionary subclass that calls a factory function (like `int`, `list`) to provide a default value when a referenced key is missing.

#### Q59: Explain the `collections.Counter` class.
**Answer:** A dictionary subclass designed to count hashable objects, returning key-occurrence count mappings.

#### Q60: Explain `collections.deque`.
**Answer:** A double-ended queue that supports thread-safe, memory-efficient appends and pops from both sides in $O(1)$ time.

---

## Functions & Scoping (Q61 - Q90)

#### Q61: How do you define a function in Python?
**Answer:**
```python
def my_function(param1, param2):
    return param1 + param2
```

#### Q62: What is the difference between a parameter and an argument?
**Answer:** 
*   **Parameter**: The variable listed in the function definition.
*   **Argument**: The actual value sent to the function when it is called.

#### Q63: What does the `return` statement do?
**Answer:** Exits a function, returning control to the caller and optionally passing back a value or object. If omitted, the function returns `None` by default.

#### Q64: What is the difference between positional and keyword arguments?
**Answer:** 
*   **Positional**: Matched based on the order they are passed.
*   **Keyword**: Passed using the format `name=value`, allowing arguments to be passed in any order.

#### Q65: What are default arguments?
**Answer:** Arguments that assume default values specified in the function definition if omitted during the function call.

#### Q66: Why should you avoid using mutable default arguments (e.g., `def append_to(element, target=[])`)?
**Answer:** Default arguments are evaluated only once when the function is defined. If you modify a mutable default argument (like a list), that modification persists across subsequent calls. Use `target=None` instead.

#### Q67: Explain `*args`.
**Answer:** A syntax parameter that packs positional arguments passed to a function into a single tuple, allowing the function to accept a variable number of positional inputs.

#### Q68: Explain `**kwargs`.
**Answer:** A syntax parameter that packs keyword arguments passed to a function into a single dictionary, allowing the function to accept a variable number of keyword inputs.

#### Q69: What is the correct order of parameters in a function definition?
**Answer:** Standard positional parameters first, followed by `*args`, default parameters, keyword-only parameters, and finally `**kwargs`.

#### Q70: What are keyword-only arguments?
**Answer:** Parameters listed after `*args` or a bare `*` in a function definition, which must be passed as keyword arguments.

#### Q71: Explain variable scope in Python.
**Answer:** The region of a program where a variable is recognized. Scope rules follow the **LEGB** rule: Local, Enclosing, Global, Built-in.

#### Q72: Explain the `global` keyword.
**Answer:** Used inside a function to declare that a variable belongs to the global (module-level) scope, allowing you to modify it locally.

#### Q73: Explain the `nonlocal` keyword.
**Answer:** Used inside nested functions to modify variables declared in the outer enclosing scope (excluding global scope).

#### Q74: What is a lambda function?
**Answer:** An anonymous, single-expression function declared using the `lambda` keyword: `add = lambda x, y: x + y`.

#### Q75: How are parameters passed in Python (Pass-by-value or Pass-by-reference)?
**Answer:** **Pass-by-assignment** (also called object reference). If you pass a mutable object, changes inside the function affect the caller. If you pass an immutable object, changes do not affect the caller.

#### Q76: What is recursion?
**Answer:** A programming technique where a function calls itself to solve smaller instances of the same problem, requiring a base case to terminate.

#### Q77: What is the default recursion depth limit in Python, and how do you change it?
**Answer:** Typically 1000. It can be checked and changed using the `sys` module: `sys.getrecursionlimit()` and `sys.setrecursionlimit(limit)`.

#### Q78: Explain the `map()` function.
**Answer:** Applies a function to all items in an input iterable and returns an iterator: `map(str, [1, 2])` yields `'1', '2'`.

#### Q79: Explain the `filter()` function.
**Answer:** Construct an iterator from elements of an iterable for which a function returns true: `filter(lambda x: x > 0, [-1, 2])` yields `2`.

#### Q80: Explain the `reduce()` function.
**Answer:** Part of the `functools` module. Applies a function of two arguments cumulatively to the items of an iterable, reducing the sequence to a single value.

#### Q81: What is a closure?
**Answer:** A nested function object that retains access to variables from its enclosing scope even after the outer function has finished executing.

#### Q82: What is the `__code__` attribute of a function?
**Answer:** An attribute containing the compiled bytecode and compilation metadata of the function object.

#### Q83: Explain the difference between `dir()` and `globals()`.
**Answer:** 
*   `globals()`: Returns a dictionary of all global variables in the current module.
*   `dir()`: Returns a list of valid attributes for the passed object, or active local variables if no argument is passed.

#### Q84: What does the `locals()` function return?
**Answer:** A dictionary representing the current local namespace table.

#### Q85: How do you declare type hints in functions?
**Answer:**
```python
def greeting(name: str) -> str:
    return f"Hello, {name}"
```

#### Q86: Are Python type hints enforced at runtime?
**Answer:** No. They are ignored by the interpreter and are used by static checkers (e.g., `mypy`) or IDEs to check code type safety.

#### Q87: What is the purpose of the `callable()` function?
**Answer:** Returns `True` if the passed object appears callable (like functions, classes, or objects implementing `__call__`), and `False` otherwise.

#### Q88: How do you access a function's name string programmatically?
**Answer:** Using the `__name__` attribute.

#### Q89: What does the `help()` function do?
**Answer:** Invokes the built-in system help utility, parsing docstrings to display module and function usage details.

#### Q90: Explain the `functools.partial` helper.
**Answer:** Returns a new partial object which behaves like the original function called with pre-filled positional and keyword arguments.
