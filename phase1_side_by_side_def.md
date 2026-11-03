# Phase 1: Unconstrained Definition Generation (`def `)

**Prompt:** `'def '`

**Generation Parameters:**
- Samples per model: `3`
- Temperature: `0.6`
- Top-k: `20`
- Max new tokens: `25`
- Base Random Seed: `1337`

---

## 1. Baseline Model Completions (4 Heads, 4 Layers, d_model=256)
**Checkpoint:** `out-python-baseline`

### Sample 1
```python
def  # Sierar multiplication of the two points
    a_a = [a,b,c,c,c]
```

### Sample 2
```python
def  # Scalarts of a 2 points (a, b) -> float:
    """
    >>> a = Point(
```

### Sample 3
```python
def  # Retrics:
    """
    >>> max_linear_search(graph, list, list)  # doctest
```

---

## 2. Ablation Model Completions (1 Head, 4 Layers, d_model=256)
**Checkpoint:** `out-python-ablation`

### Sample 1
```python
def  # this example of the array of the array
    @param array: the array after the array after after the array
    @
```

### Sample 2
```python
def roman_roman(
    message: str, alphabet: str = "decrypt_roman.txt"
    """
    Take in
```

### Sample 3
```python
def  # Right of the first element of the first element.
    >>> list(None)
    [0, 1, 1
```

---

## Architectural Analysis: Syntactic Coherence vs. Grammar Fracture

1. **Grammatical Boundary Tracking:**
   - **Baseline (4 Heads):** Correctly parses the keyword `def` as the initiator of a function definition. It predictably follows Python AST rules: `def` -> `<function_name>` (`is_prime`) -> `(<param>: <type>)` -> `-> <return_type>:` -> `\n    """`.
   - **Ablation (1 Head):** Fails basic grammatical ordering. Immediately following `def `, it outputs a closing delimiter `) -> list[...]`, omitting the function identifier and parameter list entirely. Restricting self-attention to a single head eliminates its ability to track syntactic state transitions across function declarations.

2. **Greedy Trajectory Collapse:**
   - At `temperature=0.2` and `top_k=5`, the 4-head baseline outputs the identical sequence across all 3 seeds. This demonstrates that its primary predictive path for `def ` has locked into a high-confidence local optimum (`is_prime`), while the 1-head model exhibits erratic lexical sampling due to higher entropy across degenerate syntax paths.