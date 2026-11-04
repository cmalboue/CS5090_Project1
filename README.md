<hr>

# CS 5090 Project 1: Build & Evaluate a Small Code Language Model

**Course:** CS 5090 - Software Engineering with Generative AI <br>
**Author:** Charlotte Malbouef <br>
**Institution:** Michigan Technological University  <br>
**Repository:** https://github.com/cmalboue/CS5090_Project1.git <br>

<hr>

## 1. Project Additions vs. Base nanoGPT

This repository builds upon Andrej Karpathy's `nanoGPT`. Below is the explicit file map distinguishing what was added for Project 1 from the original repository:

### Added & Project-Specific Files
*   **Documentation & Logs:**
    *   `baseline_run.log` — Training stdout log for the 4-head baseline (1,600 steps).
    *   `baseline_run_ablation.log` — Training stdout log for the 1-head ablation (1,600 steps).
    *   `val_loss_comparison.png` — Validation and training cross-entropy loss comparison curves.
    *   `plot_loss.py` — Log extraction and visualization script.
*   **Configurations (`config/`):**
    *   `config/train_python.py` — Baseline 4-head model configuration (`n_layer=4, n_head=4, n_embd=256`).
    *   `config/train_python_ablation.py` — Ablated 1-head model configuration (`n_layer=4, n_head=1, n_embd=256`).
*   **Data Preparation (`data/corpus/`):**
    *   `data/corpus/prepare.py` — Scraping pipeline: deduplication via SHA-256, AST syntax validation, 90/10 train-test split, and custom BPE training.
    *   `data/corpus/tokenizer.json` — Trained Byte-Level BPE tokenizer (`vocab_size=8192`).
    *   `data/corpus/meta.pkl` — Corpus token statistics and configuration metadata.
    *   `data/corpus/train.bin`, `data/corpus/val.bin` — Binary tokenized training (~1.2M tokens) and validation datasets.
*   **Phase 1 (Ablation Comparison):**
    *   `generate_comparison.py` — Side-by-side sampling script across checkpoints (`seed=1337`).
    *   `phase1_side_by_side_completion.md` — Qualitative output comparison between 4-head baseline and 1-head ablation.
*   **Phase 2 (Software Engineering Task):**
    *   `run_phase2_eval.py` — Test runner executing docstring generation over 20 canonical Python functions.
    *   `phase2_evaluation_results.md` — Full prompt logs, completions, and Accept/Edit/Reject judgments.
*   **Phase 3 (Evaluate & Break):**
    *   `phase3_probe.py` — Targeted vulnerability harness running 22 adversarial probes.
    *   `phase3_findings.csv` — Mandatory CSV findings table documenting failures, categories, and testability.
    *   `phase3_probe_results.md` — Raw prompt and generation logs across all 6 failure categories.
*   **Phase 4 (Improve & Re-evaluate):**
    *   `phase4_intervention.py` — Repetition penalty decoding intervention runner.
    *   `phase4_comparison.csv` — Before vs. after intervention outcomes across all 22 probes.
    *   `phase4_comparison_results.md` — Side-by-side completion records and regression analysis.

### Original nanoGPT Foundation
*   `model.py` — Core GPT transformer architecture (unmodified).
*   `train.py` — Training loop with AdamW optimizer and mixed-precision execution.
*   `sample.py` — Autoregressive sampling entry point.
*   `config/` (other) & `data/` (openwebtext, shakespeare) — Original template resources.

---

## 2. Environment & Dependency Specifications

*   **Operating System:** Windows 11 (PowerShell 7)
*   **Hardware Accelerator:** NVIDIA GeForce RTX 4060 Laptop GPU (8GB VRAM)
*   **Compute Stack:** Python 3.10+, PyTorch with CUDA support, `tokenizers`, `matplotlib`, `numpy`, `pandas`

```powershell
# Create environment and install dependencies
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install torch torchvision torchaudio --index-url [https://download.pytorch.org/whl/cu121](https://download.pytorch.org/whl/cu121)
pip install numpy tokenizers matplotlib pandas
```
<hr>

