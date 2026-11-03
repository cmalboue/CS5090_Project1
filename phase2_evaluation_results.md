# Phase 2 Evaluation: 20 Real Software Engineering Inputs

**Model:** Baseline (n_layer=4, n_head=4, n_embd=256, 1600 iterations)
**Chosen Software Engineering Task:** Python Docstring Generation

## Task Definition & Judgment Criteria
- **Accept as-is:** The generated docstring correctly describes the function intent and terminates cleanly.
- **Accept after editing:** The summary is mostly accurate, but requires trivial edits (e.g., closing `"""`, fixing minor grammar, or deleting trailing doctest loops).
- **Reject:** Hallucinates incorrect behavior, breaks syntax, or produces degenerate token loops.

## Summary Tally
| Outcome | Count |
| :--- | :--- |
| Accept as-is | 0 |
| Accept after editing | 5 |
| Reject | 15 |

---

## Detailed Results

### Input 1: is_even
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def is_even(n: int) -> bool:
    """
     Return True if n is a palindrome otherwise return False otherwise return False otherwise.

    >>> is_even(0)
    False
    >>> is_even(0)
    False
```

**Generated Docstring Completion:**
`' Return True if n is a palindrome otherwise return False otherwise return False otherwise.\n\n    >>> is_even(0)\n    False\n    >>> is_even(0)\n    False'`

**Notes / Edits needed:** Conflates parity checking with palindrome verification. Loops the phrase 'otherwise return False'. Doctest assertion is mathematically incorrect (claims 0 is not even).

---

### Input 2: is_positive
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def is_positive(n: int) -> bool:
    """
     input:
    Check if the number is negative or not a positive integer.

    >>> is_positive_positive(0)
    True
    >>> is_positive_positive_
```

**Generated Docstring Completion:**
`' input:\n    Check if the number is negative or not a positive integer.\n\n    >>> is_positive_positive(0)\n    True\n    >>> is_positive_positive_'`

**Notes / Edits needed:** Inverts the logical condition ('Check if the number is negative'). Hallucinates an invalid repetitive function identifier in the doctest ('is_positive_positive').

---

### Input 3: square
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def square(n: int) -> int:
    """
     Calculate the square square square square square square square.
    The square square square square is square.

    >>> square(2)
    2
    >>> square_square(2)
```

**Generated Docstring Completion:**
`' Calculate the square square square square square square square.\n    The square square square square is square.\n\n    >>> square(2)\n    2\n    >>> square_square(2)'`

**Notes / Edits needed:** Degenerate token collapse loop on the word 'square'. Doctest assertion is factually false (claims 2 squared is 2).

---

### Input 4: cube
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def cube(n: int) -> int:
    """
     Returns the smallest number of its left to the right.
    >>> solution(10)
    13
    >>> solution(10)
    15
    >>> solution(15)
    15
```

**Generated Docstring Completion:**
`' Returns the smallest number of its left to the right.\n    >>> solution(10)\n    13\n    >>> solution(10)\n    15\n    >>> solution(15)\n    15'`

**Notes / Edits needed:** Ignores the prompt context entirely. Hallucinates an invented API ('solution(10)') with arbitrary integer mappings.

---

### Input 5: add
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def add(a: int, b: int) -> int:
    """
     Find the start of a given a given b such that a given b such that a(a),
    a(x) = b(x)
    b = b *
```

**Generated Docstring Completion:**
`' Find the start of a given a given b such that a given b such that a(a),\n    a(x) = b(x)\n    b = b *'`

**Notes / Edits needed:** Stuttering loop ('a given a given b'). Generates pseudo-mathematical equations instead of explaining addition.

---

### Input 6: absolute_value
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def absolute_value(n: int) -> int:
    """
     Calculate the absolute value of the absolute value.
    The value of the absolute value is to the absolute value.
    It is the absolute value in the absolute value.
    The
```

**Generated Docstring Completion:**
`' Calculate the absolute value of the absolute value.\n    The value of the absolute value is to the absolute value.\n    It is the absolute value in the absolute value.\n    The'`

**Notes / Edits needed:** Autoregressive repetition loop. Continuously cycles the phrase 'absolute value' without functional description.

---

### Input 7: get_first
**Decision:** `Accept after editing`

