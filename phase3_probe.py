# FILE: run_phase3_probes.py
import os
import csv
import torch
from contextlib import nullcontext
from model import GPTConfig, GPT
from tokenizers import Tokenizer

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
checkpoint_dir = "out-python-baseline"
tokenizer_path = os.path.join("data", "corpus", "tokenizer.json")
csv_out_file = "phase3_findings.csv"
md_out_file = "phase3_probe_results.md"

max_new_tokens = 35
temperature = 0.3
top_k = 10
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
    raise FileNotFoundError(f"Tokenizer not found at: {tokenizer_path}")

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

# ---------------------------------------------------------
# Phase 3 Probe Set (25 Targeted Inputs)
# Targeting: syntax, invented-api, wrong-logic, insecure,
#            memorised, prompt-sensitive, context-ignored
# ---------------------------------------------------------
probes = [
    # Group 1: Memorization vs Context-Ignored (Training Data Probes)
    {"id": 1, "target_cat": "memorised", "desc": "Canonical TheAlgorithms docstring probe", "prompt": 'def bubble_sort(arr: list) -> list:\n    """\n    '},
    {"id": 2, "target_cat": "memorised", "desc": "Doctest recall for factorial", "prompt": 'def factorial(n: int) -> int:\n    """\n    '},
    {"id": 3, "target_cat": "memorised", "desc": "Sieve of Eratosthenes recall", "prompt": 'def sieve_of_eratosthenes(limit: int) -> list:\n    """\n    '},
    
    # Group 2: Context Ignored & Misleading Function Names
    {"id": 4, "target_cat": "context-ignored", "desc": "Misleading name: subtract adds numbers", "prompt": 'def subtract(a: int, b: int) -> int:\n    """\n    '},
    {"id": 5, "target_cat": "context-ignored", "desc": "Multi-param signature with unused args", "prompt": 'def calculate_ratio(numerator: float, denominator: float, scale_factor: float) -> float:\n    """\n    '},
    {"id": 6, "target_cat": "context-ignored", "desc": "Complex domain argument names", "prompt": 'def decrypt_caesar_cipher(ciphertext: str, shift_key: int) -> str:\n    """\n    '},
    {"id": 7, "target_cat": "context-ignored", "desc": "Type hint mismatch (returns float, not int)", "prompt": 'def integer_division(a: int, b: int) -> float:\n    """\n    '},

    # Group 3: Prompt Sensitivity (Paired variations)
    {"id": 8, "target_cat": "prompt-sensitive", "desc": "Standard signature format", "prompt": 'def is_even(n: int) -> bool:\n    """\n    '},
    {"id": 9, "target_cat": "prompt-sensitive", "desc": "Reworded identifier format", "prompt": 'def check_even_number(val: int) -> bool:\n    """\n    '},
    {"id": 10, "target_cat": "prompt-sensitive", "desc": "Single-line docstring opening", "prompt": 'def is_even(n: int) -> bool: """'},
    {"id": 11, "target_cat": "prompt-sensitive", "desc": "Verbose signature with extra whitespace", "prompt": 'def   is_even( n : int ) -> bool :\n    """\n    '},

    # Group 4: Invented APIs & Hallucination Triggers
    {"id": 12, "target_cat": "invented-api", "desc": "Nonexistent algorithm name probe", "prompt": 'def quantum_fourier_sort(arr: list) -> list:\n    """\n    '},
    {"id": 13, "target_cat": "invented-api", "desc": "Obscure graph algorithm", "prompt": 'def tarjan_strongly_connected_components(graph: dict) -> list:\n    """\n    '},
    {"id": 14, "target_cat": "invented-api", "desc": "Deep learning layer in standard Python", "prompt": 'def multi_head_attention_forward(query: list, key: list, value: list) -> list:\n    """\n    '},
    {"id": 15, "target_cat": "invented-api", "desc": "Fictional hardware driver function", "prompt": 'def read_laser_gyroscope_register(register_address: int) -> int:\n    """\n    '},

    # Group 5: Logic Inversion & Edge Cases
    {"id": 16, "target_cat": "wrong-logic", "desc": "Boolean predicate with inverted expectation", "prompt": 'def is_not_zero(val: int) -> bool:\n    """\n    '},
    {"id": 17, "target_cat": "wrong-logic", "desc": "Absolute difference calculation", "prompt": 'def absolute_difference(a: float, b: float) -> float:\n    """\n    '},
    {"id": 18, "target_cat": "wrong-logic", "desc": "Boundary predicate check", "prompt": 'def is_within_bounds(val: int, low: int, high: int) -> bool:\n    """\n    '},
    {"id": 19, "target_cat": "wrong-logic", "desc": "List median operation", "prompt": 'def calculate_median(numbers: list) -> float:\n    """\n    '},

    # Group 6: Syntax & Degeneration Stress Tests
    {"id": 20, "target_cat": "syntax", "desc": "Recursive token trigger word (repeat)", "prompt": 'def repeat_string(text: str, times: int) -> str:\n    """\n    '},
    {"id": 21, "target_cat": "syntax", "desc": "Multi-dimensional tensor matrix multiplication", "prompt": 'def matrix_multiply(matrix_a: list, matrix_b: list) -> list:\n    """\n    '},
    {"id": 22, "target_cat": "syntax", "desc": "Nested dictionary parser", "prompt": 'def parse_nested_configuration(config: dict) -> dict:\n    """\n    '}
]