## 3. Data Preparation & Reproduction Instructions

The training corpus is composed of three permissively licensed repositories: `TheAlgorithms/Python`, `faif/python-patterns`, and `trekhleb/learn-python`.

### Preprocessing and Tokenizer Generation
Execute the end-to-end data preparation pipeline:

```powershell
python data/corpus/prepare.py
```

* **Deduplication:** Uses SHA-256 content hashing to identify and discard exact duplicate source files.
* **AST Validation:** Employs Python's `ast.parse()` to drop unparseable or corrupted files, eliminating syntax junk.
* **Dataset Partitioning:** Deterministically splits clean files into 90% training and 10% validation sets using random seed `1337`.
* **Tokenizer Training:** Trains a custom Byte-Level Byte-Pair Encoding (BPE) tokenizer strictly on the training split with a target vocabulary size of 8,192.
* **Binary Compilation:** Encodes tokenized sequences delimited by `<|endoftext|>` into `uint16` binary files:
  * `data/corpus/train.bin` (~1,192,089 tokens)
  * `data/corpus/val.bin` (~132,455 tokens)
  * `data/corpus/tokenizer.json`
  * `data/corpus/meta.pkl`

<hr>

## 4. Model Training & Ablation Reproduction

Training is executed with AdamW next-token cross-entropy loss, bfloat16 mixed precision, and gradient accumulation.

### Step 4.1: Train the Baseline Model (4 Attention Heads)
Train the 5.25M-parameter baseline configuration (`n_layer=4`, `n_head=4`, `n_embd=256`, `block_size=512`):

```powershell
python train.py config/train_python.py
```
* **Logging:** Outputs are printed every 100 steps and captured in `baseline_run.log`.
* **Peak Stopping Point:** Validation loss reaches its optimum at ~1,600 iterations (~3.09 val loss, ~1.70 train loss) before overfitting begins.
* **Checkpoint Destination:** Saved to `out-python-baseline/ckpt.pt`.

### Step 4.2: Train the Ablation Model (1 Attention Head)
Train the single-head ablation model keeping all other dimensions and hyper-parameters identical (`n_head=1`):

