# CSC4007 — Lab0: Setup & Hello NLP

[![CI](https://github.com/TrangLe1912/csc4007-hello-nlp-starter/actions/workflows/ci.yml/badge.svg)](https://github.com/TrangLe1912/csc4007-hello-nlp-starter/actions/workflows/ci.yml)

## 1) Fork repo
1. Mở repo starter kit của GV.
2. Bấm **Fork** để tạo repo của bạn.
3. Clone repo fork về máy.

## 2) Setup môi trường bằng Anaconda (cài 1 lần dùng cả kỳ)
Mở **Anaconda Prompt / Terminal**:

```bash
conda create -n csc4007_nlp python=3.10 -y
conda activate csc4007_nlp
python -m pip install -U pip
pip install -r requirements_core.txt
```

## Optional (nhóm làm RAG/System):
```bash
pip install -r requirements_rag.txt
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

Seed mặc định = 42 (trong src/hello_nlp.py)

## Responsible use

Lab0 dùng dữ liệu random, không chứa PII.

Metric chỉ để xác nhận setup chạy được.

## What to submit

Repo link (GitHub) + đủ README / tests (>=5) / logs / results / report_page.md.

## 7) Lệnh chạy “1 phát ăn ngay” (SV copy)
```bash
python src/env_check.py && python src/hello_nlp_random.py && pytest -q
```

## 8) CI tự động kiểm tra bài (GitHub Actions) — vì sao bạn thấy dấu ✅ / ❌

Repo này có bật **GitHub Actions (CI)**. Mỗi lần bạn **push code** lên GitHub (hoặc mở Pull Request), hệ thống sẽ tự chạy một chuỗi kiểm tra để xem bài của bạn đã “đúng chuẩn Lab0” chưa.

### CI sẽ tự chạy những gì?
CI sẽ lần lượt:
1. Cài thư viện từ `requirements_core.txt`
2. Chạy kiểm tra môi trường:
   ```bash
   python src/env_check.py
   ```
3. Chạy chương trình “Hello NLP”
   ```bash
   python src/hello_nlp.py
   ```
4. Chạy unitest
   ```bash
   pytest -q
   ```
### ✅ Khi nào CI PASS?

  CI PASS khi:

    Cài thư viện thành công

    Code chạy không lỗi

    Tạo được các file minh chứng trong logs/ và results/

    Tất cả tests đều PASS


### ❌ Khi nào CI FAIL?

  CI FAIL nếu bạn gặp một trong các lỗi sau:

    Thiếu file / sai đường dẫn (ví dụ thiếu src/hello_nlp_random.py)

    Cài thư viện lỗi (pip/conda lỗi)

    Chạy chương trình bị lỗi (crash)

    Không tạo được output logs/… hoặc results/…

    Có test bị fail (ví dụ test anti-leakage / reproducibility / robustness)


### Xem CI ở đâu? (cách mở log lỗi)

    Vào repo GitHub của bạn

    Chọn tab Actions

    Bấm vào workflow gần nhất (có dấu ❌ nếu fail)

    Mở step bị lỗi để đọc log (thường là step “Run env check + hello NLP + tests”)
  

### Sửa xong thì làm gì?

    Sửa code/file theo log

    Commit và push lại

    CI sẽ tự chạy lại. Khi thấy ✅ là ok.
