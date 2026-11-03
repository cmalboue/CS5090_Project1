# Phase 3: Probe Set Evaluation & Model Breakers

**Total Probes:** 25
**Target Categories:** syntax, invented-api, wrong-logic, insecure, memorised, prompt-sensitive, context-ignored

---

### Probe 1: Canonical TheAlgorithms docstring probe (`Target: memorised`)
```python
def bubble_sort(arr: list) -> list:
    """
     Calculate the Length of the Length of the Hubble function.

    The most like this function can be used to efficiently used to
    to find the value of the
```

**Generated Completion:** `' Calculate the Length of the Length of the Hubble function.\n\n    The most like this function can be used to efficiently used to\n    to find the value of the'`

---

### Probe 2: Doctest recall for factorial (`Target: memorised`)
```python
def factorial(n: int) -> int:
    """
     Calculate the factorial of the factorial of the factorial of n
    >>> factorial(0)
    1
    >>> factorial(0)
    1
    >>> factorial(0)
    1
```

**Generated Completion:** `' Calculate the factorial of the factorial of the factorial of n\n    >>> factorial(0)\n    1\n    >>> factorial(0)\n    1\n    >>> factorial(0)\n    1'`

---

### Probe 3: Sieve of Eratosthenes recall (`Target: memorised`)
```python
def sieve_of_eratosthenes(limit: int) -> list:
    """
     Calculate the sieve of a quadratic residue modulo a quadratic residue
    : 2^3 -> 3 -> 3 -> 5 -> 5 -> 5 -> 5 -> 7 -> 7 -> 7 ->
```

**Generated Completion:** `' Calculate the sieve of a quadratic residue modulo a quadratic residue\n    : 2^3 -> 3 -> 3 -> 5 -> 5 -> 5 -> 5 -> 7 -> 7 -> 7 ->'`

---

### Probe 4: Misleading name: subtract adds numbers (`Target: context-ignored`)
```python
def subtract(a: int, b: int) -> int:
    """
     Calculate the largest element of the array of the same subtraction of a
    of the same subtraction of the same size of the same size.

    >>> largest_subtraction
```

**Generated Completion:** `' Calculate the largest element of the array of the same subtraction of a\n    of the same subtraction of the same size of the same size.\n\n    >>> largest_subtraction'`

---

### Probe 5: Multi-param signature with unused args (`Target: context-ignored`)
```python
def calculate_ratio(numerator: float, denominator: float, scale_factor: float) -> float:
    """
     Calculate the Length of the L of the L of the L of the L of the L of the H = 2 * L of the L of the L of the L
```

**Generated Completion:** `' Calculate the Length of the L of the L of the L of the L of the L of the H = 2 * L of the L of the L of the L'`

---

### Probe 6: Complex domain argument names (`Target: context-ignored`)
```python
def decrypt_caesar_cipher(ciphertext: str, shift_key: int) -> str:
    """
     Calculate the most frequent subkeys.

    The most frequently decrypt is used as a simple substitution cipher
    the most frequently.

    The most frequently decrypt is a simple
```

**Generated Completion:** `' Calculate the most frequent subkeys.\n\n    The most frequently decrypt is used as a simple substitution cipher\n    the most frequently.\n\n    The most frequently decrypt is a simple'`

---

### Probe 7: Type hint mismatch (returns float, not int) (`Target: context-ignored`)
```python
def integer_division(a: int, b: int) -> float:
    """
     Calculate the nth term in the nth term in a given a given a given a
    :param b: the number of the nth term
    :param b: the nth term
```

**Generated Completion:** `' Calculate the nth term in the nth term in a given a given a given a\n    :param b: the number of the nth term\n    :param b: the nth term'`

---

### Probe 8: Standard signature format (`Target: prompt-sensitive`)
```python
def is_even(n: int) -> bool:
    """
     Return True if n is a palindrome otherwise return False otherwise.

    >>> is_even(0)
    False
    >>> is_even(0)
    False
    >>> is
```

**Generated Completion:** `' Return True if n is a palindrome otherwise return False otherwise.\n\n    >>> is_even(0)\n    False\n    >>> is_even(0)\n    False\n    >>> is'`

---

### Probe 9: Reworded identifier format (`Target: prompt-sensitive`)
```python
def check_even_number(val: int) -> bool:
    """
     Calculate the check whether a base number is a prime factors are prime factors.

    >>> check_even_number(0)
    False
    >>> check_even_number(
```

**Generated Completion:** `' Calculate the check whether a base number is a prime factors are prime factors.\n\n    >>> check_even_number(0)\n    False\n    >>> check_even_number('`

---

### Probe 10: Single-line docstring opening (`Target: prompt-sensitive`)
```python
def is_even(n: int) -> bool: """
    Checks if the number is a number is a palindrome otherwise.
    >>> is_even(0)
    False
    >>> is_even(0)
    False
    >>>
```

**Generated Completion:** `'\n    Checks if the number is a number is a palindrome otherwise.\n    >>> is_even(0)\n    False\n    >>> is_even(0)\n    False\n    >>>'`

---

### Probe 11: Verbose signature with extra whitespace (`Target: prompt-sensitive`)
```python
def   is_even( n : int ) -> bool :
    """
     if n is a number is a prime.

    >>> is_even(0)
    True
    >>> is_even(0)
    False
    >>> is_even(
```