**Full Prompt & Output:**
```python
def get_first_element(arr: list) -> int:
    """
     Return the first element in the array.
    >>> get_first_search(arr)
    0
    >>> get_first_search(arr)
    0
    >>> get
```

**Generated Docstring Completion:**
`' Return the first element in the array.\n    >>> get_first_search(arr)\n    0\n    >>> get_first_search(arr)\n    0\n    >>> get'`

**Notes / Edits needed:** The first line is 100% accurate: 'Return the first element in the array.' Edit: Delete lines 4-8 (unclosed hallucinated doctest) and close with triple quotes.

---

### Input 8: is_empty
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def is_empty(arr: list) -> bool:
    """
     if a list is a list of non-empty list of non-empty list,
    If the list is empty list is empty list, the list.
    """
    if
```

**Generated Docstring Completion:**
`' if a list is a list of non-empty list of non-empty list,\n    If the list is empty list is empty list, the list.\n    """\n    if'`

**Notes / Edits needed:** Emitted closing quotes, but the body is degenerate tautological word salad ('empty list is empty list').

---

### Input 9: reverse_string
**Decision:** `Accept after editing`

**Full Prompt & Output:**
```python
def reverse_string(s: str) -> str:
    """
     return a list of reverse order of the same time complexity

    >>> reverse_string(0)
    '1'
    >>> reverse_string(0)
    '1'
```

**Generated Docstring Completion:**
`" return a list of reverse order of the same time complexity\n\n    >>> reverse_string(0)\n    '1'\n    >>> reverse_string(0)\n    '1'"`

**Notes / Edits needed:** Captures the core semantic concept of reversing order. Edit: Change 'list' to 'string', fix doctest to pass a string (e.g. 'abc') instead of 0, and close with triple quotes.

---

### Input 10: find_max
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def find_max(arr: list) -> int:
    """
     if not arr is not None:
        return

    def find_max(arr: list[int], arr: list[int]) -> int:
        """
        >>> find
```

**Generated Docstring Completion:**
`' if not arr is not None:\n        return\n\n    def find_max(arr: list[int], arr: list[int]) -> int:\n        """\n        >>> find'`

**Notes / Edits needed:** Structural breakdown. Emits executable Python control flow and a nested function definition inside the docstring.

---

### Input 11: find_min
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def find_min(arr: list) -> int:
    """
     if a list of elements in the list of elements in the list.

    >>> find_min([1, 2, 3, 3, 4, 4, 4, 5
```

**Generated Docstring Completion:**
`' if a list of elements in the list of elements in the list.\n\n    >>> find_min([1, 2, 3, 3, 4, 4, 4, 5'`

**Notes / Edits needed:** Incomplete sentence fragment; unclosed list literal and unclosed doctest.

---

### Input 12: is_palindrome
**Decision:** `Accept after editing`

**Full Prompt & Output:**
```python
def is_palindrome(s: str) -> bool:
    """
     # Check if the tree is a palindrome otherwise return it is a palindrome otherwise.

    >>> is_palindrome(0)
    False
    >>> is_palindrome(1)
   
```

**Generated Docstring Completion:**
`' # Check if the tree is a palindrome otherwise return it is a palindrome otherwise.\n\n    >>> is_palindrome(0)\n    False\n    >>> is_palindrome(1)\n   '`

**Notes / Edits needed:** Correctly identifies palindrome verification and boolean return behavior. Edit: Remove '# ', replace domain-leaked token 'tree' with 'string', delete redundant 'otherwise' clause, and close with triple quotes.

---

### Input 13: is_sorted
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def is_sorted(arr: list) -> bool:
    """
     if the list is a list of integers are integers.

    >>> is_sorted_sorted_sorted_sorted_sorted_sorted_sorted_sorted_sorted_sorted
   
```

**Generated Docstring Completion:**
`' if the list is a list of integers are integers.\n\n    >>> is_sorted_sorted_sorted_sorted_sorted_sorted_sorted_sorted_sorted_sorted\n   '`

**Notes / Edits needed:** Autoregressive identifier stuttering ('is_sorted_sorted_sorted...').

---

