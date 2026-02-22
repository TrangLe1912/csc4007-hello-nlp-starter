from pathlib import Path
import json

from src.hello_nlp import main


def test_outputs_created():
    # run pipeline
    main()

    assert Path("logs/lab0_hello_nlp.log").exists()
    assert Path("results/lab0_metrics.json").exists()

    obj = json.loads(Path("results/lab0_metrics.json").read_text(encoding="utf-8"))
    assert "config" in obj and "metrics" in obj