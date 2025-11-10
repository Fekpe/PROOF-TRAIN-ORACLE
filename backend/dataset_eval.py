import pandas as pd
import hashlib
import json
from pathlib import Path

def hash_file(file_path):
    """Generate a SHA256 hash for the dataset."""
    with open(file_path, "rb") as f:
        bytes_data = f.read()
        return hashlib.sha256(bytes_data).hexdigest()

def evaluate_dataset(file_path):
    """Evaluate dataset quality and return metrics + score."""
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    # Basic metrics
    total_rows, total_cols = df.shape
    missing_ratio = df.isnull().sum().sum() / (total_rows * total_cols)
    numeric_cols = df.select_dtypes(include='number').shape[1]
    categorical_cols = df.select_dtypes(exclude='number').shape[1]

    # Numeric vs categorical balance (ideal ~50/50)
    if total_cols > 0:
        numeric_balance = abs((numeric_cols / total_cols) - 0.5)
    else:
        numeric_balance = 0

    # Optional bias metric (simple: if a categorical column is unbalanced)
    bias_metric = 0
    for col in df.select_dtypes(exclude='number').columns:
        max_class_ratio = df[col].value_counts(normalize=True).max()
        bias_metric += max_class_ratio
    bias_metric = bias_metric / max(1, len(df.select_dtypes(exclude='number').columns))

    # Compute quality score (lower is better for bias & missing ratio)
    quality_score = round((1 - (missing_ratio + numeric_balance + (bias_metric - 0.5))) * 100, 2)
    quality_score = max(0, min(quality_score, 100))  # keep between 0 and 100

    # Dataset hash
    dataset_hash = hash_file(file_path)

    # Result dictionary
    result = {
        "dataset_hash": dataset_hash,
        "quality_score": quality_score,
        "metrics": {
            "rows": total_rows,
            "columns": total_cols,
            "missing_ratio": round(missing_ratio, 3),
            "numeric_cols": numeric_cols,
            "categorical_cols": categorical_cols,
            "bias_metric": round(bias_metric, 3)
        }
    }

    return result


if __name__ == "__main__":
    file_path = Path("sample_datasets/sample.csv")
    evaluation = evaluate_dataset(file_path)

    # Save output as JSON
    output_path = Path("docs/demo_notes.md")
    output_json = json.dumps(evaluation, indent=4)
    print(output_json)

    # Append to docs/demo_notes.md
    with open(output_path, "a") as f:
        f.write("\n### Dataset Evaluation Output\n")
        f.write("```\n")
        f.write(output_json)
        f.write("\n```\n")

    print(f"✅ Evaluation complete! Results written to {output_path}")