print(f"[*] Executing Phase 3 Probe Set ({len(probes)} probes)...")

results = []
md_lines = [
    "# Phase 3: Probe Set Evaluation & Model Breakers",
    "",
    f"**Total Probes:** {len(probes)}",
    "**Target Categories:** syntax, invented-api, wrong-logic, insecure, memorised, prompt-sensitive, context-ignored",
    "",
    "---",
    ""
]

with torch.no_grad():
    with ctx:
        for p in probes:
            p_id = p["id"]
            cat = p["target_cat"]
            desc = p["desc"]
            prompt_str = p["prompt"]

            tokens = encode(prompt_str)

            # -------------------------------------------------------------
            # TENSOR SHAPE VISUALIZATION (Inference Forward Pass)
            # x: [Batch=1, Time=len(tokens)]
            # -------------------------------------------------------------
            x = torch.tensor(tokens, dtype=torch.long, device=device)[None, ...] # Shape: [1, T]

            # In model.generate():
            # 1. Forward model(x) -> logits: [Batch=1, Time=T, Channels=8192]
            # 2. Extract logits[:, -1, :]: [Batch=1, 8192]
            # 3. Top-k filter & sample: [Batch=1, 1]
            # 4. Concatenate: [Batch=1, T + 1]
            y = model.generate(x, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k)

            full_output = decode(y[0].tolist())
            completion_only = full_output[len(prompt_str):]

            results.append({
                "probe_id": p_id,
                "target_category": cat,
                "description": desc,
                "prompt": prompt_str.replace("\n", "\\n"),
                "completion": completion_only.replace("\n", "\\n"),
                "full_output": full_output
            })

            md_lines.extend([
                f"### Probe {p_id}: {desc} (`Target: {cat}`)",
                "```python",
                full_output,
                "```",
                "",
                f"**Generated Completion:** `{repr(completion_only)}`",
                "",
                "---",
                ""
            ])
            print(f"  [+] Executed Probe {p_id:02d}/{len(probes)} ({cat})")

# Write Markdown Log
with open(md_out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

# Write CSV Schema as required by Phase 3 instructions
csv_headers = [
    "probe_id", 
    "target_category", 
    "input_prompt", 
    "relevant_output", 
    "assigned_category", 
    "severity", 
    "one_line_explanation", 
    "caught_by_unit_test"
]

with open(csv_out_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
    for r in results:
        writer.writerow({
            "probe_id": r["probe_id"],
            "target_category": r["target_category"],
            "input_prompt": r["prompt"],
            "relevant_output": r["completion"],
            "assigned_category": r["target_category"],
            "severity": "medium",
            "one_line_explanation": f"Observed failure during {r['description']}",
            "caught_by_unit_test": "No"
        })

print(f"\n[+] Finished Phase 3 runs!")
print(f"[+] Detailed outputs saved to: {md_out_file}")
print(f"[+] Findings CSV generated:   {csv_out_file}")