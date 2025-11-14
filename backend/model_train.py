import pandas as pd
import hashlib
import json
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def hash_model(model):
    model_str = str(model.get_params())
    return hashlib.sha256(model_str.encode()).hexdigest()

def train_and_prove(dataset_path):
    # Load dataset
    df = pd.read_csv(dataset_path, encoding='utf-8-sig')

    # Simple cleanup
    df = df.dropna()

    # Encode categorical columns automatically
    df = pd.get_dummies(df, drop_first=True)

    # Separate features/labels (last column = target)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Debug: show unique labels in the target column
    print("Unique labels in target column:", getattr(y, 'unique', lambda: 'N/A')())

    #  Split data — stratify to preserve class distribution in small datasets
    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    except ValueError:
        # Fallback: if stratify fails (e.g., too few members of a class), do a plain split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Train model
    start_time = time.time()
    # Ensure training set has at least 2 classes
    if y_train.nunique() < 2:
        raise ValueError(f"Training set contains only one class ({y_train.unique()}); try a smaller test_size or provide more data.")

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    training_time = round(time.time() - start_time, 3)

    # Evaluate
    y_pred = model.predict(X_test)
    acc = round(accuracy_score(y_test, y_pred) * 100, 2)

    # Generate hashes
    dataset_hash = hash_file(dataset_path)
    model_hash = hash_model(model)

    # Prepare metadata
    metadata = {
        "dataset_hash": dataset_hash,
        "model_hash": model_hash,
        "accuracy": acc,
        "training_time_s": training_time,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Save to JSON
    with open("output_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print(json.dumps(metadata, indent=4))
    # return for programmatic use
    return metadata

if __name__ == "__main__":
    dataset_path = "sample_datasets/sample.csv"
    train_and_prove(dataset_path)