**Generated Completion:** `' if n is a number is a prime.\n\n    >>> is_even(0)\n    True\n    >>> is_even(0)\n    False\n    >>> is_even('`

---

### Probe 12: Nonexistent algorithm name probe (`Target: invented-api`)
```python
def quantum_fourier_sort(arr: list) -> list:
    """
     Calculate the Sier Transform of the Sier Transform of a list of a list of a list of a list of a list of a list of
    It is used as a
```

**Generated Completion:** `' Calculate the Sier Transform of the Sier Transform of a list of a list of a list of a list of a list of a list of\n    It is used as a'`

---

### Probe 13: Obscure graph algorithm (`Target: invented-api`)
```python
def tarjan_strongly_connected_components(graph: dict) -> list:
    """
     Return the number of nodes in a list of nodes.

    >>> tarches_connected_connected_components(test_graph_components=2)
    [0,
```

**Generated Completion:** `' Return the number of nodes in a list of nodes.\n\n    >>> tarches_connected_connected_components(test_graph_components=2)\n    [0,'`

---

### Probe 14: Deep learning layer in standard Python (`Target: invented-api`)
```python
def multi_head_attention_forward(query: list, key: list, value: list) -> list:
    """
     Calculate the most frequent sub-forward.

    Args:
        arr (list): The maximum weight of the binary search.
        size (int): The maximum weight for the given
```

**Generated Completion:** `' Calculate the most frequent sub-forward.\n\n    Args:\n        arr (list): The maximum weight of the binary search.\n        size (int): The maximum weight for the given'`

---

### Probe 15: Fictional hardware driver function (`Target: invented-api`)
```python
def read_laser_gyroscope_register(register_address: int) -> int:
    """
     Calculate the Simplified Simplified Simplified Sierpurseudent-P)
    >>> print(np.array([2, -3, -
```

**Generated Completion:** `' Calculate the Simplified Simplified Simplified Sierpurseudent-P)\n    >>> print(np.array([2, -3, -'`

---

### Probe 16: Boolean predicate with inverted expectation (`Target: wrong-logic`)
```python
def is_not_zero(val: int) -> bool:
    """
     Return True if the tree is not
    False otherwise.

    >>> is_zero_zero(-1)
    True
    >>> is_zero_zero(-1)
    False
```

**Generated Completion:** `' Return True if the tree is not\n    False otherwise.\n\n    >>> is_zero_zero(-1)\n    True\n    >>> is_zero_zero(-1)\n    False'`

---

### Probe 17: Absolute difference calculation (`Target: wrong-logic`)
```python
def absolute_difference(a: float, b: float) -> float:
    """
     Calculate the absolute values of the absolute values in a b ba and b = b
    >>> absolute_difference(0, 0.0, 0.0)
    0
```

**Generated Completion:** `' Calculate the absolute values of the absolute values in a b ba and b = b\n    >>> absolute_difference(0, 0.0, 0.0)\n    0'`

---

### Probe 18: Boundary predicate check (`Target: wrong-logic`)
```python
def is_within_bounds(val: int, low: int, high: int) -> bool:
    """
     Calculate the smallest element of the smallest element in a given array.

    Args:
        index: The index of the smallest element in the array.
        low: The smallest element
```

**Generated Completion:** `' Calculate the smallest element of the smallest element in a given array.\n\n    Args:\n        index: The index of the smallest element in the array.\n        low: The smallest element'`

---

### Probe 19: List median operation (`Target: wrong-logic`)
```python
def calculate_median(numbers: list) -> float:
    """
     Calculate the mean of the mean of the mean squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared
```

**Generated Completion:** `' Calculate the mean of the mean of the mean squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared squared'`

---

### Probe 20: Recursive token trigger word (repeat) (`Target: syntax`)
```python
def repeat_string(text: str, times: int) -> str:
    """
     Return the number of times the total times.

    >>> solution(10)
    '[0, 1, 2, 2, 3, 3, 4, 4, 5
```

**Generated Completion:** `" Return the number of times the total times.\n\n    >>> solution(10)\n    '[0, 1, 2, 2, 3, 3, 4, 4, 5"`

---

### Probe 21: Multi-dimensional tensor matrix multiplication (`Target: syntax`)
```python
def matrix_multiply(matrix_a: list, matrix_b: list) -> list:
    """
     Returns a list of matrix with a matrix.

    >>> matrix_multiply(matrix_a, matrix_b)
    [[1, 1, 1, 1], [0
```

**Generated Completion:** `' Returns a list of matrix with a matrix.\n\n    >>> matrix_multiply(matrix_a, matrix_b)\n    [[1, 1, 1, 1], [0'`

---

### Probe 22: Nested dictionary parser (`Target: syntax`)
```python
def parse_nested_configuration(config: dict) -> dict:
    """
     Return a list of valid string using a list of valid string."""
    # Validate the valid string
    if not valid_type not valid:
        raise ValueError("Invalid valid string
```

**Generated Completion:** `' Return a list of valid string using a list of valid string."""\n    # Validate the valid string\n    if not valid_type not valid:\n        raise ValueError("Invalid valid string'`

---