### Input 14: count_vowels
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def count_vowels(s: str) -> int:
    """
     Calculate the number of substrings in a given string.

    >>> count_vowels("a")
    0
    >>> count_vowels("a")
    0
    >>> count_
```

**Generated Docstring Completion:**
`' Calculate the number of substrings in a given string.\n\n    >>> count_vowels("a")\n    0\n    >>> count_vowels("a")\n    0\n    >>> count_'`

**Notes / Edits needed:** Semantic drift (describes 'substrings' instead of vowels). Doctest assertion is factually wrong ('a' is a vowel, count should be 1).

---

### Input 15: factorial
**Decision:** `Accept after editing`

**Full Prompt & Output:**
```python
def factorial(n: int) -> int:
    """
     Calculate the factorial of the factorial of the factorial of [1,1]
    >>> factorial(0)
    1
    >>> factorial(0)
    1
    >>> factorial(
```

**Generated Docstring Completion:**
`' Calculate the factorial of the factorial of the factorial of [1,1]\n    >>> factorial(0)\n    1\n    >>> factorial(0)\n    1\n    >>> factorial('`

**Notes / Edits needed:** Synthesizes a mathematically correct doctest: factorial(0) equals 1. Edit: Change repetitive first line to 'Calculate the factorial of integer n.', delete duplicate doctest line, and close with triple quotes.

---

### Input 16: fibonacci
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def fibonacci(n: int) -> int:
    """
     Calculate the fibonacci number of digits in the Fibonacci number.

    >>> fibonacci(0)
    1
    >>> fibonacci(100)
    5
    >>> fibonacci(100)
    10
```

**Generated Docstring Completion:**
`' Calculate the fibonacci number of digits in the Fibonacci number.\n\n    >>> fibonacci(0)\n    1\n    >>> fibonacci(100)\n    5\n    >>> fibonacci(100)\n    10'`

**Notes / Edits needed:** Factual hallucination in doctest numbers (fibonacci(100) does not evaluate to 5 or 10).

---

### Input 17: linear_search
**Decision:** `Accept after editing`

**Full Prompt & Output:**
```python
def linear_search(arr: list, target: int) -> int:
    """
     Calculate the LSTMSTMSTMSTM.

    Args:
        arr (int): The input array.
        target (int): The target index of the target
```

**Generated Docstring Completion:**
`' Calculate the LSTMSTMSTMSTM.\n\n    Args:\n        arr (int): The input array.\n        target (int): The target index of the target'`

**Notes / Edits needed:** Provides a usable Google-style docstring template, correctly extracting both parameters ('arr' and 'target') from the signature. Edit: Replace top line ('Calculate the LSTM...') with 'Search for target in array.', fix type annotation for arr to (list), and close with triple quotes.

---

### Input 18: binary_search
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def binary_search(arr: list, target: int) -> int:
    """
     Calculate the binary search tree.

    >>> binary_search(0, 0, 0, 0)
    0
    >>> binary_search(0, 0, 0, 0
```

**Generated Docstring Completion:**
`' Calculate the binary search tree.\n\n    >>> binary_search(0, 0, 0, 0)\n    0\n    >>> binary_search(0, 0, 0, 0'`

**Notes / Edits needed:** Conflates binary search with binary search trees (BST). Hallucinates 4 arguments for a 2-parameter function.

---

### Input 19: bubble_sort
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def bubble_sort(arr: list) -> list:
    """
     Calculate the Hubble function of the hubble list of the hubble list using the Bubble list.

    The hubble function can be used for the
    the same as
```

**Generated Docstring Completion:**
`' Calculate the Hubble function of the hubble list of the hubble list using the Bubble list.\n\n    The hubble function can be used for the\n    the same as'`

**Notes / Edits needed:** Sub-word BPE token confusion ('Bubble' corrupted into 'Hubble'). Repetitive phrasing without describing sorting logic.

---

### Input 20: clamp
**Decision:** `Reject`

**Full Prompt & Output:**
```python
def clamp(val: float, min_val: float, max_val: float) -> float:
    """
     Calculate the Sherman's algorithm for a given a given max_val.

    Args:
        point: The list of the item.
        point: The point.
       
```

**Generated Docstring Completion:**
`" Calculate the Sherman's algorithm for a given a given max_val.\n\n    Args:\n        point: The list of the item.\n        point: The point.\n       "`

**Notes / Edits needed:** Hallucinates an invented algorithm name ('Sherman's algorithm') and parameters unrelated to the function signature.