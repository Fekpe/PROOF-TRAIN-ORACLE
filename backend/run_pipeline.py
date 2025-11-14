import json
import os
from pathlib import Path

import runpy
from model_train import train_and_prove
import sys
from pathlib import Path

# interactions lives in ../blockchain
sys.path.append(str(Path(__file__).resolve().parent.parent))
from blockchain import interactions

import pandas as pd


def evaluate_dataset_local(path):
    """Compute basic dataset metrics similar to the evaluator and return a dict suitable for frontend mock."""
    df = pd.read_csv(path, encoding='utf-8-sig')
    total_rows, total_cols = df.shape
    missing_ratio = df.isnull().sum().sum() / (total_rows * total_cols)
    numeric_cols = df.select_dtypes(include='number').shape[1]
    categorical_cols = df.select_dtypes(exclude='number').shape[1]
    bias_metric = 0
    cat_cols = df.select_dtypes(exclude='number').columns
    for col in cat_cols:
        max_class_ratio = df[col].value_counts(normalize=True).max()
        bias_metric += max_class_ratio
    bias_metric = bias_metric / max(1, len(cat_cols))

    return {
        "name": Path(path).name,
        "dataset_hash": None,
        "quality_score": round((1 - (missing_ratio + abs((numeric_cols/ max(1,total_cols)) - 0.5) + (bias_metric - 0.5))) * 100, 2),
        "metrics": {
            "rows": int(total_rows),
            "columns": int(total_cols),
            "missing_ratio": round(missing_ratio, 3),
            "numeric_cols": int(numeric_cols),
            "categorical_cols": int(categorical_cols),
            "bias_metric": round(bias_metric, 3)
        }
    }

# alias
evaluate_dataset = evaluate_dataset_local


ROOT = Path(__file__).resolve().parent.parent
FRONTEND_MOCK = ROOT / "frontend" / "mock"
DOCS = ROOT / "docs"


def ensure_frontend_mock():
    FRONTEND_MOCK.mkdir(parents=True, exist_ok=True)


def run_full_pipeline(dataset_rel_path="sample_datasets/sample.csv"):
    # resolve dataset path relative to backend directory
    backend_dir = Path(__file__).resolve().parent
    dataset_path = Path(dataset_rel_path)
    if not dataset_path.exists():
        dataset_path = backend_dir / dataset_rel_path
    print(f"1) Evaluating dataset: {dataset_path}")
    eval_result = evaluate_dataset(dataset_path)

    # write evaluation to backend and frontend mock
    backend_eval_path = Path(__file__).resolve().parent / "dataset_evaluation.json"
    with open(backend_eval_path, "w", encoding='utf-8') as f:
        json.dump(eval_result, f, indent=4)

    ensure_frontend_mock()
    with open(FRONTEND_MOCK / "datasets.json", "w") as f:
        json.dump([eval_result], f, indent=4)

    print("2) Training model")
    metadata = train_and_prove(dataset_path)

    # Save backend output is already handled by train_and_prove (output_metadata.json)

    print("3) Pushing proof to mock chain")
    tx_record = interactions.push_to_chain(metadata)

    # Update frontend mock models.json
    model_entry = {
        "model_hash": metadata.get("model_hash"),
        "dataset_hash": metadata.get("dataset_hash"),
        "accuracy": metadata.get("accuracy"),
        "training_time_s": metadata.get("training_time_s"),
        "timestamp": metadata.get("timestamp"),
        "tx_hash": tx_record.get("tx_hash")
    }
    with open(FRONTEND_MOCK / "models.json", "w") as f:
        json.dump([model_entry], f, indent=4)

    print("Pipeline complete. Frontend mock files updated:")
    print(f" - {FRONTEND_MOCK / 'datasets.json'}")
    print(f" - {FRONTEND_MOCK / 'models.json'}")
    print(f"Mock chain log: {interactions.MOCK_CHAIN_LOG}")


if __name__ == "__main__":
    run_full_pipeline()
