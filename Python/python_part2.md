# Python 250 Interview Questions & Answers - Part 2 (Q91 - Q170)

This document is Part 2 of the comprehensive Python interview questions series, covering Object-Oriented Programming (OOP), File I/O, Exception Handling, Comprehensions, Iterators/Generators, and Decorators.

---

## 📋 Table of Contents
*   [Object-Oriented Programming (Q91 - Q120)](#object-oriented-programming-q91---q120)
*   [Exceptions & File I/O (Q121 - Q140)](#exceptions--file-io-q121---q140)
*   [Comprehensions, Iterators & Generators (Q141 - Q170)](#comprehensions-iterators--generators-q141---q170)

---

## Object-Oriented Programming (Q91 - Q120)

#### Q91: What is a Class in Python?
**Answer:** A user-defined prototype or blueprint from which objects are created. It encapsulates variables (attributes) and functions (methods) into a single entity.

#### Q92: What is an Object?
**Answer:** An instance of a class that has a state (attributes) and behavior (methods) defined by its class.

#### Q93: What does the `self` parameter represent in class methods?
**Answer:** It represents the specific instance of the class calling the method, allowing access to attributes and other methods of that object.

#### Q94: What is the purpose of the `__init__` method?
**Answer:** The constructor method in Python. It is called automatically when a new object instance is created, initialized with user arguments.

#### Q95: Explain the difference between Instance, Class, and Static methods.
**Answer:** 
*   **Instance Method**: Takes `self` as the first argument; accesses and modifies instance-specific state.
*   **Class Method**: Marked with `@classmethod` and takes `cls` as the first argument; accesses and modifies class-level state.
*   **Static Method**: Marked with `@staticmethod`; behaves like a regular function, not accessing `self` or `cls` state.

#### Q96: What is Inheritance?
**Answer:** A mechanism where a child class inherits attributes and methods from a parent class, promoting code reusability.

#### Q97: What is Multiple Inheritance, and how does Python resolve method lookup?
**Answer:** A feature where a class inherits from more than one parent class. Method resolution order is determined by the Method Resolution Order (MRO) algorithm (C3 linearization).

#### Q98: How do you check the Method Resolution Order (MRO) of a class?
**Answer:** Access the `__mro__` attribute or call the `.mro()` method on the class (e.g., `MyClass.mro()`).

#### Q99: What is the purpose of the `super()` function?
**Answer:** Returns a proxy object that delegates method calls to a parent or sibling class, commonly used to call a parent constructor from a subclass.

#### Q100: Explain Polymorphism.
**Answer:** The ability of different classes to respond to the same method call in their own specific way (e.g., calling `draw()` on different Shape objects).

#### Q101: Explain Encapsulation, and how Python enforces private variables.
**Answer:** Restricting access to internal object components. Python uses name mangling: prefixing a variable with two underscores (e.g., `__private_var`) changes its address externally to `_ClassName__private_var`.

#### Q102: What is a "dunder" (double underscore) or magic method?
**Answer:** Special predefined methods with double leading and trailing underscores (e.g., `__str__`, `__repr__`, `__len__`) that customize object behavior.

#### Q103: Explain the difference between `__str__` and `__repr__`.
**Answer:** 
*   `__str__` (Readable): Returns a user-friendly string representation of the object, called by `print()` and `str()`.
*   `__repr__` (Unambiguous): Returns an official, developer-friendly string representation of the object, ideally valid Python code to recreate the object, called by `repr()`.

#### Q104: What is the `__new__` method, and how is it different from `__init__`?
**Answer:** 
*   `__new__`: The creator method; it creates and returns the new object instance.
*   `__init__`: The initializer method; it configures the instance created by `__new__`.

#### Q105: What is a Descriptor in Python?
**Answer:** An object that defines the behavior of attribute access (get, set, delete methods) on other objects, implementing `__get__`, `__set__`, or `__delete__`.

#### Q106: How do you declare properties using decorators?
**Answer:** Using the `@property` decorator to create read-only getters, and matching setters:
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    @property
    def radius(self):
        return self._radius
    @radius.setter
    def radius(self, value):
        self._radius = value
```

#### Q107: What is the purpose of `__slots__`?
**Answer:** Optimization that restricts the set of attributes an object instance can have, bypassing the dynamic `__dict__` dictionary to save memory.

#### Q108: What does the `@classmethod` decorator do?
**Answer:** Binds a method to the class namespace, passing the class object (`cls`) rather than the instance object (`self`) as the first argument.

#### Q109: What is Abstract Base Class (ABC)?
**Answer:** A class from the `abc` module that cannot be instantiated directly, used to define interface blueprints requiring child subclasses to implement abstract methods.

#### Q110: How do you declare an abstract method?
**Answer:** Using the `@abstractmethod` decorator from the `abc` module.

#### Q111: What is "Duck Typing"?
**Answer:** A programming style where an object's suitability is determined by the presence of certain methods and properties, rather than its inheritance (i.e., "If it walks like a duck and quacks like a duck, it is a duck").

#### Q112: Explain the `__call__` magic method.
**Answer:** Allows an instance of a class to be called like a function: `object()`.

#### Q113: Explain the `__getitem__` and `__setitem__` methods.
**Answer:** Magic methods that enable index or key lookup syntax on custom objects: `object[key]`.

#### Q114: What is a metaclass?
**Answer:** The class of a class, defining how classes themselves are constructed. By default, Python classes are instances of the `type` metaclass.

#### Q115: How do you define a custom metaclass?
**Answer:** By inheriting from `type` and overriding `__new__` or `__init__` methods:
```python
class Meta(type):
    def __new__(cls, name, bases, dct):
        return super().__new__(cls, name, bases, dct)
```

#### Q116: How do you verify if an object is callable?
**Answer:** Using the built-in `callable(object)` function.

#### Q117: What does `hasattr()` do?
**Answer:** Returns `True` if the passed object has a named attribute, and `False` otherwise: `hasattr(obj, "name")`.

#### Q118: Explain the `setattr()` and `getattr()` functions.
**Answer:** 
*   `getattr(obj, "name")`: Gets the value of the named attribute.
*   `setattr(obj, "name", value)`: Sets the value of the named attribute.

#### Q119: What is the purpose of `delattr()`?
**Answer:** Deletes an attribute from an object instance: `delattr(obj, "name")`.

#### Q120: How do you dynamically create a class at runtime?
**Answer:** Using the three-argument call of the `type` constructor: `type(class_name, bases_tuple, attributes_dict)`.

---

## Exceptions & File I/O (Q121 - Q140)

#### Q121: How do you handle exceptions in Python?
**Answer:** Using `try`, `except`, `else`, and `finally` blocks:
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    result = 0
```

#### Q122: What does the `finally` block do?
**Answer:** A cleanup block that is guaranteed to execute whether an exception occurred or not, commonly used to close file streams or DB connections.

#### Q123: Explain the `else` block in exception handling.
**Answer:** Executes only if no exceptions were raised during the execution of the `try` block.

#### Q124: How do you raise an exception manually?
**Answer:** Using the `raise` keyword: `raise ValueError("Invalid number input")`.

#### Q125: How do you create a custom exception class?
**Answer:** Create a subclass inheriting from the built-in `Exception` class:
```python
class MyCustomError(Exception):
    pass
```

#### Q126: What is a context manager?
**Answer:** An object that manages runtime environments using the `with` statement, automating resource setup and teardown.

#### Q127: Explain the `with` statement.
**Answer:** Automatically closes resource streams (like files or database connections) when execution exits the block, even if exceptions occur.

#### Q128: How do you create a custom context manager class?
**Answer:** By implementing the `__enter__` and `__exit__` magic methods:
```python
class FileOpener:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
```

#### Q129: What is the `contextlib` module?
**Answer:** A standard library module providing decorators and utilities to create context managers easily (e.g., `@contextmanager`).

#### Q130: What is the difference between reading a file with `read()`, `readline()`, and `readlines()`?
**Answer:** 
*   `read()`: Reads the entire file content as a single string.
*   `readline()`: Reads a single line of the file.
*   `readlines()`: Reads the entire file, returning a list of line strings.

#### Q131: How do you open a file for writing in binary mode?
**Answer:** Open it with the mode string `"wb"`: `open("file.bin", "wb")`.

#### Q132: What is the difference between `"w"` and `"a"` write modes?
**Answer:** 
*   `"w"`: Overwrites the file contents if it exists, or creates it if missing.
*   `"a"`: Appends data to the end of the file if it exists, preserving previous contents.

#### Q133: Explain `StopIteration` exception.
**Answer:** A built-in exception raised by an iterator's `__next__` method to signal that there are no further elements to retrieve.

#### Q134: How do you catch multiple distinct exceptions?
**Answer:**
```python
try:
    pass
except (ValueError, TypeError) as e:
    print(f"Error: {e}")
```

#### Q135: What is the danger of a bare `except:` block?
**Answer:** It catches all exceptions, including system exits (`SystemExit`, `KeyboardInterrupt`), which makes it difficult to terminate the script with `Ctrl+C`.

#### Q136: Explain exception chaining.
**Answer:** Raising a new exception while preserving the stack trace of the original exception using the `from` keyword: `raise ValueError("Invalid") from KeyError`.

#### Q137: What is the `sys.argv` list?
**Answer:** A list of command-line arguments passed to a Python script, where `sys.argv[0]` represents the script name itself.

#### Q138: How do you serialize Python objects to disk?
**Answer:** Using the built-in `pickle` module or converting them to JSON format using the `json` module.

#### Q139: What is the risk of using `pickle` for untrusted data?
**Answer:** Security hazard. Deserializing untrusted pickles can execute arbitrary code on the host machine.

#### Q140: What does `file.seek(offset)` do?
**Answer:** Sets the file's current read/write pointer to a new position relative to the beginning, current position, or end.

---

## Comprehensions, Iterators & Generators (Q141 - Q170)

#### Q141: What is a List Comprehension?
**Answer:** A concise syntax to construct lists from existing iterables: `[x**2 for x in range(5)]`.

#### Q142: How do you write a list comprehension with a conditional statement?
**Answer:**
```python
evens = [x for x in range(10) if x % 2 == 0]
```

#### Q143: Explain Dictionary Comprehensions.
**Answer:** A concise syntax to construct dictionaries: `{x: x**2 for x in range(3)}`.

#### Q144: Explain Set Comprehensions.
**Answer:** A concise syntax to construct sets: `{x for x in [1, 2, 2, 3]}` yields `{1, 2, 3}`.

#### Q145: What is a Generator?
**Answer:** A function that yields values lazily using the `yield` keyword instead of returning a single value, returning a generator iterator.

#### Q146: What is the difference between a function containing `return` vs. one containing `yield`?
**Answer:** 
*   `return`: Terminates the function execution and returns a value.
*   `yield`: Pauses the function execution, returning a value to the caller, and retains its local state to resume from that point on the next call.

#### Q147: What is a Generator Expression?
**Answer:** A concise syntax returning an evaluator iterator, declared using parentheses: `(x**2 for x in range(10))`.

#### Q148: What is the difference between a List Comprehension and a Generator Expression?
**Answer:** 
*   **List Comprehension**: Evaluates immediately and builds the entire list in memory.
*   **Generator Expression**: Evaluates lazily, yielding one element at a time on request, which is much more memory efficient for large collections.

#### Q149: What is an Iterable?
**Answer:** An object that can return its elements one at a time, implementing the `__iter__` method (e.g., list, string, tuple).

#### Q150: What is an Iterator?
**Answer:** An object representing a stream of data that implements `__next__` and `__iter__` methods, returning elements on demand.

#### Q151: How do you manually get the next value from an iterator?
**Answer:** Using the built-in `next(iterator)` function.

#### Q152: How does a `for` loop work under the hood?
**Answer:** It calls `iter()` on the iterable to get an iterator, then repeatedly calls `next()` on the iterator inside a `try-except` block, stopping when a `StopIteration` exception is caught.

#### Q153: Can you reset an iterator?
**Answer:** No. Once an iterator is exhausted, it cannot be reset. You must create a new iterator instance from the original iterable.

#### Q154: Explain the `iter()` function.
**Answer:** Returns an iterator object for the passed iterable container.

#### Q155: How do you create a custom iterator class?
**Answer:** Implement `__iter__` (returning `self`) and `__next__` (returning the next item or raising `StopIteration`).

#### Q156: What is a Decorator?
**Answer:** A design pattern that allows you to modify or extend the behavior of a function or class without changing its source code.

#### Q157: How do you write a simple function decorator?
**Answer:**
```python
def my_decorator(func):
    def wrapper():
        print("Before call")
        func()
        print("After call")
    return wrapper
```

#### Q158: What is the `@` syntax for decorators?
**Answer:** Syntactic sugar to apply a decorator:
```python
@my_decorator
def hello():
    print("Hello World")
```

#### Q159: What is the purpose of `functools.wraps`?
**Answer:** A decorator applied to the wrapper function inside a custom decorator to preserve the name, docstring, and metadata of the original decorated function.

#### Q160: How do you write a decorator that accepts arguments?
**Answer:** By wrapping it in another outer function that accepts the arguments:
```python
def repeat(num):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(num):
                func(*args, **kwargs)
        return wrapper
    return decorator
```

#### Q161: What is a class decorator?
**Answer:** A decorator applied to a class definition that takes a class object as its argument and returns a modified class.

#### Q162: Explain the `yield from` expression.
**Answer:** A syntax to delegate generator operations to another sub-generator or iterable:
```python
def count():
    yield from range(3)
```

#### Q163: How do you send values into a generator dynamically?
**Answer:** Using the `generator.send(value)` method.

#### Q164: Explain the `generator.throw(type)` method.
**Answer:** Raises an exception of the specified type inside the generator function at the point where it was paused.

#### Q165: Explain `generator.close()`.
**Answer:** Raises a `GeneratorExit` exception inside the generator, stopping further iterations.

#### Q166: What is the difference between `itertools.count` and `range()`?
**Answer:** 
*   `range()`: Has a defined start and stop boundary.
*   `itertools.count()`: An infinite iterator that yields incrementing integers indefinitely.

#### Q167: Explain the `itertools.cycle` utility.
**Answer:** An infinite iterator that cycles through the elements of an input iterable repeatedly.

#### Q168: What is the purpose of `itertools.chain`?
**Answer:** Combines multiple iterables into a single sequence, yielding elements from each sequentially.

#### Q169: Explain list comprehension nesting.
**Answer:** Using one list comprehension inside another, similar to nested for loops: `[[x for x in range(3)] for y in range(2)]`.

#### Q170: How do you sort a list of dictionaries using a key?
**Answer:** Using the `sorted()` function with a lambda key: `sorted(my_list, key=lambda x: x['age'])`.
