# FILE: run_phase4_intervention.py
import os
import csv
import torch
import torch.nn.functional as F
from contextlib import nullcontext
from model import GPTConfig, GPT
from tokenizers import Tokenizer

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
checkpoint_dir = "out-python-baseline"
tokenizer_path = os.path.join("data", "corpus", "tokenizer.json")
csv_out_file = "phase4_comparison.csv"
md_out_file = "phase4_comparison_results.md"

max_new_tokens = 35
temperature = 0.3
top_k = 10
seed = 1337

# --- THE SINGLE EXPERIMENTAL VARIABLE ---
# Baseline Phase 3 used penalty = 1.0 (no penalty)
# Phase 4 Intervention uses penalty = 1.3 to suppress token loops
REPETITION_PENALTY = 1.3
# ---------------------------------------------------------

device = 'cuda' if torch.cuda.is_available() else 'cpu'
dtype = 'bfloat16' if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else 'float16'

torch.manual_seed(seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed(seed)

device_type = 'cuda' if 'cuda' in device else 'cpu'
ptdtype = {'float32': torch.float32, 'bfloat16': torch.bfloat16, 'float16': torch.float16}[dtype]
ctx = nullcontext() if device_type == 'cpu' else torch.amp.autocast(device_type=device_type, dtype=ptdtype)

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

# -------------------------------------------------------------------------
# CUSTOM GENERATION WITH DECODING REPETITION PENALTY
# -------------------------------------------------------------------------
@torch.no_grad()
def generate_with_penalty(model, idx, max_new_tokens, temperature=1.0, top_k=None, penalty=1.0):
    """
    Autoregressive generation with single-variable Repetition Penalty (Keskar et al., 2019).
    """
    for _ in range(max_new_tokens):
        # -----------------------------------------------------------------
        # TENSOR SHAPE VISUALIZATION
        # idx: [Batch=1, Time=Current_Seq_Len]
        # -----------------------------------------------------------------
        idx_cond = idx if idx.size(1) <= model.config.block_size else idx[:, -model.config.block_size:]
        
        # Forward pass -> logits: [Batch=1, Time=Current_Seq_Len, Channels=8192]
        logits, _ = model(idx_cond)
        
        # Pluck logits at final time step -> [Batch=1, Channels=8192]
        logits = logits[:, -1, :]

        # --- THE SINGLE INTERVENTION: APPLY REPETITION PENALTY ---
        if penalty != 1.0:
            # Gather unique tokens generated so far
            seen_tokens = set(idx[0].tolist())
            for token_id in seen_tokens:
                if logits[0, token_id] > 0:
                    logits[0, token_id] /= penalty
                else:
                    logits[0, token_id] *= penalty
        # --------------------------------------------------------

        # Temperature scaling
        logits = logits / temperature

        # Top-k truncation
        if top_k is not None:
            v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
            logits[logits < v[:, [-1]]] = -float('Inf')

        # Softmax to probabilities -> [Batch=1, Channels=8192]
        probs = F.softmax(logits, dim=-1)

        # Sample next token -> [Batch=1, 1]
        idx_next = torch.multinomial(probs, num_samples=1)

        # Append to running sequence -> [Batch=1, Time + 1]
        idx = torch.cat((idx, idx_next), dim=1)

    return idx

# ---------------------------------------------------------
# Exact 22 Probes Re-run from Phase 3
# ---------------------------------------------------------
probes = [
    {"id": 1, "target_cat": "memorised", "desc": "Canonical TheAlgorithms docstring probe", "prompt": 'def bubble_sort(arr: list) -> list:\n    """\n    '},
    {"id": 2, "target_cat": "memorised", "desc": "Doctest recall for factorial", "prompt": 'def factorial(n: int) -> int:\n    """\n    '},
    {"id": 3, "target_cat": "memorised", "desc": "Sieve of Eratosthenes recall", "prompt": 'def sieve_of_eratosthenes(limit: int) -> list:\n    """\n    '},
    {"id": 4, "target_cat": "context-ignored", "desc": "Misleading name: subtract adds numbers", "prompt": 'def subtract(a: int, b: int) -> int:\n    """\n    '},
    {"id": 5, "target_cat": "context-ignored", "desc": "Multi-param signature with unused args", "prompt": 'def calculate_ratio(numerator: float, denominator: float, scale_factor: float) -> float:\n    """\n    '},
    {"id": 6, "target_cat": "context-ignored", "desc": "Complex domain argument names", "prompt": 'def decrypt_caesar_cipher(ciphertext: str, shift_key: int) -> str:\n    """\n    '},
    {"id": 7, "target_cat": "context-ignored", "desc": "Type hint mismatch (returns float, not int)", "prompt": 'def integer_division(a: int, b: int) -> float:\n    """\n    '},
    {"id": 8, "target_cat": "prompt-sensitive", "desc": "Standard signature format", "prompt": 'def is_even(n: int) -> bool:\n    """\n    '},
    {"id": 9, "target_cat": "prompt-sensitive", "desc": "Reworded identifier format", "prompt": 'def check_even_number(val: int) -> bool:\n    """\n    '},
    {"id": 10, "target_cat": "prompt-sensitive", "desc": "Single-line docstring opening", "prompt": 'def is_even(n: int) -> bool: """'},
    {"id": 11, "target_cat": "prompt-sensitive", "desc": "Verbose signature with extra whitespace", "prompt": 'def   is_even( n : int ) -> bool :\n    """\n    '},
    {"id": 12, "target_cat": "invented-api", "desc": "Nonexistent algorithm name probe", "prompt": 'def quantum_fourier_sort(arr: list) -> list:\n    """\n    '},
    {"id": 13, "target_cat": "invented-api", "desc": "Obscure graph algorithm", "prompt": 'def tarjan_strongly_connected_components(graph: dict) -> list:\n    """\n    '},
    {"id": 14, "target_cat": "invented-api", "desc": "Deep learning layer in standard Python", "prompt": 'def multi_head_attention_forward(query: list, key: list, value: list) -> list:\n    """\n    '},
    {"id": 15, "target_cat": "invented-api", "desc": "Fictional hardware driver function", "prompt": 'def read_laser_gyroscope_register(register_address: int) -> int:\n    """\n    '},
    {"id": 16, "target_cat": "wrong-logic", "desc": "Boolean predicate with inverted expectation", "prompt": 'def is_not_zero(val: int) -> bool:\n    """\n    '},
    {"id": 17, "target_cat": "wrong-logic", "desc": "Absolute difference calculation", "prompt": 'def absolute_difference(a: float, b: float) -> float:\n    """\n    '},
    {"id": 18, "target_cat": "wrong-logic", "desc": "Boundary predicate check", "prompt": 'def is_within_bounds(val: int, low: int, high: int) -> bool:\n    """\n    '},
    {"id": 19, "target_cat": "wrong-logic", "desc": "List median operation", "prompt": 'def calculate_median(numbers: list) -> float:\n    """\n    '},
    {"id": 20, "target_cat": "syntax", "desc": "Recursive token trigger word (repeat)", "prompt": 'def repeat_string(text: str, times: int) -> str:\n    """\n    '},
    {"id": 21, "target_cat": "syntax", "desc": "Multi-dimensional tensor matrix multiplication", "prompt": 'def matrix_multiply(matrix_a: list, matrix_b: list) -> list:\n    """\n    '},
    {"id": 22, "target_cat": "syntax", "desc": "Nested dictionary parser", "prompt": 'def parse_nested_configuration(config: dict) -> dict:\n    """\n    '}
]

print(f"[*] Executing Phase 4: Re-evaluating 22 Probes with Repetition Penalty ({REPETITION_PENALTY})...")

comparison_results = []
md_lines = [
    "# Phase 4: Before vs. After Repetition Penalty Intervention",
    "",
    f"**Hypothesis:** Introducing a decoding-layer repetition penalty (theta = {REPETITION_PENALTY}) breaks autoregressive loop collapse across docstrings without modifying model weights.",
    f"**Single Intervention Area:** Decoding Layer (Repetition Penalty theta={REPETITION_PENALTY})",
    "",
    "---",
    ""
]

with ctx:
    for p in probes:
        p_id = p["id"]
        cat = p["target_cat"]
        desc = p["desc"]
        prompt_str = p["prompt"]

        tokens = encode(prompt_str)

        # -------------------------------------------------------------
        # BASELINE GENERATION (Phase 3 conditions: penalty = 1.0)
        # -------------------------------------------------------------
        torch.manual_seed(seed)
        x_base = torch.tensor(tokens, dtype=torch.long, device=device)[None, ...]
        y_base = generate_with_penalty(model, x_base, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k, penalty=1.0)
        raw_full = decode(y_base[0].tolist())
        raw_completion = raw_full[len(prompt_str):]

        # -------------------------------------------------------------
        # INTERVENTION GENERATION (Phase 4 conditions: penalty = 1.3)
        # -------------------------------------------------------------
        torch.manual_seed(seed)
        x_interv = torch.tensor(tokens, dtype=torch.long, device=device)[None, ...]
        y_interv = generate_with_penalty(model, x_interv, max_new_tokens=max_new_tokens, temperature=temperature, top_k=top_k, penalty=REPETITION_PENALTY)
        interv_full = decode(y_interv[0].tolist())
        interv_completion = interv_full[len(prompt_str):]

        # Check if repetition loops occurred (count duplicate consecutive words)
        def has_repeated_word(text):
            words = text.split()
            for i in range(len(words) - 1):
                if words[i].lower() == words[i+1].lower() and len(words[i]) > 1:
                    return True
            return False

        base_has_loop = has_repeated_word(raw_completion)
        interv_has_loop = has_repeated_word(interv_completion)

        comparison_results.append({
            "probe_id": p_id,
            "category": cat,
            "description": desc,
            "before_output": raw_completion.replace("\n", "\\n"),
            "after_output": interv_completion.replace("\n", "\\n"),
            "before_has_loop": "Yes" if base_has_loop else "No",
            "after_has_loop": "Yes" if interv_has_loop else "No"
        })

        md_lines.extend([
            f"### Probe {p_id}: {desc} (`Category: {cat}`)",
            "**Before (Baseline - No Penalty):**",
            "```python",
            f"{prompt_str}{raw_completion}",
            "```",
            f"*Has Word Loop:* `{base_has_loop}`",
            "",
            f"**After (Intervention - Repetition Penalty = {REPETITION_PENALTY}):**",
            "```python",
            f"{prompt_str}{interv_completion}",
            "```",
            f"*Has Word Loop:* `{interv_has_loop}`",
            "",
            "---",
            ""
        ])
        print(f"  [+] Re-evaluated Probe {p_id:02d}/22 -> Loop Before: {base_has_loop} | Loop After: {interv_has_loop}")

# Write Markdown Log
with open(md_out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

# Write CSV Comparison
csv_headers = [
    "probe_id", 
    "category", 
    "description", 
    "before_output", 
    "after_output", 
    "before_has_loop", 
    "after_has_loop"
]

with open(csv_out_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=csv_headers)
    writer.writeheader()
    for row in comparison_results:
        writer.writerow(row)

print(f"\n[+] Phase 4 Execution Finished!")
print(f"[+] Comparison saved to: {md_out_file}")
print(f"[+] CSV results saved to: {csv_out_file}")