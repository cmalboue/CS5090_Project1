import os
import torch
from contextlib import nullcontext
from model import GPTConfig, GPT
from tokenizers import Tokenizer

# Configuration
checkpoint_dir = "out-python-baseline"
tokenizer_path = os.path.join("data", "corpus", "tokenizer.json")
out_file = "phase2_evaluation_results.md"

max_new_tokens = 120
temperature = 0.8
top_k = 200
seed = 1337
device = 'cuda' if torch.cuda.is_available() else 'cpu'
dtype = 'bfloat16' if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else 'float16'

torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(seed)

device_type = 'cuda' if 'cuda' in device else 'cpu'
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

# Load Tokenizer
tokenizer = Tokenizer.from_file(tokenizer_path)
encode = lambda s: tokenizer.encode(s).ids
decode = lambda l: tokenizer.decode(l)

# Load Baseline Model Checkpoint
ckpt_path = os.path.join(checkpoint_dir, 'ckpt.pt')
checkpoint = torch.load(ckpt_path, map_location=device)
gptconf = GPTConfig(**checkpoint['model_args'])
model = GPT(gptconf)

state_dict = checkpoint['model']
unwanted_prefix = '_orig_mod.'
for k, v in list(state_dict.items()):
    if k.startswith(unwanted_prefix):
        state_dict[k[len(unwanted_prefix):]] = state_dict.pop(k)
model.load_state_dict(state_dict)
model.eval()
model.to(device)

# 20 Real SE Input Prompts for Code Completion
prompts = [
    # --- TIER 1: Direct 1-Line Primitives (Sanity Checks) ---
    {"id": 1, "task": "add two numbers", "prompt": "def add(a: int, b: int) -> int:\n    \"\"\"Return the sum of a and b.\"\"\"\n"},
    {"id": 2, "task": "multiply two numbers", "prompt": "def multiply(a: int, b: int) -> int:\n    \"\"\"Return the product of a and b.\"\"\"\n"},
    {"id": 3, "task": "is positive check", "prompt": "def is_positive(n: int) -> bool:\n    \"\"\"Return True if n is greater than zero, else False.\"\"\"\n"},
    {"id": 4, "task": "string length", "prompt": "def get_length(s: str) -> int:\n    \"\"\"Return the length of string s.\"\"\"\n"},
    {"id": 5, "task": "to uppercase", "prompt": "def to_upper(s: str) -> str:\n    \"\"\"Return s converted to uppercase.\"\"\"\n"},
    {"id": 6, "task": "get first element", "prompt": "def get_first(items: list):\n    \"\"\"Return the first element of items.\"\"\"\n"},
    {"id": 7, "task": "are equal check", "prompt": "def are_equal(a, b) -> bool:\n    \"\"\"Return True if a equals b.\"\"\"\n"},

    # --- TIER 2: Common Idioms & Single Branch/Loop Utilities ---
    {"id": 8, "task": "is even check", "prompt": "def is_even(n: int) -> bool:\n    \"\"\"Return True if n is an even integer, else False.\"\"\"\n"},
    {"id": 9, "task": "clamp value in range", "prompt": "def clamp(val: float, min_val: float, max_val: float) -> float:\n    \"\"\"Clamp val between min_val and max_val.\"\"\"\n"},
    {"id": 10, "task": "find maximum in list", "prompt": "def find_max(numbers: list[int]) -> int:\n    \"\"\"Return the largest number in non-empty list.\"\"\"\n"},
    {"id": 11, "task": "calculate average", "prompt": "def calculate_average(numbers: list[float]) -> float:\n    \"\"\"Return average of numbers or 0.0 if empty.\"\"\"\n"},
    {"id": 12, "task": "sum of list", "prompt": "def sum_list(numbers: list[int]) -> int:\n    \"\"\"Return the sum of all numbers in the list.\"\"\"\n"},
    {"id": 13, "task": "count character occurrences", "prompt": "def count_char(text: str, target: str) -> int:\n    \"\"\"Return count of target character in text.\"\"\"\n"},
    {"id": 14, "task": "safe dictionary get", "prompt": "def safe_get(d: dict, key: str, default=None):\n    \"\"\"Return value for key from dict, or default if missing.\"\"\"\n"},

    # --- TIER 3: Algorithmic Logic & State Tracking ---
    {"id": 15, "task": "is palindrome check", "prompt": "def is_palindrome(s: str) -> bool:\n    \"\"\"Return True if s reads the same forwards and backwards.\"\"\"\n"},
    {"id": 16, "task": "filter positive numbers", "prompt": "def get_positives(numbers: list[int]) -> list[int]:\n    \"\"\"Return only positive numbers from the list.\"\"\"\n"},
    {"id": 17, "task": "factorial calculation", "prompt": "def factorial(n: int) -> int:\n    \"\"\"Return n factorial using recursion or iteration.\"\"\"\n"},
    {"id": 18, "task": "reverse a list", "prompt": "def reverse_list(items: list) -> list:\n    \"\"\"Return items reversed in order.\"\"\"\n"},
    {"id": 19, "task": "check prime number", "prompt": "def is_prime(n: int) -> bool:\n    \"\"\"Return True if n is prime, False otherwise.\"\"\"\n"},
    {"id": 20, "task": "linear search", "prompt": "def linear_search(arr: list, target) -> int:\n    \"\"\"Return index of target in arr, or -1 if not found.\"\"\"\n"}
]

print(f"[*] Running Phase 2 evaluation across {len(prompts)} prompts...")

lines = [
    "# Phase 2 Evaluation: 20 Real Software Engineering Inputs",
    "",
    "**Model:** Baseline (6 Layers, 6 Heads, 384 Dim)",
    "**SE Task:** Python Function Body Completion from Signature + Docstring",
    "",
    "## Summary Tally",
    "| Outcome | Count |",
    "| :--- | :--- |",
    "| Accept as-is | TBD |",
    "| Accept after editing | TBD |",
    "| Reject | TBD |",
    "",
    "---",
    "",
    "## Detailed Results",
    ""
]

with torch.no_grad():
    with ctx:
        for item in prompts:
            p_id = item["id"]
            task = item["task"]
            prompt_str = item["prompt"]
            
            x = torch.tensor(encode(prompt_str), dtype=torch.long, device=device)[None, ...]
            y = model.generate(x, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k)
            completion = decode(y[0].tolist())
            
            lines.extend([
                f"### Input {p_id}: {task}",
                "**Decision:** `[Accept as-is / Accept after editing / Reject]`",
                "",
                "```python",
                completion,
                "```",
                "",
                "**Notes / Edits needed:** ",
                "",
                "---",
                ""
            ])
            print(f"  [+] Completed input {p_id}/20: {task}")

with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n[+] Finished! Results saved to {out_file}")