import json
from pathlib import Path

from src.hello_nlp import main


def test_reproducible_same_seed():
    main()
    a = json.loads(Path("results/lab0_metrics.json").read_text(encoding="utf-8"))

    main()
    b = json.loads(Path("results/lab0_metrics.json").read_text(encoding="utf-8"))

    assert a["config"]["seed"] == b["config"]["seed"]
    assert a["metrics"] == b["metrics"]