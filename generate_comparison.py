import os
import torch
from contextlib import nullcontext
from model import GPTConfig, GPT
from tokenizers import Tokenizer

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
prompt = "def "
baseline_dir = "out-python-baseline"
ablation_dir = "out-python-ablation"
out_file = "phase1_side_by_side_completion.md"
tokenizer_path = os.path.join("data", "corpus", "tokenizer.json")

num_samples = 3
max_new_tokens = 100
temperature = 0.8
top_k = 200
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

# Load your custom 8,192 BPE tokenizer
if not os.path.exists(tokenizer_path):
    raise FileNotFoundError(f"Cannot find custom tokenizer at: {tokenizer_path}")

tokenizer = Tokenizer.from_file(tokenizer_path)
encode = lambda s: tokenizer.encode(s).ids
decode = lambda l: tokenizer.decode(l)

start_ids = encode(prompt)
x = torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...]

def generate_samples_from_ckpt(ckpt_dir, n_samples):
    ckpt_path = os.path.join(ckpt_dir, 'ckpt.pt')
    if not os.path.exists(ckpt_path):
        return f"Error: Checkpoint missing in {ckpt_dir}", [f"[!] File not found: {ckpt_path}"]
    
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
    
    samples = []
    with torch.no_grad():
        with ctx:
            for _ in range(n_samples):
                y = model.generate(x, max_new_tokens, temperature=temperature, top_k=top_k)
                samples.append(decode(y[0].tolist()))
    
    n_head = checkpoint['model_args'].get('n_head', 'unknown')
    n_layer = checkpoint['model_args'].get('n_layer', 'unknown')
    n_embd = checkpoint['model_args'].get('n_embd', 'unknown')
    header_info = f"Checkpoint: {ckpt_dir} (n_layer={n_layer}, n_head={n_head}, n_embd={n_embd})"
    return header_info, samples

print(f"[*] Generating {num_samples} samples each using {tokenizer_path}...")

base_info, base_samples = generate_samples_from_ckpt(baseline_dir, num_samples)
abl_info, abl_samples = generate_samples_from_ckpt(ablation_dir, num_samples)

lines = [
    "# Phase 1: Side-by-Side Generation Comparison",
    "",
    "**Generation Settings:**",
    f"- Samples per model: `{num_samples}`",
    f"- Temperature: `{temperature}`",
    f"- Top-k: `{top_k}`",
    f"- Max new tokens: `{max_new_tokens}`",
    f"- Base Random Seed: `{seed}`",
    "",
    "---",
    "",
    "## Prompt",
    "```python",
    prompt.strip(),
    "```",
    "",
    "---",
    "",
    "## 1. Baseline Model Completions (6 Heads)",
    f"**{base_info}**",
    ""
]

for idx, sample in enumerate(base_samples, 1):
    lines.extend([
        f"### Sample {idx}",
        "```python",
        sample,
        "```",
        ""
    ])

lines.extend([
    "---",
    "",
    "## 2. Ablation Model Completions (1 Head)",
    f"**{abl_info}**",
    ""
])

for idx, sample in enumerate(abl_samples, 1):
    lines.extend([
        f"### Sample {idx}",
        "```python",
        sample,
        "```",
        ""
    ])

report_text = "\n".join(lines)

with open(out_file, "w", encoding="utf-8") as f:
    f.write(report_text)

print(f"\n[+] Successfully generated all samples without tokenizer mismatch!")
print(f"[+] Output saved to: {out_file}\n")
print(report_text)