# FILE: run_phase2_eval.py
import os
import torch
from contextlib import nullcontext
from model import GPTConfig, GPT
from tokenizers import Tokenizer

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
checkpoint_dir = "out-python-baseline"
tokenizer_path = os.path.join("data", "corpus", "tokenizer.json")
out_file = "phase2_evaluation_results.md"

max_new_tokens = 35  # Sufficient budget for 1-2 sentence description + closing quotes
temperature = 0.3    # Controlled sampling to avoid token collapse while allowing variety
top_k = 10           # Top-k candidate filtering
seed = 1337

device = 'cuda' if torch.cuda.is_available() else 'cpu'
dtype = 'bfloat16' if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else 'float16'
# ---------------------------------------------------------

torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(seed)

device_type = 'cuda' if 'cuda' in device else 'cpu'
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

if not os.path.exists(tokenizer_path):
    raise FileNotFoundError(f"Tokenizer not found at {tokenizer_path}")

tokenizer = Tokenizer.from_file(tokenizer_path)
encode = lambda s: tokenizer.encode(s).ids
decode = lambda l: tokenizer.decode(l)

checkpoint = torch.load(os.path.join(checkpoint_dir, 'ckpt.pt'), map_location=device, weights_only=False)
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

# -----------------------------------------------------------------------------------
# Phase 2: Exactly 20 Real Software Engineering Inputs for DOCSTRING GENERATION
# Sourced from: TheAlgorithms/Python, Trekhleb/learn-python, and Faif/python-patterns
# -----------------------------------------------------------------------------------
prompts = [
    # Tier 1: Canonical Math & Boolean Predicates (High expectation of working intent)
    {"id": 1, "task": "is_even", "signature": "def is_even(n: int) -> bool:"},
    {"id": 2, "task": "is_positive", "signature": "def is_positive(n: int) -> bool:"},
    {"id": 3, "task": "square", "signature": "def square(n: int) -> int:"},
    {"id": 4, "task": "cube", "signature": "def cube(n: int) -> int:"},
    {"id": 5, "task": "add", "signature": "def add(a: int, b: int) -> int:"},
    {"id": 6, "task": "absolute_value", "signature": "def absolute_value(n: int) -> int:"},

    # Tier 2: Sequence & Collection Operations (List, Array, String manipulation)
    {"id": 7, "task": "get_first", "signature": "def get_first_element(arr: list) -> int:"},
    {"id": 8, "task": "is_empty", "signature": "def is_empty(arr: list) -> bool:"},
    {"id": 9, "task": "reverse_string", "signature": "def reverse_string(s: str) -> str:"},
    {"id": 10, "task": "find_max", "signature": "def find_max(arr: list) -> int:"},
    {"id": 11, "task": "find_min", "signature": "def find_min(arr: list) -> int:"},
    {"id": 12, "task": "is_palindrome", "signature": "def is_palindrome(s: str) -> bool:"},
    {"id": 13, "task": "is_sorted", "signature": "def is_sorted(arr: list) -> bool:"},
    {"id": 14, "task": "count_vowels", "signature": "def count_vowels(s: str) -> int:"},

    # Tier 3: Classic Algorithms & System Utilities (Complex logic and domain concepts)
    {"id": 15, "task": "factorial", "signature": "def factorial(n: int) -> int:"},
    {"id": 16, "task": "fibonacci", "signature": "def fibonacci(n: int) -> int:"},
    {"id": 17, "task": "linear_search", "signature": "def linear_search(arr: list, target: int) -> int:"},
    {"id": 18, "task": "binary_search", "signature": "def binary_search(arr: list, target: int) -> int:"},
    {"id": 19, "task": "bubble_sort", "signature": "def bubble_sort(arr: list) -> list:"},
    {"id": 20, "task": "clamp", "signature": "def clamp(val: float, min_val: float, max_val: float) -> float:"}
]

lines = [
    "# Phase 2 Evaluation: 20 Real Software Engineering Inputs",
    "",
    "**Model:** Baseline (n_layer=4, n_head=4, n_embd=256, 1600 iterations)",
    "**Chosen Software Engineering Task:** Python Docstring Generation",
    "",
    "## Task Definition & Judgment Criteria",
    "- **Accept as-is:** The generated docstring correctly describes the function intent and terminates cleanly.",
    "- **Accept after editing:** The summary is mostly accurate, but requires trivial edits (e.g., closing `\"\"\"`, fixing minor grammar, or deleting trailing doctest loops).",
    "- **Reject:** Hallucinates incorrect behavior, breaks syntax, or produces degenerate token loops.",
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

print(f"[*] Starting Phase 2 Evaluation: Docstring Generation across {len(prompts)} inputs...")

with torch.no_grad():
    with ctx:
        for item in prompts:
            p_id = item["id"]
            task = item["task"]
            sig = item["signature"]
            
            # Format prompt strictly: Signature -> newline -> 4 spaces -> opening quotes -> newline -> 4 spaces
            prompt_str = f'{sig}\n    """\n    '

            tokens = encode(prompt_str)

            # -------------------------------------------------------------------------
            # TENSOR SHAPE VISUALIZATION (nanoGPT forward pass during inference)
            # x: [Batch=1, Time=len(tokens)]
            # -------------------------------------------------------------------------
            x = torch.tensor(tokens, dtype=torch.long, device=device)[None, ...] # Shape: [1, T]

            # In model.generate():
            # 1. Forward model(x) -> logits: [Batch=1, Time=T, Channels=vocab_size (8192)]
            # 2. Slice last token -> logits[:, -1, :]: [Batch=1, Channels=8192]
            # 3. Top-k filter & sample token: [Batch=1, 1]
            # 4. Concatenate: x = torch.cat((x, idx_next), dim=1) -> [Batch=1, T + 1]
            y = model.generate(x, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k) # Shape: [1, T + max_new_tokens]

            full_output = decode(y[0].tolist())
            completion_only = full_output[len(prompt_str):]

            lines.extend([
                f"### Input {p_id}: {task}",
                "**Decision:** `[Accept as-is / Accept after editing / Reject]`",
                "",
                "**Full Prompt & Output:**",
                "```python",
                full_output,
                "```",
                "",
                "**Generated Docstring Completion:**",
                f"`{repr(completion_only)}`",
                "",
                "**Notes / Edits needed:** ",
                "",
                "---",
                ""
            ])
            print(f"  [+] Completed Input {p_id:02d}/20: {task}")

with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"\n[+] Finished! Results successfully written to: {out_file}")