```powershell
python train.py config/train_python_ablation.py
```
* **Logging:** Outputs captured in `baseline_run_ablation.log`.
* **Convergence:** Step 1,600 yields a validation loss of ~3.03 (~0.06 lower than baseline due to reduced projection variance on the 1.3M-token corpus).
* **Checkpoint Destination:** Saved to `out-python
### Step 4.3: Generate Cross-Entropy Loss Curves
Extract step metrics from both log files and render the comparative plot:

```powershell
python plot_loss.py
```
* **Artifact Produced:** `val_loss_comparison.png`.

<hr>

## 5. Phase-by-Phase Evaluation Reproduction

### Step 5.1: Phase 1 Side-by-Side Generation (Baseline vs. Ablation)
Compare sample completions across both checkpoints (`seed=1337`, `temperature=0.35`, `top_k=10`, `max_new_tokens=40`):

```powershell
python generate_comparison.py
```
* **Artifact Produced:** `phase1_side_by_side_completion.md`.

### Step 5.2: Phase 2 Real SE Task Evaluation (Docstring Generation)
Run the baseline model on the 20 canonical software engineering function signatures:

```powershell
python run_phase2_eval.py
```
* **Artifact Produced:** `phase2_evaluation_results.md`.
* **Evaluation Tallies:**
  * **Accept as-is:** 0 / 20 (0.0%)
  * **Accept after editing:** 5 / 20 (25.0%) (Inputs 7, 9, 12, 15, 17)
  * **Reject:** 15 / 20 (75.0%)

### Step 5.3: Phase 3 Vulnerability Probing & Testability Assessment
Execute the 22 targeted probes across the 6 standardized failure modes:

```powershell
python phase3_probe.py
```
* **Artifacts Produced:** `phase3_findings.csv` and `phase3_probe_results.md`.
* **Failure Distribution (N = 22 Probes):**
  * `context-ignored`: Probes 4, 5, 6, 7 -> **4/22 (18.18%)**
  * `prompt-sensitive`: Probes 8, 9, 10, 11 -> **4/22 (18.18%)**
  * `invented-api`: Probes 12, 13, 14, 15 -> **4/22 (18.18%)**
  * `wrong-logic`: Probes 16, 17, 18, 19 -> **4/22 (18.18%)**
  * `syntax`: Probes 20, 21, 22 -> **3/22 (13.64%)**
  * `memorized`: Probes 1, 2, 3 -> **3/22 (13.64%)**
* **Detection Rates (N = 22 Probes):**
  * Standard Unit Tests: **3/22 (13.64%)** caught (syntax rejections only; non-crashing semantic/logic bugs bypass silent passes).
  * Docstring Tests (`doctest`): **9/22 (40.91%)** caught (uncovers mathematically broken outputs and unclosed test loops in docstring assertions).

### Step 5.4: Phase 4 Decoding Intervention & Comparative Analysis
Re-run the 22 Phase 3 probes with an inference-level candidate repetition penalty to suppress softmax entropy collapse:

```powershell
python phase4_intervention.py
```
* **Artifacts Produced:** `phase4_comparison.csv` and `phase4_comparison_results.md`.
* **Intervention Outcome Rates (N = 22 Probes):**
  * **Major Improvement:** **5/22 (22.73%)** (Probes 4, 5, 7, 12, 19 - terminated degeneration loops, closed quote blocks cleanly)
  * **Some Improvement:** **13/22 (59.09%)** (repetition reduced; generated varied docstring skeletons)
  * **No Change:** **2/22 (9.09%)** (Probes 11, 18 - base logic errors persisted)
  * **Regression:** **2/22 (9.09%)** (Probes 2, 13 - penalizing duplicate tokens broke valid repetition such as recursive base-case identifiers and nested types)
  * **Total Positive Impact:** **18/22 (81.82%)**

<hr>

## 6. AI-Use Disclosure

An AI coding assistant was used in a lightweight, supervised capacity during development:
* **Scaffolding & Templates:** Generating initial file parsing logic in `data/corpus/prepare.py` and repetitive test execution harnesses.
* **Concept Clarification:** Verifying cross-entropy formulation, attention head tensor shapes, and BPE subword edge cases.
* **Human Control & Verification:** Every script was debugged and tested locally in PowerShell. Syntax errors, hallucinated flags, and incorrect parameters were caught and corrected manually before committing.
* Full detailed log and human verification notes are available in Appendix 5.1 of `Project_1_Report.pdf`.

# nanoGPT

![nanoGPT](assets/nanogpt.jpg)


---

**Update Nov 2025** nanoGPT has a new and improved cousin called [nanochat](https://github.com/karpathy/nanochat). It is very likely you meant to use/find nanochat instead. nanoGPT (this repo) is now very old and deprecated but I will leave it up for posterity.

---

The simplest, fastest repository for training/finetuning medium-sized GPTs. It is a rewrite of [minGPT](https://github.com/karpathy/minGPT) that prioritizes teeth over education. Still under active development, but currently the file `train.py` reproduces GPT-2 (124M) on OpenWebText, running on a single 8XA100 40GB node in about 4 days of training. The code itself is plain and readable: `train.py` is a ~300-line boilerplate training loop and `model.py` a ~300-line GPT model definition, which can optionally load the GPT-2 weights from OpenAI. That's it.

![repro124m](assets/gpt2_124M_loss.png)

Because the code is so simple, it is very easy to hack to your needs, train new models from scratch, or finetune pretrained checkpoints (e.g. biggest one currently available as a starting point would be the GPT-2 1.3B model from OpenAI).

## install

```
pip install torch numpy transformers datasets tiktoken wandb tqdm
```

Dependencies:

- [pytorch](https://pytorch.org) <3
- [numpy](https://numpy.org/install/) <3
-  `transformers` for huggingface transformers <3 (to load GPT-2 checkpoints)
-  `datasets` for huggingface datasets <3 (if you want to download + preprocess OpenWebText)
-  `tiktoken` for OpenAI's fast BPE code <3
-  `wandb` for optional logging <3
-  `tqdm` for progress bars <3

## quick start

If you are not a deep learning professional and you just want to feel the magic and get your feet wet, the fastest way to get started is to train a character-level GPT on the works of Shakespeare. First, we download it as a single (1MB) file and turn it from raw text into one large stream of integers:

```sh
python data/shakespeare_char/prepare.py
```

This creates a `train.bin` and `val.bin` in that data directory. Now it is time to train your GPT. The size of it very much depends on the computational resources of your system:

**I have a GPU**. Great, we can quickly train a baby GPT with the settings provided in the [config/train_shakespeare_char.py](config/train_shakespeare_char.py) config file:

```sh
python train.py config/train_shakespeare_char.py
```

If you peek inside it, you'll see that we're training a GPT with a context size of up to 256 characters, 384 feature channels, and it is a 6-layer Transformer with 6 heads in each layer. On one A100 GPU this training run takes about 3 minutes and the best validation loss is 1.4697. Based on the configuration, the model checkpoints are being written into the `--out_dir` directory `out-shakespeare-char`. So once the training finishes we can sample from the best model by pointing the sampling script at this directory:

```sh
python sample.py --out_dir=out-shakespeare-char
```

This generates a few samples, for example:

```
ANGELO:
And cowards it be strawn to my bed,
And thrust the gates of my threats,
Because he that ale away, and hang'd
An one with him.

