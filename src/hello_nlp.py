import json
import random
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split


@dataclass
class Config:
    seed: int = 42
    n_samples: int = 300
    test_size: float = 0.2
    ngram_range: Tuple[int, int] = (1, 2)
    max_iter: int = 500


def make_random_vietnamese_text_dataset(n: int, seed: int = 42) -> Tuple[List[str], List[int]]:
    rng = random.Random(seed)

    vocab_pos = ["hay", "tuyet", "xuc_dong", "dang_xem", "chat_luong", "dinh", "cam_xuc"]
    vocab_neg = ["te", "chan", "phi_thoi_gian", "do", "kho_hieu", "giong_gao", "that_vong"]
    noises = ["😄", "😡", "!!!", "???", "^^", ""]

    texts, labels = [], []
    for _ in range(n):
        y = rng.randint(0, 1)
        labels.append(y)

        vocab = vocab_pos if y == 1 else vocab_neg
        length = rng.randint(5, 16)

        words = rng.choices(vocab, k=length)

        # add 0–2 noise tokens
        for _ in range(rng.randint(0, 2)):
            words.append(rng.choice(noises))

        texts.append(" ".join(words).strip())

    return texts, labels


def train_eval_pipeline(texts: List[str], labels: List[int], cfg: Config) -> dict:
    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=cfg.test_size,
        random_state=cfg.seed,
        stratify=labels,
    )

    # IMPORTANT: fit ONLY on train (anti-leakage)
    vec = TfidfVectorizer(ngram_range=cfg.ngram_range)
    Xtr = vec.fit_transform(X_train)
    Xte = vec.transform(X_test)

    clf = LogisticRegression(max_iter=cfg.max_iter, random_state=cfg.seed)
    clf.fit(Xtr, y_train)
    pred = clf.predict(Xte)

    acc = accuracy_score(y_test, pred)
    f1 = f1_score(y_test, pred, average="macro")
    cm = confusion_matrix(y_test, pred).tolist()

    return {
        "accuracy": float(acc),
        "macro_f1": float(f1),
        "confusion_matrix": cm,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
        "vocab_size": int(len(vec.vocabulary_)),
    }


def write_artefacts(cfg: Config, metrics: dict) -> None:
    Path("logs").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)

    run_info = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "config": cfg.__dict__,
        "metrics": metrics,
    }

    Path("logs/lab0_hello_nlp.log").write_text(
        "[LAB0] HELLO NLP (random data) DONE\n"
        + json.dumps(run_info, indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )

    Path("results/lab0_metrics.json").write_text(
        json.dumps(run_info, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def main():
    cfg = Config(seed=42, n_samples=300)
    texts, labels = make_random_vietnamese_text_dataset(cfg.n_samples, seed=cfg.seed)
    metrics = train_eval_pipeline(texts, labels, cfg)
    write_artefacts(cfg, metrics)

    print("✅ Hello NLP DONE")
    print("Metrics:", metrics)
    print("Saved: logs/lab0_hello_nlp.log, results/lab0_metrics.json")


if __name__ == "__main__":
    main()