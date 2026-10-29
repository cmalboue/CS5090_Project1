import os
import ast
import hashlib
import pickle
import numpy as np
from pathlib import Path
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders

# --- 1. CONFIGURATION ---
RAW_DATA_DIR = Path("raw_data")
VOCAB_SIZE = 8192
TRAIN_SPLIT_RATIO = 0.90
SEED = 1337

np.random.seed(SEED)

def harvest_and_clean_code(root_dir: Path):
    """
    Crawls raw code directories, eliminates duplicate files via SHA-256,
    and discards any files that fail Python AST parsing.
    """
    seen_hashes = set()
    valid_documents = []
    total_found = 0
    syntax_errors = 0

    print(f"Crawling {root_dir.resolve()} for Python (.py) files...")
    
    for filepath in root_dir.rglob("*.py"):
        total_found += 1
        try:
            content = filepath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        # Skip empty files
        if not content.strip():
            continue

        # Deduplicate using SHA-256
        file_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        if file_hash in seen_hashes:
            continue
        seen_hashes.add(file_hash)

        # Syntax verification: drop corrupted or invalid Python files
        try:
            ast.parse(content)
        except SyntaxError:
            syntax_errors += 1
            continue

        valid_documents.append(content)

    print(f"Discovered: {total_found} files")
    print(f"Syntax rejections: {syntax_errors} files")
    print(f"Clean, unique documents retained: {len(valid_documents)}")
    return valid_documents

# --- 2. HARVEST & SPLIT ---
docs = harvest_and_clean_code(RAW_DATA_DIR)
assert len(docs) > 0, "No valid Python files were found! Check your raw directory paths."

# Shuffle documents deterministically before splitting
np.random.shuffle(docs)

split_idx = int(len(docs) * TRAIN_SPLIT_RATIO)
train_docs = docs[:split_idx]
val_docs = docs[split_idx:]

print(f"Split: {len(train_docs)} train docs | {len(val_docs)} val docs")

# --- 3. TRAIN BYTE-LEVEL BPE TOKENIZER (TRAIN SPLIT ONLY) ---
print(f"Training Byte-Level BPE Tokenizer (vocab_size={VOCAB_SIZE})...")

tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
tokenizer.decoder = decoders.ByteLevel()

trainer = trainers.BpeTrainer(
    vocab_size=VOCAB_SIZE,
    special_tokens=["<|endoftext|>"],
    show_progress=True,
    initial_alphabet=pre_tokenizers.ByteLevel.alphabet()
)

# Train ONLY on the training split to satisfy project constraints
tokenizer.train_from_iterator(train_docs, trainer=trainer)
tokenizer.save("tokenizer.json")

eos_token_id = tokenizer.token_to_id("<|endoftext|>")
actual_vocab_size = tokenizer.get_vocab_size()
print(f"Tokenizer trained successfully! Effective vocab size: {actual_vocab_size}")

# --- 4. ENCODE TO BINARY (UINT16) ---
def encode_docs_to_bin(documents, output_bin_path: Path):
    print(f"Encoding {len(documents)} documents to {output_bin_path.name}...")
    token_ids = []
    
    for doc in documents:
        # Delimit documents with <|endoftext|>
        encoded = tokenizer.encode(doc).ids
        token_ids.extend(encoded)
        token_ids.append(eos_token_id)
        
    arr = np.array(token_ids, dtype=np.uint16)
    arr.tofile(output_bin_path)
    print(f"Saved {output_bin_path.name}: {len(arr):,} tokens ({os.path.getsize(output_bin_path) / (1024 * 1024):.2f} MB)")
    return len(arr)

train_token_count = encode_docs_to_bin(train_docs, Path("train.bin"))
val_token_count = encode_docs_to_bin(val_docs, Path("val.bin"))

# --- 5. SAVE METADATA FOR nanoGPT ---
meta = {
    'vocab_size': actual_vocab_size,
    'tokenizer_type': 'byte_bpe_custom',
    'eos_token_id': eos_token_id,
    'train_tokens': train_token_count,
    'val_tokens': val_token_count
}

with open("meta.pkl", "wb") as f:
    pickle.dump(meta, f)

print("\n--- Phase 1 Preprocessing Complete ---")
print(f"Total tokens generated: {train_token_count + val_token_count:,}")
print("Generated files: train.bin, val.bin, meta.pkl, tokenizer.json")