DUKE VINCENTIO:
I thank your eyes against it.

DUKE VINCENTIO:
Then will answer him to save the malm:
And what have you tyrannous shall do this?

DUKE VINCENTIO:
If you have done evils of all disposition
To end his power, the day of thrust for a common men
That I leave, to fight with over-liking
Hasting in a roseman.
```

lol  `¯\_(ツ)_/¯`. Not bad for a character-level model after 3 minutes of training on a GPU. Better results are quite likely obtainable by instead finetuning a pretrained GPT-2 model on this dataset (see finetuning section later).

**I only have a macbook** (or other cheap computer). No worries, we can still train a GPT but we want to dial things down a notch. I recommend getting the bleeding edge PyTorch nightly ([select it here](https://pytorch.org/get-started/locally/) when installing) as it is currently quite likely to make your code more efficient. But even without it, a simple train run could look as follows:

```sh
python train.py config/train_shakespeare_char.py --device=cpu --compile=False --eval_iters=20 --log_interval=1 --block_size=64 --batch_size=12 --n_layer=4 --n_head=4 --n_embd=128 --max_iters=2000 --lr_decay_iters=2000 --dropout=0.0
```

Here, since we are running on CPU instead of GPU we must set both `--device=cpu` and also turn off PyTorch 2.0 compile with `--compile=False`. Then when we evaluate we get a bit more noisy but faster estimate (`--eval_iters=20`, down from 200), our context size is only 64 characters instead of 256, and the batch size only 12 examples per iteration, not 64. We'll also use a much smaller Transformer (4 layers, 4 heads, 128 embedding size), and decrease the number of iterations to 2000 (and correspondingly usually decay the learning rate to around max_iters with `--lr_decay_iters`). Because our network is so small we also ease down on regularization (`--dropout=0.0`). This still runs in about ~3 minutes, but gets us a loss of only 1.88 and therefore also worse samples, but it's still good fun:

```sh
python sample.py --out_dir=out-shakespeare-char --device=cpu
```
Generates samples like this:

```
GLEORKEN VINGHARD III:
Whell's the couse, the came light gacks,
And the for mought you in Aut fries the not high shee
bot thou the sought bechive in that to doth groan you,
No relving thee post mose the wear
```

Not bad for ~3 minutes on a CPU, for a hint of the right character gestalt. If you're willing to wait longer, feel free to tune the hyperparameters, increase the size of the network, the context length (`--block_size`), the length of training, etc.

Finally, on Apple Silicon Macbooks and with a recent PyTorch version make sure to add `--device=mps` (short for "Metal Performance Shaders"); PyTorch then uses the on-chip GPU that can *significantly* accelerate training (2-3X) and allow you to use larger networks. See [Issue 28](https://github.com/karpathy/nanoGPT/issues/28) for more.

## reproducing GPT-2

A more serious deep learning professional may be more interested in reproducing GPT-2 results. So here we go - we first tokenize the dataset, in this case the [OpenWebText](https://openwebtext2.readthedocs.io/en/latest/), an open reproduction of OpenAI's (private) WebText:

```sh
python data/openwebtext/prepare.py
```

This downloads and tokenizes the [OpenWebText](https://huggingface.co/datasets/openwebtext) dataset. It will create a `train.bin` and `val.bin` which holds the GPT2 BPE token ids in one sequence, stored as raw uint16 bytes. Then we're ready to kick off training. To reproduce GPT-2 (124M) you'll want at least an 8X A100 40GB node and run:

```sh
torchrun --standalone --nproc_per_node=8 train.py config/train_gpt2.py
```

This will run for about 4 days using PyTorch Distributed Data Parallel (DDP) and go down to loss of ~2.85. Now, a GPT-2 model just evaluated on OWT gets a val loss of about 3.11, but if you finetune it it will come down to ~2.85 territory (due to an apparent domain gap), making the two models ~match.

If you're in a cluster environment and you are blessed with multiple GPU nodes you can make GPU go brrrr e.g. across 2 nodes like:

```sh
# Run on the first (master) node with example IP 123.456.123.456:
torchrun --nproc_per_node=8 --nnodes=2 --node_rank=0 --master_addr=123.456.123.456 --master_port=1234 train.py
# Run on the worker node:
torchrun --nproc_per_node=8 --nnodes=2 --node_rank=1 --master_addr=123.456.123.456 --master_port=1234 train.py
```

It is a good idea to benchmark your interconnect (e.g. iperf3). In particular, if you don't have Infiniband then also prepend `NCCL_IB_DISABLE=1` to the above launches. Your multinode training will work, but most likely _crawl_. By default checkpoints are periodically written to the `--out_dir`. We can sample from the model by simply `python sample.py`.

Finally, to train on a single GPU simply run the `python train.py` script. Have a look at all of its args, the script tries to be very readable, hackable and transparent. You'll most likely want to tune a number of those variables depending on your needs.

## baselines

OpenAI GPT-2 checkpoints allow us to get some baselines in place for openwebtext. We can get the numbers as follows:

```sh
$ python train.py config/eval_gpt2.py
$ python train.py config/eval_gpt2_medium.py
$ python train.py config/eval_gpt2_large.py
$ python train.py config/eval_gpt2_xl.py
```

and observe the following losses on train and val:

| model | params | train loss | val loss |
| ------| ------ | ---------- | -------- |
| gpt2 | 124M         | 3.11  | 3.12     |
| gpt2-medium | 350M  | 2.85  | 2.84     |
| gpt2-large | 774M   | 2.66  | 2.67     |
| gpt2-xl | 1558M     | 2.56  | 2.54     |

However, we have to note that GPT-2 was trained on (closed, never released) WebText, while OpenWebText is just a best-effort open reproduction of this dataset. This means there is a dataset domain gap. Indeed, taking the GPT-2 (124M) checkpoint and finetuning on OWT directly for a while reaches loss down to ~2.85. This then becomes the more appropriate baseline w.r.t. reproduction.

## finetuning

Finetuning is no different than training, we just make sure to initialize from a pretrained model and train with a smaller learning rate. For an example of how to finetune a GPT on new text go to `data/shakespeare` and run `prepare.py` to download the tiny shakespeare dataset and render it into a `train.bin` and `val.bin`, using the OpenAI BPE tokenizer from GPT-2. Unlike OpenWebText this will run in seconds. Finetuning can take very little time, e.g. on a single GPU just a few minutes. Run an example finetuning like:

```sh
python train.py config/finetune_shakespeare.py
```

This will load the config parameter overrides in `config/finetune_shakespeare.py` (I didn't tune them much though). Basically, we initialize from a GPT2 checkpoint with `init_from` and train as normal, except shorter and with a small learning rate. If you're running out of memory try decreasing the model size (they are `{'gpt2', 'gpt2-medium', 'gpt2-large', 'gpt2-xl'}`) or possibly decreasing the `block_size` (context length). The best checkpoint (lowest validation loss) will be in the `out_dir` directory, e.g. in `out-shakespeare` by default, per the config file. You can then run the code in `sample.py --out_dir=out-shakespeare`:

```
THEODORE:
Thou shalt sell me to the highest bidder: if I die,
I sell thee to the first; if I go mad,
I sell thee to the second; if I
lie, I sell thee to the third; if I slay,
I sell thee to the fourth: so buy or sell,
I tell thee again, thou shalt not sell my
possession.

