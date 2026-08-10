# Python 100 Interview Programs - Part 1 (Programs 1 - 50)

This document is Part 1 of the essential interview preparation programs in Python, providing short, clean, and self-contained code snippets.

---

## 📋 Table of Contents
*   [Basic Calculations & Logic (Programs 1 - 15)](#basic-calculations--logic-programs-1---15)
*   [String Operations & Manipulation (Programs 16 - 30)](#string-operations--manipulation-programs-16---30)
*   [Array & List Processing (Programs 31 - 50)](#array--list-processing-programs-31---50)

---

## Basic Calculations & Logic (Programs 1 - 15)

### 1. Swap Two Variables Without a Temp Variable
```python
a = 5
b = 10
a, b = b, a
print(f"a: {a}, b: {b}")  # a: 10, b: 5
```

### 2. Check if a Number is Even or Odd
```python
def is_even(n):
    return n % 2 == 0

print(is_even(4))  # True
print(is_even(7))  # False
```

### 3. Find the Factorial of a Number (Iterative)
```python
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

print(factorial(5))  # 120
```

### 4. Find the Factorial of a Number (Recursive)
```python
def factorial_rec(n):
    if n <= 1:
        return 1
    return n * factorial_rec(n - 1)

print(factorial_rec(5))  # 120
```

### 5. Generate Fibonacci Sequence Up to N Terms
```python
def fibonacci(n):
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq[:n]

print(fibonacci(7))  # [0, 1, 1, 2, 3, 5, 8]
```

### 6. Check if a Number is Prime
```python
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

print(is_prime(11))  # True
print(is_prime(4))   # False
```

### 7. Find Greatest Common Divisor (GCD) of Two Numbers
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

print(gcd(48, 18))  # 6
```

### 8. Find Least Common Multiple (LCM) of Two Numbers
```python
def lcm(a, b):
    return abs(a * b) // gcd(a, b)

print(lcm(12, 18))  # 36
```

### 9. Check if a Year is a Leap Year
```python
def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

print(is_leap_year(2000))  # True
print(is_leap_year(1900))  # False
```

### 10. Check if a Number is an Armstrong Number
```python
def is_armstrong(n):
    digits = str(n)
    power = len(digits)
    total = sum(int(d)**power for d in digits)
    return total == n

print(is_armstrong(153))  # True (1^3 + 5^3 + 3^3 = 153)
```

### 11. Reverse an Integer
```python
def reverse_integer(n):
    sign = -1 if n < 0 else 1
    rev = int(str(abs(n))[::-1])
    return sign * rev

print(reverse_integer(-123))  # -321
```

### 12. Sum of Digits of a Number
```python
def sum_of_digits(n):
    return sum(int(d) for d in str(abs(n)))

print(sum_of_digits(456))  # 15
```

### 13. Convert Decimal to Binary String
```python
def decimal_to_binary(n):
    return bin(n)[2:]

print(decimal_to_binary(10))  # "1010"
```

### 14. Convert Binary String to Decimal
```python
def binary_to_decimal(b):
    return int(b, 2)

print(binary_to_decimal("1010"))  # 10
```

### 15. Check if a Number is a Perfect Number
```python
def is_perfect(n):
    if n <= 1:
        return False
    divisors_sum = sum(i for i in range(1, n) if n % i == 0)
    return divisors_sum == n

print(is_perfect(28))  # True (1 + 2 + 4 + 7 + 14 = 28)
```

---

## String Operations & Manipulation (Programs 16 - 30)

### 16. Reverse a String
```python
def reverse_string(s):
    return s[::-1]

print(reverse_string("python"))  # "nohtyp"
```

### 17. Check if a String is a Palindrome
```python
def is_palindrome(s):
    clean = "".join(char.lower() for char in s if char.isalnum())
    return clean == clean[::-1]

print(is_palindrome("A man, a plan, a canal: Panama"))  # True
```

### 18. Count Vowels and Consonants in a String
```python
def count_vowels_consonants(s):
    vowels = "aeiouAEIOU"
    v_count = 0
    c_count = 0
    for char in s:
        if char.isalpha():
            if char in vowels:
                v_count += 1
            else:
                c_count += 1
    return {"vowels": v_count, "consonants": c_count}

print(count_vowels_consonants("Hello World"))  # {'vowels': 3, 'consonants': 7}
```

### 19. Count Character Occurrences in a String
```python
from collections import Counter

def count_characters(s):
    return dict(Counter(s))

print(count_characters("hello"))  # {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

### 20. Find the First Non-Repeated Character in a String
```python
def first_non_repeated_char(s):
    counts = {}
    for char in s:
        counts[char] = counts.get(char, 0) + 1
    for char in s:
        if counts[char] == 1:
            return char
    return None

print(first_non_repeated_char("swiss"))  # "w"
```

### 21. Check if Two Strings are Anagrams
```python
def are_anagrams(s1, s2):
    return sorted(s1.lower()) == sorted(s2.lower())

print(are_anagrams("listen", "silent"))  # True
```

### 22. Remove All Duplicate Characters from a String
```python
def remove_duplicates(s):
    seen = set()
    result = []
    for char in s:
        if char not in seen:
            seen.add(char)
            result.append(char)
    return "".join(result)

print(remove_duplicates("hello"))  # "helo"
```

### 23. Capitalize the First and Last Character of Each Word
```python
def capitalize_ends(s):
    words = s.split()
    res = []
    for word in words:
        if len(word) > 1:
            res.append(word[0].upper() + word[1:-1] + word[-1].upper())
        else:
            res.append(word.upper())
    return " ".join(res)

print(capitalize_ends("hello world"))  # "HellO WorlD"
```

### 24. Find All Substrings of a String
```python
def get_substrings(s):
    return [s[i:j] for i in range(len(s)) for j in range(i + 1, len(s) + 1)]

print(get_substrings("abc"))  # ['a', 'ab', 'abc', 'b', 'bc', 'c']
```

### 25. Check if a String Contains Only Digits
```python
def is_only_digits(s):
    return s.isdigit()

print(is_only_digits("12345"))  # True
print(is_only_digits("123a5"))  # False
```

### 26. Count the Number of Words in a String
```python
def count_words(s):
    return len(s.split())

print(count_words("   Python is fun to learn   "))  # 5
```

### 27. Find the Longest Word in a Sentence
```python
def longest_word(sentence):
    words = sentence.split()
    return max(words, key=len) if words else ""

print(longest_word("Be extremely clean and consistent"))  # "consistent"
```

### 28. Remove All Whitespace from a String
```python
def remove_whitespace(s):
    return "".join(s.split())

print(remove_whitespace(" a b   c "))  # "abc"
```

### 29. Replace All Spaces with a Hyphen
```python
def replace_spaces_with_hyphen(s):
    return s.replace(" ", "-")

print(replace_spaces_with_hyphen("hello world app"))  # "hello-world-app"
```

### 30. Check if a Substring is Present in a String
```python
def has_substring(s, sub):
    return sub in s

print(has_substring("python coding", "code"))  # True
```

---

## Array & List Processing (Programs 31 - 50)

### 31. Find the Largest Element in a List
```python
def find_largest(arr):
    return max(arr) if arr else None

print(find_largest([1, 8, 3, 9, 2]))  # 9
```

### 32. Find the Smallest Element in a List
```python
def find_smallest(arr):
    return min(arr) if arr else None

print(find_smallest([1, 8, -3, 9, 2]))  # -3
```

### 33. Find the Second Largest Element in a List
```python
def second_largest(arr):
    unique = list(set(arr))
    if len(unique) < 2:
        return None
    unique.sort()
    return unique[-2]

print(second_largest([1, 8, 8, 9, 9, 2]))  # 8
```

### 34. Sum of All Elements in a List
```python
def sum_list(arr):
    return sum(arr)

print(sum_list([1, 2, 3, 4]))  # 10
```

### 35. Average of Elements in a List
```python
def average_list(arr):
    return sum(arr) / len(arr) if arr else 0

print(average_list([1, 2, 3, 4]))  # 2.5
```

### 36. Reverse a List In-Place
```python
def reverse_list_inplace(arr):
    arr.reverse()
    return arr

print(reverse_list_inplace([1, 2, 3]))  # [3, 2, 1]
```

### 37. Rotate a List to the Left by K Positions
```python
def rotate_left(arr, k):
    if not arr:
        return arr
    k = k % len(arr)
    return arr[k:] + arr[:k]

print(rotate_left([1, 2, 3, 4, 5], 2))  # [3, 4, 5, 1, 2]
```

### 38. Rotate a List to the Right by K Positions
```python
def rotate_right(arr, k):
    if not arr:
        return arr
    k = k % len(arr)
    return arr[-k:] + arr[:-k]

print(rotate_right([1, 2, 3, 4, 5], 2))  # [4, 5, 1, 2, 3]
```

### 39. Count Occurrences of an Element in a List
```python
def count_occurrences(arr, target):
    return arr.count(target)

print(count_occurrences([1, 2, 2, 3, 2], 2))  # 3
```

### 40. Find the Common Elements in Two Lists
```python
def common_elements(list1, list2):
    return list(set(list1) & set(list2))

print(common_elements([1, 2, 3], [2, 3, 4]))  # [2, 3]
```

### 41. Remove All Even Numbers from a List
```python
def remove_evens(arr):
    return [x for x in arr if x % 2 != 0]

print(remove_evens([1, 2, 3, 4, 5]))  # [1, 3, 5]
```

### 42. Check if a List is Sorted
```python
def is_sorted(arr):
    return arr == sorted(arr)

print(is_sorted([1, 2, 3]))  # True
print(is_sorted([1, 3, 2]))  # False
```

### 43. Merge Two Sorted Lists into One Sorted List
```python
def merge_sorted(arr1, arr2):
    result = []
    i, j = 0, 0
    while i < len(arr1) and j < len(arr2):
        if arr1[i] < arr2[j]:
            result.append(arr1[i])
            i += 1
        else:
            result.append(arr2[j])
            j += 1
    result.extend(arr1[i:])
    result.extend(arr2[j:])
    return result

print(merge_sorted([1, 3, 5], [2, 4, 6]))  # [1, 2, 3, 4, 5, 6]
```

### 44. Find the Missing Number in a List of 1 to N
```python
def find_missing_number(arr, n):
    expected_sum = n * (n + 1) // 2
    actual_sum = sum(arr)
    return expected_sum - actual_sum

print(find_missing_number([1, 2, 4, 5], 5))  # 3
```

### 45. Find the Intersection of Multiple Lists
```python
def list_intersection(*lists):
    if not lists:
        return []
    return list(set(lists[0]).intersection(*lists[1:]))

print(list_intersection([1, 2, 3], [2, 3, 4], [3, 4, 5]))  # [3]
```

### 46. Flatten a Nested List of Lists (One Level)
```python
def flatten_list(nested):
    return [item for sublist in nested for item in sublist]

print(flatten_list([[1, 2], [3, 4]]))  # [1, 2, 3, 4]
```

### 47. Check if a List Contains Sublist
```python
def is_sublist(main_list, sub_list):
    if not sub_list:
        return True
    n = len(sub_list)
    for i in range(len(main_list) - n + 1):
        if main_list[i:i+n] == sub_list:
            return True
    return False

print(is_sublist([1, 2, 3, 4], [2, 3]))  # True
```

### 48. Print Elements with Their Square Root as Key-Value Pairs
```python
def element_sqrt_map(arr):
    return {x: x**0.5 for x in arr if x >= 0}

print(element_sqrt_map([4, 9]))  # {4: 2.0, 9: 3.0}
```

### 49. Partition a List into Even and Odd Lists
```python
def partition_even_odd(arr):
    evens = [x for x in arr if x % 2 == 0]
    odds = [x for x in arr if x % 2 != 0]
    return evens, odds

print(partition_even_odd([1, 2, 3, 4]))  # ([2, 4], [1, 3])
```

### 50. Remove All Null / None Elements from a List
```python
def remove_none(arr):
    return [x for x in arr if x is not None]

print(remove_none([1, None, 2, None, 3]))  # [1, 2, 3]
```
