import re
import os
import matplotlib.pyplot as plt

def read_log_file(filepath):
    if not os.path.exists(filepath):
        print(f"[!] Error: '{filepath}' does not exist.")
        return ""
    
    # PowerShell defaults to utf-16 le when redirecting stdout with '>'
    for enc in ["utf-16", "utf-8", "cp1252"]:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
                if "step" in content:
                    return content
        except (UnicodeError, UnicodeDecodeError):
            continue
    return ""

def extract_losses(filepath):
    content = read_log_file(filepath)
    if not content:
        print(f"[!] Could not read valid text from '{filepath}'.")
        return [], [], []

    # Strip ANSI color codes if present
    content = re.sub(r"\x1b\[[0-9;]*[mK]", "", content)

    # Regex matches: step <digits>: train loss <float>, val loss <float>
    pattern = re.compile(
        r"step\s+(\d+)\s*:\s*train\s+loss\s+([0-9.]+)\s*,\s*val\s+loss\s+([0-9.]+)",
        re.IGNORECASE
    )

    steps, train_losses, val_losses = [], [], []
    for match in pattern.finditer(content):
        steps.append(int(match.group(1)))
        train_losses.append(float(match.group(2)))
        val_losses.append(float(match.group(3)))

    print(f"[*] Parsed {len(steps)} points from '{filepath}'.")
    return steps, train_losses, val_losses

base_file = "baseline_run.log"
abl_file = "baseline_run_ablation.log"

steps_base, tr_base, val_base = extract_losses(base_file)
steps_abl, tr_abl, val_abl = extract_losses(abl_file)

if not steps_base or not steps_abl:
    print("[!] Parser still found 0 points. Inspecting the first matching line directly:")
    content = read_log_file(base_file)
    for line in content.splitlines():
        if "val loss" in line:
            print(f"Sample raw line: {repr(line)}")
            break
    exit(1)

plt.figure(figsize=(9, 5.5), dpi=150)
plt.plot(steps_base, val_base, label="Baseline (6 Heads) - Val", color="#1f77b4", marker="o", linewidth=2)
plt.plot(steps_abl, val_abl, label="Ablation (1 Head) - Val", color="#d62728", marker="s", linewidth=2)
plt.plot(steps_base, tr_base, label="Baseline (6 Heads) - Train", color="#1f77b4", linestyle="--", alpha=0.5)
plt.plot(steps_abl, tr_abl, label="Ablation (1 Head) - Train", color="#d62728", linestyle="--", alpha=0.5)

plt.title("NanoGPT: Baseline (6 Heads) vs Ablation (1 Head)", fontsize=12, fontweight="bold")
plt.xlabel("Step", fontsize=10)
plt.ylabel("Cross-Entropy Loss", fontsize=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend(frameon=True)
plt.tight_layout()

out_file = "val_loss_comparison.png"
plt.savefig(out_file)
print(f"[+] Saved plot directly to '{out_file}'")