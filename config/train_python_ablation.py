# Configuration for CS 5090 Project 1 Baseline Model
# Directory where train.bin and val.bin live
dataset = 'corpus'

# Output directory for saving model checkpoints and training logs
out_dir = 'out-python-baseline'
eval_interval = 100
eval_iters = 50
log_interval = 10

# We don't save every step to save SSD space, but we save the best checkpoint on validation loss
always_save_checkpoint = False

# WandB logging (disabled by default, clean terminal logging)
wandb_log = False

# --- ARCHITECTURE SPECIFICATION (Matching Project 1 Baseline) ---
# 6 layers, 6 heads, 384 embedding dimension, 512 context window
n_layer = 6
n_head = 1 	# changed from 6 ABLATION
n_embd = 384
block_size = 512
dropout = 0.0

# --- BATCH SIZING & HARDWARE TUNING (Optimized for RTX 4060 8GB VRAM) ---
# Effective batch size = batch_size * gradient_accumulation_steps
# 8 * 4 = 32 sequences per optimizer step = 32 * 512 = 16,384 tokens/step
batch_size = 8
gradient_accumulation_steps = 4

# --- TRAINING SCHEDULE & OPTIMIZER ---
max_iters = 1000           # ~16.4M tokens seen total (~14 epochs over corpus)
lr_decay_iters = 1000      # Match max_iters for cosine decay
learning_rate = 6e-4       # Standard learning rate for ~10M param models
min_lr = 6e-5              # Typically learning_rate / 10
beta2 = 0.95               # Default for nanoGPT small models
warmup_iters = 150         # Gradual warmup to stabilize early gradients

# --- HARDWARE PRECISION & WINDOWS SETTINGS ---
# RTX 4060 natively accelerates bfloat16
dtype = 'bfloat16'
# compile = True relies on Triton/MSVC C++ build tools which is brittle on native Windows; keep False
compile = False