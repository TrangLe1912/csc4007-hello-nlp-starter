import json
import platform
from datetime import datetime
from pathlib import Path


def main() -> None:
    # Minimal imports to verify environment for the course
    import numpy as np
    import pandas as pd
    import sklearn
    import transformers
    import datasets
    import evaluate
    import underthesea  # noqa: F401

    info = {
        "timestamp_utc": datetime.utcnow().isoformat() + "Z",
        "python": platform.python_version(),
        "platform": platform.platform(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "sklearn": sklearn.__version__,
        "transformers": transformers.__version__,
        "datasets": datasets.__version__,
        "evaluate": evaluate.__version__,
        "vn_lib": "underthesea",
    }

    Path("logs").mkdir(exist_ok=True)
    Path("results").mkdir(exist_ok=True)

    Path("logs/lab0_run.log").write_text(
        "[LAB0] ENV CHECK OK\n" + json.dumps(info, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    Path("results/lab0_env.json").write_text(
        json.dumps(info, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print("✅ ENV CHECK OK → logs/lab0_run.log, results/lab0_env.json")


if __name__ == "__main__":
    main()