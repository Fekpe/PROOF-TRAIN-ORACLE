import json
import os
import hashlib
import random
import time
from datetime import datetime
from pathlib import Path

# Correct variable name
BACKEND_OUTPUT = Path(__file__).resolve().parent.parent / "backend" / "output_metadata.json"
MOCK_CHAIN_LOG = Path(__file__).resolve().parent / "mock_chain_log.json"


def generate_tx_hash():
    """Generate a mock blockchain transaction hash."""
    random_bytes = os.urandom(16)
    return "0x" + hashlib.sha256(random_bytes).hexdigest()[:16]


def load_backend_metadata():
    """Load the latest output from model_train.py."""
    if not os.path.exists(BACKEND_OUTPUT):
        raise FileNotFoundError("No backend output found. Run model_train.py first.")
    
    with open(BACKEND_OUTPUT, "r") as f:
        data = json.load(f)
    return data


def push_to_chain(backend_data):
    """Simulate pushing metadata to blockchain."""
    record = {
        "tx_hash": generate_tx_hash(),
        "dataset_hash": backend_data.get("dataset_hash", ""),
        "model_hash": backend_data.get("model_hash", ""),
        "accuracy": backend_data.get("accuracy", 0),
        "training_time": backend_data.get("training_time_s", 0),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": round(random.uniform(0.01, 0.1), 4),  # Mock price
        "quality_score": random.randint(70, 100)       # Mock dataset score
    }

    # Append record to mock chain log
    existing = []
    if os.path.exists(MOCK_CHAIN_LOG):
        with open(MOCK_CHAIN_LOG, "r") as f:
            existing = json.load(f)
    existing.append(record)

    with open(MOCK_CHAIN_LOG, "w") as f:
        json.dump(existing, f, indent=4)

    return record


if __name__ == "__main__":
    print("Proof Train Oracle | On-Chain Registry Simulation\n")

    try:
        backend_data = load_backend_metadata()
        print(f"Loaded backend proof:\n{json.dumps(backend_data, indent=4)}\n")

        tx_record = push_to_chain(backend_data)
        print(f"Successfully pushed to mock chain:\n{json.dumps(tx_record, indent=4)}")

    except Exception as e:
        print(f"Error: {e}")
