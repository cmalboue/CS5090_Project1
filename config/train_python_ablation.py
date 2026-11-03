# Configuration for CS 5090 Project 1 Ablation Model (1 Head)
dataset = 'corpus'
out_dir = 'out-python-ablation'
eval_interval = 100
eval_iters = 50
log_interval = 10

# Force save at the 1600 sweet spot
always_save_checkpoint = True
wandb_log = False

# 4 layers, 1 head (Ablation), 256 embedding dimension, 512 context window
n_layer = 4
n_head = 1
n_embd = 256
block_size = 512
dropout = 0.0

# 8 * 4 = 32 sequences per optimizer step
batch_size = 8
gradient_accumulation_steps = 4

# --- EXACT SWEET SPOT REPRODUCTION ---
max_iters = 1600           # Stop the script exactly here
lr_decay_iters = 5000      # BUT keep the decay curve stretched across 5000 steps
learning_rate = 6e-4       
min_lr = 6e-5              
beta2 = 0.95               
warmup_iters = 250         # Keep the original 5000-step warmup scale        

# RTX 4060 natively accelerates bfloat16
dtype = 'bfloat16'
compile = False