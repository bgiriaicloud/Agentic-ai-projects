# Python 250 Interview Questions & Answers - Part 3 (Q171 - Q250)

This document is Part 3 of the comprehensive Python interview questions series, covering Memory Management, Concurrency & Parallelism, testing, logging, and advanced system integrations.

---

## 📋 Table of Contents
*   [Memory Management & Garbage Collection (Q171 - Q195)](#memory-management--garbage-collection-q171---q195)
*   [Concurrency, Parallelism & AsyncIO (Q196 - Q225)](#concurrency-parallelism--asyncio-q196---q225)
*   [Testing, Logging & Diagnostic Profiling (Q226 - Q250)](#testing-logging--diagnostic-profiling-q226---q250)

---

## Memory Management & Garbage Collection (Q171 - Q195)

#### Q171: How is memory managed in Python?
**Answer:** Python uses a private heap space to manage memory. The Python memory manager allocates heap space for objects, while automatic garbage collection reclaims unused memory.

#### Q172: What is Reference Counting?
**Answer:** Python's primary memory reclamation mechanism. Each object tracks how many references point to it. When an object's reference count drops to zero, the object is immediately deleted and its memory is freed.

#### Q173: How do you check the reference count of an object?
**Answer:** Using the `sys.getrefcount(object)` function. Note that this function returns a count that is 1 higher than expected because passing the object to `getrefcount()` creates a temporary reference.

#### Q174: What is a Reference Cycle (Circular Reference)?
**Answer:** A scenario where two or more objects reference each other, creating a cycle (e.g., `A` references `B`, and `B` references `A`). Their reference counts never drop to zero, even if they are no longer reachable from the root program.

#### Q175: How does Python detect and clean up reference cycles?
**Answer:** Using a cyclic garbage collector (via the `gc` module) that runs periodically. It detects unreachable object clusters by checking for cyclic references and frees their memory.

#### Q176: What are the three generations in Python's garbage collector?
**Answer:** The garbage collector organizes objects into three generations (0, 1, and 2) based on how long they have survived. New objects are placed in Generation 0. If they survive a garbage collection run, they are promoted to the next generation, with Generation 2 containing long-lived objects.

#### Q177: How do you manually trigger garbage collection?
**Answer:** Import the `gc` module and run `gc.collect()`.

#### Q178: What are Weak References?
**Answer:** References to an object that do not increment its reference count, created using the `weakref` module. This allows the object to be garbage collected even if weak references still point to it, which is useful for caching.

#### Q179: What is the Python Global Interpreter Lock (GIL)?
**Answer:** A mutex lock that ensures only one thread executes Python bytecode at a time, protecting the interpreter's state and reference counts from race conditions.

#### Q180: What is a memory leak in Python, and how does it happen?
**Answer:** A scenario where unused memory is not reclaimed, commonly caused by maintaining references to objects in global lists or dictionaries, or by uncollected circular references containing custom `__del__` methods in older Python versions.

#### Q181: Explain the purpose of the `sys.getsizeof()` function.
**Answer:** Returns the memory consumption size of an object in bytes, including garbage collection overhead.

#### Q182: How does Python optimize memory for small integers?
**Answer:** Integer caching. Python pre-allocates and caches integers in the range `-5` to `256` during startup. Any reference to these numbers points to the same pre-cached object in memory.

#### Q183: What is String Interning?
**Answer:** An optimization where Python stores only one copy of each distinct string value in a lookup table, allowing string comparisons to be performed as fast pointer comparison operations instead of character-by-character matches.

#### Q184: How do you force string interning?
**Answer:** Using the `sys.intern(string)` function.

#### Q185: What does the `__del__` method do?
**Answer:** The destructor method, called automatically when an object's reference count reaches zero, immediately before it is garbage collected.

#### Q186: Why is relying on `__del__` for resource cleanup discouraged?
**Answer:** The timing of its execution is not guaranteed, and errors raised inside `__del__` are ignored by the interpreter. It is better to use context managers (`with` statements).

#### Q187: Explain Python's memory allocation layers (PyMalloc).
**Answer:** An internal small-object allocator built on top of the standard C `malloc` to optimize memory allocations for objects smaller than 512 bytes, minimizing system call overhead.

#### Q188: What is the role of the `gc.garbage` list?
**Answer:** A list of uncollectable, unreachable objects (such as circular references with custom `__del__` methods in Python versions prior to 3.4) that the garbage collector could not clean up.

#### Q189: How do you disable the garbage collector?
**Answer:** Run `gc.disable()`. Disabling the garbage collector disables cyclic detection but leaves reference counting active.

#### Q190: What is the difference between memory fragmentation and a memory leak?
**Answer:** 
*   **Leak**: Memory is held by unreachable or unused objects.
*   **Fragmentation**: Free memory is split into small, non-contiguous blocks, preventing allocations for large objects.

#### Q191: How does Python handle memory for lists when they grow?
**Answer:** Over-allocation. When a list runs out of space, Python allocates extra capacity to minimize the performance cost of subsequent appends.

#### Q192: What is the purpose of `weakref.WeakValueDictionary`?
**Answer:** A dictionary subclass where values are stored as weak references. If a value is no longer referenced elsewhere in the program, its entry is automatically removed from the dictionary.

#### Q193: Explain memory views (`memoryview`).
**Answer:** A built-in class that allows Python code to access the internal buffer data of an object (like bytes or bytearrays) without copying the data in memory, which is useful for handling large files or binary streams efficiently.

#### Q194: What is the difference between stack and heap memory allocations?
**Answer:** 
*   **Stack**: Stores function call frames, local variables, and execution scopes.
*   **Heap**: Stores all Python objects and their dynamically allocated data.

#### Q195: How do you profile memory usage in a Python script?
**Answer:** Using third-party profiling libraries like `memory_profiler` or the built-in `tracemalloc` module.

---

## Concurrency, Parallelism & AsyncIO (Q196 - Q225)

#### Q196: What is the difference between Concurrency and Parallelism?
**Answer:** 
*   **Concurrency**: Managing and executing multiple tasks by switching between them (overlapping execution).
*   **Parallelism**: Executing multiple tasks at the exact same time on multiple CPU cores.

#### Q197: Why does multi-threading in Python not achieve true parallelism for CPU-bound tasks?
**Answer:** Because of the Global Interpreter Lock (GIL), which restricts execution to only one thread at a time, even on multi-core processors.

#### Q198: When should you use multi-threading?
**Answer:** For **I/O-bound tasks** (e.g., web scraping, file downloads, database queries) where threads spend most of their time waiting for external operations to complete.

#### Q199: When should you use multi-processing?
**Answer:** For **CPU-bound tasks** (e.g., heavy mathematical computations, image processing, data analysis) because each process runs in its own Python interpreter with its own GIL, enabling true parallel execution across multiple CPU cores.

#### Q200: What is `asyncio`?
**Answer:** A standard Python library used to write concurrent code using the `async`/`await` syntax, utilizing a single-threaded event loop to manage asynchronous I/O operations.

#### Q201: Explain the difference between `async def` and `def`.
**Answer:** 
*   `def`: Defines a standard synchronous function.
*   `async def`: Defines a coroutine function, which returns a coroutine object when called instead of executing the code immediately.

#### Q202: What does the `await` keyword do?
**Answer:** Pauses the execution of a coroutine, yielding control back to the event loop to run other tasks until the awaited operation completes.

#### Q203: What is the Event Loop in `asyncio`?
**Answer:** The core engine of `asyncio` that manages and schedules the execution of asynchronous tasks, handles network connections, and coordinates I/O events.

#### Q204: How do you run the event loop in Python 3.7+?
**Answer:** Using `asyncio.run(main_coroutine())`.

#### Q205: What is the difference between a Task and a Future in `asyncio`?
**Answer:** 
*   **Future**: An object that represents an eventual result of an asynchronous operation.
*   **Task**: A subclass of Future that wraps a coroutine and schedules its execution on the event loop.

#### Q206: How do you run multiple coroutines concurrently in `asyncio`?
**Answer:** Using `asyncio.gather(*coroutines)`.

#### Q207: What is the `threading` module?
**Answer:** The standard library module used to create and manage operating system threads.

#### Q208: What is a Race Condition?
**Answer:** A bug that occurs when multiple threads attempt to read and modify shared data concurrently, leading to unpredictable results.

#### Q209: How do you prevent race conditions in multi-threaded programs?
**Answer:** Using synchronization primitives like `Lock` or `RLock` (re-entrant lock) from the `threading` module to ensure only one thread accesses shared code blocks at a time.

#### Q210: What is a Deadlock?
**Answer:** A situation where two or more threads are blocked indefinitely, each waiting for a lock held by another thread in the cycle.

#### Q211: Explain the `multiprocessing` module.
**Answer:** A package that supports spawning side processes using an API similar to the `threading` module, bypassing the GIL to utilize multiple CPU cores.

#### Q212: How do you share data between processes in the `multiprocessing` module?
**Answer:** Since processes do not share memory, you must use inter-process communication (IPC) tools like `Queue`, `Pipe`, or `Value` / `Array` in shared memory.

#### Q213: Explain the concept of a Process Pool.
**Answer:** A collection of pre-spawned worker processes managed by a controller (e.g., `multiprocessing.Pool`), used to distribute batch tasks across multiple cores.

#### Q214: What is the `concurrent.futures` module?
**Answer:** A high-level interface for asynchronously executing callables using pools of threads (`ThreadPoolExecutor`) or processes (`ProcessPoolExecutor`).

#### Q215: Explain the `daemon` thread property.
**Answer:** A boolean flag. A daemon thread runs in the background and does not prevent the Python program from exiting if only daemon threads are left running.

#### Q216: What is the GIL's impact on C extensions?
**Answer:** C extensions can release the GIL while performing heavy computations or long I/O operations, allowing true parallelism outside the Python runtime.

#### Q217: Why is `asyncio` preferred over multi-threading for high-concurrency web servers?
**Answer:** Threads have high memory overhead (typically 8MB stack per thread). `asyncio` uses a single thread to multiplex connections, supporting thousands of concurrent connections with minimal memory usage.

#### Q218: How do you run a synchronous, blocking function inside an asynchronous function?
**Answer:** Run it in a separate thread pool executor using `loop.run_in_executor()`, preventing the event loop from blocking.

#### Q219: What does `asyncio.sleep()` do?
**Answer:** Pauses the coroutine non-blockingly, allowing the event loop to run other tasks, unlike `time.sleep()`, which blocks the entire thread.

#### Q220: What is the purpose of the `Queue` class in the `queue` module?
**Answer:** Provides a thread-safe FIFO queue implementation, commonly used for producer-consumer workflows.

#### Q221: What is a Thread Local variable?
**Answer:** A variable whose values are specific to individual threads, managed using the `threading.local()` class.

#### Q222: How do you terminate a process spawned by the `multiprocessing` module?
**Answer:** Call the `process.terminate()` or `process.kill()` method.

#### Q223: Explain the `async for` statement.
**Answer:** Used to iterate over an asynchronous iterator, where the next element is retrieved using an asynchronous call (e.g., streaming network packets).

#### Q224: Explain the `async with` statement.
**Answer:** Used to enter an asynchronous context manager, where the setup and teardown methods (`__aenter__`, `__aexit__`) are coroutines.

#### Q225: What is the CPU affinity of a process?
**Answer:** A scheduler setting that binds a process to run on a specific CPU core or set of cores, configured using the `os` module or external tools.

---

## Testing, Logging & Diagnostic Profiling (Q226 - Q250)

#### Q226: What is Unit Testing?
**Answer:** A software testing method where individual components of a program (like functions or classes) are tested in isolation to verify they work as expected.

#### Q227: Explain the built-in `unittest` module.
**Answer:** Python's standard unit testing framework, which uses classes inheriting from `unittest.TestCase` to group test assertions.

#### Q228: What is `pytest`?
**Answer:** A popular third-party testing framework that simplifies writing tests using plain assertions and provides features like fixtures and parameterization.

#### Q229: What are Test Fixtures in `pytest`?
**Answer:** Functions run before (and optionally after) tests to set up the environment, database state, or mock objects needed for the tests.

#### Q230: How do you assert that a specific exception is raised in a test?
**Answer:** 
*   In `unittest`: `with self.assertRaises(ValueError):`.
*   In `pytest`: `with pytest.raises(ValueError):`.

#### Q231: Explain the concept of Mocking in tests.
**Answer:** Replacing real dependencies or APIs (like database calls or external HTTP endpoints) with dummy objects (mocks) to isolate the code being tested.

#### Q232: What is the purpose of the `unittest.mock` module?
**Answer:** A standard library module providing the `Mock` and `MagicMock` classes, along with the `@patch` decorator to mock modules or classes during tests.

#### Q233: Explain the `logging` module.
**Answer:** The standard library module used to log diagnostic messages during application execution, offering customizable formatters and handlers.

#### Q234: What are the default log levels in Python?
**Answer:** In increasing order of severity: `DEBUG`, `INFO`, `WARNING` (default threshold), `ERROR`, and `CRITICAL`.

#### Q235: How do you configure logging to output to both console and a file?
**Answer:** Add both a `StreamHandler` (for the console) and a `FileHandler` (for the file) to the root logger configuration.

#### Q236: Explain the difference between logging formatters and handlers.
**Answer:** 
*   **Formatter**: Defines the layout and structure of the log message text.
*   **Handler**: Determines where the log message is sent (e.g., standard output, a log file, or an email server).

#### Q237: What is the `timeit` module?
**Answer:** A tool used to measure the execution time of small snippets of Python code, avoiding common timing pitfalls like CPU scheduling changes.

#### Q238: What is `cProfile`?
**Answer:** A built-in profiling tool that measures how long and how often individual functions in a program are executed, helping to identify performance bottlenecks.

#### Q239: How do you run `cProfile` on a script from the command line?
**Answer:** Run `python -m cProfile script.py`.

#### Q240: Explain the `pstats` module.
**Answer:** A utility module used to format, sort, and analyze the profiling data reports generated by `cProfile`.

#### Q241: What does `sys.path` represent?
**Answer:** A list of directory paths where Python looks for modules when importing them, initialized from the `PYTHONPATH` environment variable.

#### Q242: What is the difference between `os.system()` and the `subprocess` module?
**Answer:** 
*   `os.system()`: Runs a command in a subshell, returning only the exit status.
*   `subprocess`: A modern module (using `subprocess.run()`) that allows you to spawn subprocesses, connect to their input/output/error pipes, and obtain their exit codes.

#### Q243: Explain `shutil.copytree()`.
**Answer:** A utility function used to recursively copy an entire directory tree from a source path to a destination path.

#### Q244: What is a Virtual Environment (virtualenv / venv)?
**Answer:** An isolated Python runtime environment that allows you to install package dependencies for a project without affecting the global system Python installation.

#### Q245: How do you create a virtual environment in Python 3?
**Answer:** Run `python3 -m venv myenv`.

#### Q246: What does the command `pip freeze` do?
**Answer:** Outputs a list of all installed packages in the current environment along with their exact versions, suitable for creating a `requirements.txt` file.

#### Q247: What is the purpose of `setup.py`?
**Answer:** The build script for Python packages, defining metadata (name, version, author) and dependency requirements for distribution.

#### Q248: What is a Wheel (`.whl`) file?
**Answer:** The standard built-in packaging format for Python, containing compiled binaries or source files ready to be installed via `pip`.

#### Q249: Explain the `warnings` module.
**Answer:** A module used to alert developers of deprecations, API changes, or non-fatal issues in their code without halting execution.

#### Q250: What is the purpose of the `__main__` guard (`if __name__ == "__main__":`)?
**Answer:** A guard statement that ensures block code only runs if the script is executed directly from the terminal, preventing it from running if the script is imported as a module in another file.
