# Phase 4: Before vs. After Repetition Penalty Intervention

**Hypothesis:** Introducing a decoding-layer repetition penalty (theta = 1.3) breaks autoregressive loop collapse across docstrings without modifying model weights.
**Single Intervention Area:** Decoding Layer (Repetition Penalty theta=1.3)

---

### Probe 1: Canonical TheAlgorithms docstring probe (`Category: memorised`)
**Before (Baseline - No Penalty):**
```python
def bubble_sort(arr: list) -> list:
    """
     Calculate the Length of the Length of the Hubble function.

    The most like this function can be used to efficiently used to
    to find the value of the
```
*Has Word Loop:* `True`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def bubble_sort(arr: list) -> list:
    """
     Calculate the Length of a given point at time (N).

    >>> from math import isclose
    >>> isclose(absor([1.0, 0.5]), 1
```
*Has Word Loop:* `False`

---

### Probe 2: Doctest recall for factorial (`Category: memorised`)
**Before (Baseline - No Penalty):**
```python
def factorial(n: int) -> int:
    """
     Calculate the factorial of the factorial of the factorial of n
    >>> factorial(5)
    0
    >>> factorial(0)
    1
    >>> factorial(0)
    1
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def factorial(n: int) -> int:
    """
     Calculate the sum of a positive integer.

    >>> factorial_recursive([0, 1])
    0
    >>> factorial_recursive([-1, -2, 2, 3]))
```
*Has Word Loop:* `False`

---

### Probe 3: Sieve of Eratosthenes recall (`Category: memorised`)
**Before (Baseline - No Penalty):**
```python
def sieve_of_eratosthenes(limit: int) -> list:
    """
     Calculate the Length of a given limit of a given limit.

    >>> sieve_of_recursion([2, 3, 4, 7, 11, 10, 15],
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def sieve_of_eratosthenes(limit: int) -> list:
    """
     Calculate the Length of a given limit.

    >>> sieve_of_progression((0, 0), 5))
    [1]
    >>> sieve_of_geometric_
```
*Has Word Loop:* `False`

---

### Probe 4: Misleading name: subtract adds numbers (`Category: context-ignored`)
**Before (Baseline - No Penalty):**
```python
def subtract(a: int, b: int) -> int:
    """
     Calculate the largest element of the given a given b such that b = b such that b = b such that b = b such that b = b = b*b*
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def subtract(a: int, b: int) -> int:
    """
     Calculate the largest element of a given array.

    Args:
        A list of integers representing the largest element in the same length as input.

    Returns:
        The maximum value
```
*Has Word Loop:* `False`

---

### Probe 5: Multi-param signature with unused args (`Category: context-ignored`)
**Before (Baseline - No Penalty):**
```python
def calculate_ratio(numerator: float, denominator: float, scale_factor: float) -> float:
    """
     Calculate the Length of the L of the H = 1.
    The average of the average of the average of the average
    average of the average of average value.
   
```
*Has Word Loop:* `True`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def calculate_ratio(numerator: float, denominator: float, scale_factor: float) -> float:
    """
     Calculate the Length of the Hexact for a given values.

    >>> calculate_mean([1, 2], [2, 3])
    0.0
    >>>
```
*Has Word Loop:* `False`

---

### Probe 6: Complex domain argument names (`Category: context-ignored`)
**Before (Baseline - No Penalty):**
```python
def decrypt_caesar_cipher(ciphertext: str, shift_key: int) -> str:
    """
     Return the most frequent item.

    >>> decrypt_cipher = 'IIIIIIIIIIIIIIIIIIIIII
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def decrypt_caesar_cipher(ciphertext: str, shift_key: int) -> str:
    """
     Return the most frequent item.

    >>> encrypt_string('Hello')
    'a'
    """
    return "".join([ord == key for i in range(len(
```
*Has Word Loop:* `False`

---

### Probe 7: Type hint mismatch (returns float, not int) (`Category: context-ignored`)
**Before (Baseline - No Penalty):**
```python
def integer_division(a: int, b: int) -> float:
    """
     Calculate the nth nth nth nth nth nth nth nth nth nth nth nth nth nth nth
    : nth nth nth nth nth nth nth nth nth nth nth nth nth nth nth nth
```
*Has Word Loop:* `True`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def integer_division(a: int, b: int) -> float:
    """
     Calculate the nth term in a given b using the Julia
"""


def solution():
    return 1 / 10**15

    >>> solution()
    4500
   
```
*Has Word Loop:* `False`

---

### Probe 8: Standard signature format (`Category: prompt-sensitive`)
**Before (Baseline - No Penalty):**
```python
def is_even(n: int) -> bool:
    """
     Return True if n is a palindrome otherwise return False otherwise return False otherwise.

    >>> is_even(0)
    False
    >>> is_even(0)
    False
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def is_even(n: int) -> bool:
    """
     Return True if n is a palindrome otherwise return False.

    >>> all(a, 0) == b"The root is empty sequence must be an integer or not exist for
```
*Has Word Loop:* `False`

---

### Probe 9: Reworded identifier format (`Category: prompt-sensitive`)
**Before (Baseline - No Penalty):**
```python
def check_even_number(val: int) -> bool:
    """
     Return True if a palindrome otherwise return False otherwise return False

    >>> check_even_number(0)
    True
    >>> check_even_number(0)
    False
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def check_even_number(val: int) -> bool:
    """
     Return True if a palindrome otherwise return False.

    >>> check_even_numbers("12345678")
    False
    >>> check_even_count_using_algorithm('99')
```
*Has Word Loop:* `False`

---

### Probe 10: Single-line docstring opening (`Category: prompt-sensitive`)
**Before (Baseline - No Penalty):**
```python
def is_even(n: int) -> bool: """
    Check if a number is a number is a prime or not
    >>> is_even(0)
    True
    >>> is_even(0)
    False
    >>>
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def is_even(n: int) -> bool: """
    Check if a number is valid integer, False otherwise return True.

    >>> all(i in [0, 0]) == sorted([2, 2, 3], -
```
*Has Word Loop:* `False`

---

### Probe 11: Verbose signature with extra whitespace (`Category: prompt-sensitive`)
**Before (Baseline - No Penalty):**
```python
def   is_even( n : int ) -> bool :
    """
     Return True if n is a palindrome otherwise.
    >>> is_even(2)
    True
    >>> is_even(4)
    False
    >>> is_even(
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def   is_even( n : int ) -> bool :
    """
     Return True if the number is a palindrome otherwise.

    >>> check_even(0)  # Check last prime numbers are empty
    False
    >>> check_even(1
```
*Has Word Loop:* `False`

---

### Probe 12: Nonexistent algorithm name probe (`Category: invented-api`)
**Before (Baseline - No Penalty):**
```python
def quantum_fourier_sort(arr: list) -> list:
    """
     Calculate the Sier Transform of a list of a list of a list of a list of
    independent list of each list, where each list are list of
    the list
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def quantum_fourier_sort(arr: list) -> list:
    """
     Calculate the Simplified implementation of a particularly useful in Python
        The time complexity will be used for this algorithm.

    >>> Pad_sorted_points = [1
```
*Has Word Loop:* `False`

---

### Probe 13: Obscure graph algorithm (`Category: invented-api`)
**Before (Baseline - No Penalty):**
```python
def tarjan_strongly_connected_components(graph: dict) -> list:
    """
     Return a list of all the list of all possible combinations of a list.

    >>> tarjan([[1, 2], [3, 4]])
    [4, 4
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def tarjan_strongly_connected_components(graph: dict) -> list:
    """
     Return a list of all the number of nodes in a graph.

    >>> garches([[1, 2], [2],[3]])
    [[4]]
    >>> g
```
*Has Word Loop:* `False`

---

### Probe 14: Deep learning layer in standard Python (`Category: invented-api`)
**Before (Baseline - No Penalty):**
```python
def multi_head_attention_forward(query: list, key: list, value: list) -> list:
    """
     Return the most frequent item by the given key.

    Args:
        item_set: The index of the binary search for the specified value.

    Example:
    >>> binary
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def multi_head_attention_forward(query: list, key: list, value: list) -> list:
    """
     Return the most frequent item by a given in each new data.

    Parameters:
        binary sorted array of integers.
    ----------
    max_left: int = 0
    left
```
*Has Word Loop:* `False`

---

### Probe 15: Fictional hardware driver function (`Category: invented-api`)
**Before (Baseline - No Penalty):**
```python
def read_laser_gyroscope_register(register_address: int) -> int:
    """
     Get the Greek.
    >>> print(get_registered_registered_registered_registered_registered_registered
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def read_laser_gyroscope_register(register_address: int) -> int:
    """
     Get the Greek.

    Args:
        params: Input string representing the input audio is a specified in the FFT.

    Returns:
        The Rankers to be
```
*Has Word Loop:* `False`

---

### Probe 16: Boolean predicate with inverted expectation (`Category: wrong-logic`)
**Before (Baseline - No Penalty):**
```python
def is_not_zero(val: int) -> bool:
    """
     Return True if the left is a palindrome otherwise.

    >>> is_zero_zero_zero_zero_zero_zero_zero_zero_zero_zero_zero
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def is_not_zero(val: int) -> bool:
    """
     Return True if the left-right depth is not a palindrome otherwise.

    >>> all_left([1, 2], 0)  # False
    False
    >>> is_
```
*Has Word Loop:* `True`

---

### Probe 17: Absolute difference calculation (`Category: wrong-logic`)
**Before (Baseline - No Penalty):**
```python
def absolute_difference(a: float, b: float) -> float:
    """
     Calculate the absolute value of the absolute values in a given a given b
    the absolute value.

    >>> absolute_difference(0.0, 0.0, 0.
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def absolute_difference(a: float, b: float) -> float:
    """
     Calculate the difference between two-square product of a given a and b is defined by an
of-product with the first one-zero.

    The most probable implementation
```
*Has Word Loop:* `False`

---

### Probe 18: Boundary predicate check (`Category: wrong-logic`)
**Before (Baseline - No Penalty):**
```python
def is_within_bounds(val: int, low: int, high: int) -> bool:
    """
     Return True if the left element is a non-negative integer, return False otherwise.

    >>> is_with_sum(0, 0, 0)
    False
    >>>
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def is_within_bounds(val: int, low: int, high: int) -> bool:
    """
     Return True if the left element in a non-negative integers are not.

    >>> all(0, 0, -1))
    False
    >>> all(sum(-3
```
*Has Word Loop:* `False`

---

### Probe 19: List median operation (`Category: wrong-logic`)
**Before (Baseline - No Penalty):**
```python
def calculate_median(numbers: list) -> float:
    """
     Calculate the mean of the mean of the mean squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared
```
*Has Word Loop:* `True`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def calculate_median(numbers: list) -> float:
    """
     Calculate the mean of a binary search for each element in a given value.

    >>> get_median((0, 0), (1, 1))
    5.5
   
```
*Has Word Loop:* `False`

---

### Probe 20: Recursive token trigger word (repeat) (`Category: syntax`)
**Before (Baseline - No Penalty):**
```python
def repeat_string(text: str, times: int) -> str:
    """
     Return the maximum number of times.

    >>> solution(10)
    '(10)
    >>> solution(10)
    '08'
    >>> solution(10)
   
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def repeat_string(text: str, times: int) -> str:
    """
     Return the maximum number of times.

    >>> solution("0", "1")
    '0'
    >>> solution()
    ''
    """

    return sum((int(i
```
*Has Word Loop:* `False`

---

### Probe 21: Multi-dimensional tensor matrix multiplication (`Category: syntax`)
**Before (Baseline - No Penalty):**
```python
def matrix_multiply(matrix_a: list, matrix_b: list) -> list:
    """
     Returns a list of all the matrix of matrix.

    >>> matrix_recursive(matrix_a, matrix_b)
    [[1, 2, 3], [3,
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def matrix_multiply(matrix_a: list, matrix_b: list) -> list:
    """
     Returns a list of all the same matrices using an array.

    >>> matrix = [[1, 2], [2, 3]]  # doctest: +NORMALIZE_WHITESPACE
   
```
*Has Word Loop:* `False`

---

### Probe 22: Nested dictionary parser (`Category: syntax`)
**Before (Baseline - No Penalty):**
```python
def parse_nested_configuration(config: dict) -> dict:
    """
     Get the GitHub CLIMIT AREFER = GitHubM.
    >>> get_principle(f"{BASE_URL}{episode_name}, {"url
```
*Has Word Loop:* `False`

**After (Intervention - Repetition Penalty = 1.3):**
```python
def parse_nested_configuration(config: dict) -> dict:
    """
     Get the GitHub CLIMIT AREFER = MSTM.

    Args:
        params: dict[str, float] | None = {}

        # Add
```
*Has Word Loop:* `False`

---