JULIET:
And if thou steal, thou shalt not sell thyself.

THEODORE:
I do not steal; I sell the stolen goods.

THEODORE:
Thou know'st not what thou sell'st; thou, a woman,
Thou art ever a victim, a thing of no worth:
Thou hast no right, no right, but to be sold.
```

Whoa there, GPT, entering some dark place over there. I didn't really tune the hyperparameters in the config too much, feel free to try!

## sampling / inference

Use the script `sample.py` to sample either from pre-trained GPT-2 models released by OpenAI, or from a model you trained yourself. For example, here is a way to sample from the largest available `gpt2-xl` model:

```sh
python sample.py \
    --init_from=gpt2-xl \
    --start="What is the answer to life, the universe, and everything?" \
    --num_samples=5 --max_new_tokens=100
```

If you'd like to sample from a model you trained, use the `--out_dir` to point the code appropriately. You can also prompt the model with some text from a file, e.g. ```python sample.py --start=FILE:prompt.txt```.

## efficiency notes

For simple model benchmarking and profiling, `bench.py` might be useful. It's identical to what happens in the meat of the training loop of `train.py`, but omits much of the other complexities.

Note that the code by default uses [PyTorch 2.0](https://pytorch.org/get-started/pytorch-2.0/). At the time of writing (Dec 29, 2022) this makes `torch.compile()` available in the nightly release. The improvement from the one line of code is noticeable, e.g. cutting down iteration time from ~250ms / iter to 135ms / iter. Nice work PyTorch team!

## todos

- Investigate and add FSDP instead of DDP
- Eval zero-shot perplexities on standard evals (e.g. LAMBADA? HELM? etc.)
- Finetune the finetuning script, I think the hyperparams are not great
- Schedule for linear batch size increase during training
- Incorporate other embeddings (rotary, alibi)
- Separate out the optim buffers from model params in checkpoints I think
- Additional logging around network health (e.g. gradient clip events, magnitudes)
- Few more investigations around better init etc.

## troubleshooting

Note that by default this repo uses PyTorch 2.0 (i.e. `torch.compile`). This is fairly new and experimental, and not yet available on all platforms (e.g. Windows). If you're running into related error messages try to disable this by adding `--compile=False` flag. This will slow down the code but at least it will run.

For some context on this repository, GPT, and language modeling it might be helpful to watch my [Zero To Hero series](https://karpathy.ai/zero-to-hero.html). Specifically, the [GPT video](https://www.youtube.com/watch?v=kCc8FmEb1nY) is popular if you have some prior language modeling context.

For more questions/discussions feel free to stop by **#nanoGPT** on Discord:

[![](https://dcbadge.vercel.app/api/server/3zy8kqD9Cp?compact=true&style=flat)](https://discord.gg/3zy8kqD9Cp)

## acknowledgements

All nanoGPT experiments are powered by GPUs on [Lambda labs](https://lambdalabs.com), my favorite Cloud GPU provider. Thank you Lambda labs for sponsoring nanoGPT!
