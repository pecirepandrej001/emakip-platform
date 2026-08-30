"""Minimal fine-tuning entry point for a CrossEncoder reranker.

Provide a CSV with columns: query, positive, negative.
"""
import argparse
import pandas as pd
from sentence_transformers import CrossEncoder, InputExample
from torch.utils.data import DataLoader
from src.core.config import get_settings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--output", default="artifacts/reranker")
    parser.add_argument("--epochs", type=int, default=1)
    args = parser.parse_args()

    df = pd.read_csv(args.data)
    samples = []
    for row in df.itertuples():
        samples.append(InputExample(texts=[row.query, row.positive], label=1.0))
        samples.append(InputExample(texts=[row.query, row.negative], label=0.0))

    model = CrossEncoder(get_settings().reranker_model, num_labels=1)
    loader = DataLoader(samples, shuffle=True, batch_size=8)
    model.fit(train_dataloader=loader, epochs=args.epochs, warmup_steps=max(1, len(loader)//10), output_path=args.output)
    print(f"Saved reranker to {args.output}")

if __name__ == "__main__":
    main()
