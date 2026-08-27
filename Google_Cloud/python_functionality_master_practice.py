"""
===============================================================================
MASTER PYTHON FUNCTIONALITY PRACTICE MODULE
===============================================================================
A self-contained, executable reference covering all core Python features:
1. Data Types & Control Flow (including structural pattern matching)
2. Advanced Data Structures & Collections (Counter, defaultdict, deque)
3. Functions, Generators, & Decorators (@wraps, @lru_cache)
4. Object-Oriented Programming (Properties, Dunder methods, Abstract Classes)
5. Exception Handling & Custom Context Managers
6. File I/O & Data Serialization (JSON)
7. Concurrency: Multi-Threading, Multi-Processing, & Asyncio
8. Modern Type Hints & Dataclasses (@dataclass)
===============================================================================
"""

import os
import sys
import json
import time
import asyncio
import logging
import functools
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from collections import defaultdict, Counter, deque, namedtuple
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import List, Dict, Set, Tuple, Optional, Union, Any, Generator, Callable

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("PythonPractice")


# =============================================================================
# 1. DATA TYPES, CONTROL FLOW & PATTERN MATCHING
# =============================================================================

def demo_control_flow_and_matching(val: Any) -> str:
    """Demonstrates Python 3.10+ Structural Pattern Matching (match/case)."""
    match val:
        case int(x) if x > 100:
            return f"Large integer: {x}"
        case int(x):
            return f"Standard integer: {x}"
        case [first, *rest]:
            return f"List starting with {first}, remaining count: {len(rest)}"
        case {"status": "SUCCESS", "code": code}:
            return f"Success response with code: {code}"
        case str(text):
            return f"String input: {text.upper()}"
        case _:
            return "Unknown data structure"


# =============================================================================
# 2. ADVANCED DATA STRUCTURES & COLLECTIONS
# =============================================================================

def demo_collections():
    """Demonstrates Counter, defaultdict, deque, and namedtuple."""
    logger.info("=== 2. ADVANCED COLLECTIONS DEMO ===")
    
    # 1. Counter
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    word_counts = Counter(words)
    logger.info(f"Top 2 Most Common Words: {word_counts.most_common(2)}")
    
    # 2. defaultdict (avoid KeyError)
    grouped_data = defaultdict(list)
    items = [("even", 2), ("odd", 1), ("even", 4), ("odd", 3)]
    for key, num in items:
        grouped_data[key].append(num)
    logger.info(f"DefaultDict Grouped Data: {dict(grouped_data)}")
    
    # 3. deque (double-ended queue with O(1) appends/pops)
    queue = deque(maxlen=3)
    queue.append(10)
    queue.append(20)
    queue.append(30)
    queue.append(40) # 10 drops off automatically because maxlen=3
    logger.info(f"Deque (Maxlen=3): {list(queue)}")
    
    # 4. NamedTuple
    Point = namedtuple("Point", ["x", "y"])
    pt = Point(10, 20)
    logger.info(f"NamedTuple Point: x={pt.x}, y={pt.y}")


# =============================================================================
# 3. FUNCTIONS, GENERATORS & DECORATORS
# =============================================================================

