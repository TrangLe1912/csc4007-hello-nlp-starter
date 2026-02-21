# CSC4007 — Lab0: Setup & Hello NLP

## 1) Fork repo
1. Mở repo starter kit của GV.
2. Bấm **Fork** để tạo repo của bạn.
3. Clone repo fork về máy.

## 2) Setup môi trường bằng Anaconda (cài 1 lần dùng cả kỳ)
Mở **Anaconda Prompt / Terminal**:

```bash
conda create -n csc4007-nlp python=3.10 -y
conda activate csc4007-nlp
python -m pip install -U pip
pip install -r requirements.txt
```

## Optional (nhóm làm RAG/System):
```bash
pip install -r requirements-rag.txt
```
## Chạy chương trình test cài đặt môi trường

```bash
python src/env_check.py
python src/hello_nlp.py
pytest -q
```

### Output (bắt buộc có)

logs/lab0_run.log

results/lab0_env.json

logs/lab0_hello_nlp.log

results/lab0_metrics.json

## Reproducibility

Seed mặc định = 42 (trong src/hello_nlp_random.py)

## Responsible use

Lab0 dùng dữ liệu random, không chứa PII.

Metric chỉ để xác nhận setup chạy được.

## What to submit

Repo link (GitHub) + đủ README / tests (>=5) / logs / results / report_page.md.

## 7) Lệnh chạy “1 phát ăn ngay” (SV copy)
```bash
python src/env_check.py && python src/hello_nlp_random.py && pytest -q
```