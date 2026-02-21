# CSC4007 — Lab0: Setup & Hello NLP (Starter Kit)

## 1) How to run

### Option A — Local (Conda)
```bash
conda create -n csc4007-nlp python=3.10 -y
conda activate csc4007-nlp
python -m pip install -U pip

# PyTorch CPU (safe default)
pip install torch --index-url https://download.pytorch.org/whl/cpu

pip install -r requirements-core.txt

python src/env_check.py
python src/mini_pipeline.py
pytest -q