def timing_decorator(func: Callable) -> Callable:
    """Custom decorator preserving metadata using @functools.wraps."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start_time
        logger.info(f"Function [{func.__name__}] executed in {elapsed:.6f} seconds.")
        return result
    return wrapper


@timing_decorator
@functools.lru_cache(maxsize=128)
def fibonacci_memoized(n: int) -> int:
    """O(N) Time complexity Fibonacci using LRU Cache memoization."""
    if n <= 1:
        return n
    return fibonacci_memoized(n - 1) + fibonacci_memoized(n - 2)


def stream_even_numbers(limit: int) -> Generator[int, None, None]:
    """Generator function demonstrating memory-efficient O(1) streaming."""
    for num in range(limit):
        if num % 2 == 0:
            yield num


# =============================================================================
# 4. OBJECT-ORIENTED PROGRAMMING (OOP), PROPERTIES & DUNDER METHODS
# =============================================================================

class BaseRepository(ABC):
    """Abstract Base Class (ABC) enforcing contract definitions."""
    @abstractmethod
    def save(self, record: Dict[str, Any]) -> bool:
        pass


class UserAccount(BaseRepository):
    """Encapsulated class with properties, thread lock, and dunder methods."""
    def __init__(self, username: str, initial_balance: float = 0.0):
        self.username = username
        self._balance = initial_balance  # Encapsulated private variable
        self._lock = threading.Lock()     # Thread safety lock

    @property
    def balance(self) -> float:
        """Read-only balance property."""
        with self._lock:
            return self._balance

    def deposit(self, amount: float):
        """Thread-safe deposit operation."""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        with self._lock:
            self._balance += amount
            logger.info(f"User [{self.username}] deposited ${amount:.2f}. New Balance: ${self._balance:.2f}")

    def save(self, record: Dict[str, Any]) -> bool:
        """Concrete implementation of BaseRepository abstract method."""
        logger.info(f"Saved user record to repository: {record}")
        return True

    def __repr__(self) -> str:
        return f"UserAccount(username='{self.username}', balance={self._balance:.2f})"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, UserAccount):
            return self.username == other.username
        return False


# =============================================================================
# 5. CUSTOM CONTEXT MANAGERS & ERROR HANDLING
# =============================================================================

class ManagedResource:
    """Custom Context Manager enforcing setup/cleanup via __enter__ and __exit__."""
    def __init__(self, resource_name: str):
        self.resource_name = resource_name

    def __enter__(self):
        logger.info(f"Acquiring Resource: [{self.resource_name}]...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Releasing Resource: [{self.resource_name}]...")
        if exc_type:
            logger.error(f"Handled Exception inside Context Manager: {exc_val}")
        return True  # Suppresses exception propagation if set to True


# =============================================================================
# 6. DATACLASSES & MODERN TYPE HINTS
# =============================================================================

@dataclass(frozen=True)
class EmployeeRecord:
    """Immutable Dataclass generating automatic __init__, __repr__, and __eq__."""
    emp_id: int
    name: str
    department: str
    skills: Tuple[str, ...] = field(default_factory=tuple)

    def is_engineering(self) -> bool:
        return self.department.lower() == "engineering"


# =============================================================================
# 7. CONCURRENCY: MULTI-THREADING, MULTI-PROCESSING & ASYNCIO
# =============================================================================

def cpu_bound_task(n: int) -> int:
    """Heavy mathematical task for Multi-Processing (Bypasses Python GIL)."""
    return sum(i * i for i in range(n))


def run_multiprocessing():
    """Executes tasks in parallel using process pools (Multi-core scaling)."""
    logger.info("=== 7A. MULTI-PROCESSING DEMO (CPU-Bound) ===")
    inputs = [5_000_000, 5_000_000, 5_000_000, 5_000_000]
    with ProcessPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        results = list(executor.map(cpu_bound_task, inputs))
    logger.info(f"Multi-Processing Results: {results[:2]}...")


async def async_fetch_data(task_id: int, delay: float) -> Dict[str, Any]:
    """Asynchronous IO-bound task using asyncio."""
    logger.info(f"Async Task [{task_id}] starting (Simulating {delay}s delay)...")
    await asyncio.sleep(delay)
    logger.info(f"Async Task [{task_id}] finished.")
    return {"task_id": task_id, "status": "COMPLETED"}


async def run_asyncio_tasks():
    """Executes non-blocking concurrent async tasks using asyncio.gather."""
    logger.info("=== 7B. ASYNCIO DEMO (IO-Bound Non-blocking) ===")
    tasks = [
        async_fetch_data(1, 0.5),
        async_fetch_data(2, 0.3),
        async_fetch_data(3, 0.1)
    ]
    results = await asyncio.gather(*tasks)
    logger.info(f"Asyncio Combined Results: {results}")


# =============================================================================
# MAIN EXECUTION ROUTINE
# =============================================================================

def main():
    logger.info("🚀 Starting Master Python Practice Script Execution...\n")

    # 1. Pattern Matching
    logger.info("=== 1. PATTERN MATCHING DEMO ===")
    logger.info(demo_control_flow_and_matching(150))
    logger.info(demo_control_flow_and_matching(["GCP", "Python", "Docker"]))
    logger.info(demo_control_flow_and_matching({"status": "SUCCESS", "code": 200}))

    # 2. Collections
    demo_collections()

    # 3. Generators & Decorators
    logger.info("\n=== 3. GENERATORS & DECORATORS DEMO ===")
    fib_30 = fibonacci_memoized(30)
    logger.info(f"Fibonacci(30) Result: {fib_30}")
    evens = list(stream_even_numbers(10))
    logger.info(f"Streamed Evens (<10): {evens}")

    # 4. OOP & Properties
    logger.info("\n=== 4. OOP & PROPERTIES DEMO ===")
    user = UserAccount(username="biswanath_giri", initial_balance=100.0)
    user.deposit(50.0)
    logger.info(f"User Representation: {repr(user)}")
    user.save({"username": user.username, "balance": user.balance})

    # 5. Context Manager
    logger.info("\n=== 5. CONTEXT MANAGER DEMO ===")
    with ManagedResource("GCP_BigQuery_Connection"):
        logger.info("Inside managed resource block executing queries...")

    # 6. Dataclasses
    logger.info("\n=== 6. DATACLASSES DEMO ===")
    emp = EmployeeRecord(emp_id=101, name="Alice", department="Engineering", skills=("Python", "GCP", "Kubernetes"))
    logger.info(f"Employee Dataclass: {emp}")
    logger.info(f"Is Engineering? {emp.is_engineering()}")

    # 7. Concurrency
    logger.info("\n=== 7. CONCURRENCY DEMOS ===")
    run_multiprocessing()
    asyncio.run(run_asyncio_tasks())

    logger.info("\n✅ All Python Functionality Demos Executed Successfully!")


if __name__ == "__main__":
    main()
