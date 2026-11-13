#!/usr/bin/env python3
"""
The baseline. ← UNIT 6, MILESTONE 1

Before you judge your trained model, find out how hard the task is without one.

This runs a general model over your held-out posts using **only your label
definitions** — no training, no examples. That's called zero-shot, and it's a
fair opponent. If it matches your fine-tuned model, your training added
nothing, and that is a finding worth having rather than a failure.

**The same posts, both models.** Section 5 of the notebook writes the held-out
split to `test_split.csv` and commits it. This reads that file, so the two
columns of your Baseline vs. Trained table are scored on one set of posts. A
comparison across two different sets isn't a comparison.

Everything here runs **on your own machine**. No account, no key, nothing to
sign up for. It is slower than the trained model — expect a few seconds per
post, so 30 posts takes a couple of minutes. That's normal, and it's part of
the point: this is what "no fine-tuning" costs you at runtime as well as in
accuracy.

    python baseline.py --help
    python baseline.py
    python baseline.py --trained results.json
    python baseline.py --review-threshold 0.75 --review-out review_results.json

The first run downloads the model, about 1.6 GB. Do that before class, not
during.
"""

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Windows consoles default to a codepage that can't encode the characters this
# file prints, and Python only notices when the output is redirected — so
# `python baseline.py > log.txt` would crash where the same command on screen is
# fine. Ask for UTF-8 on the way out.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, OSError, ValueError):
        pass


# The zero-shot model. It was trained to judge whether a piece of text entails
# a hypothesis, which is enough to ask "is this post about X?" without ever
# having seen your labels.
ZERO_SHOT_MODEL = "facebook/bart-large-mnli"

# What gets slotted into the hypothesis for each label. Your label names are
# short, so this gives the model a sentence to work with.
HYPOTHESIS = "This post is {}."


def load_definitions(path):
    """
    Read your label definitions.

    Format is one label per line:

        analysis: makes an argument backed by a specific checkable fact
        hot_take: a confident claim with no support offered
        reaction: an immediate response to something that just happened

    Copy these from your README so the baseline is judged on exactly the
    definitions you wrote. If the file doesn't exist, the label names are used
    on their own — which is a weaker prompt and worth saying so in your README.
    """
    if not Path(path).exists():
        return {}
    definitions = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        label, definition = line.split(":", 1)
        definitions[label.strip()] = definition.strip()
    return definitions


def classify(texts, labels, definitions=None, quiet=False):
    """
    Zero-shot classify every text. Returns a list of predicted label strings.

    The model scores each candidate and the highest wins, so — unlike asking a
    chat model for a label — this can't come back as a sentence, an apology, or
    a label you never defined. That whole class of parsing problem doesn't
    exist here, which is why the brief's warning about replies "in the wrong
    format" doesn't apply to this route.
    """
    from transformers import pipeline

    if not quiet:
        print(f"Loading {ZERO_SHOT_MODEL} (first run downloads ~1.6 GB)…", flush=True)

    classifier = pipeline("zero-shot-classification", model=ZERO_SHOT_MODEL)

    definitions = definitions or {}
    # Give the model the definition where we have one; it discriminates far
    # better on "makes an argument backed by a checkable fact" than on "analysis".
    candidates = [definitions.get(label, label) for label in labels]
    back = {candidate: label for candidate, label in zip(candidates, labels)}

    predictions = []
    for i, text in enumerate(texts, 1):
        if not quiet:
            print(f"  {i}/{len(texts)}", end="\r", flush=True)
        result = classifier(
            str(text),
            candidate_labels=candidates,
            hypothesis_template=HYPOTHESIS,
        )
        predictions.append(back[result["labels"][0]])

    if not quiet:
        print(" " * 30, end="\r")
    return predictions


def log_record(path, record):
    with Path(path).open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=True) + "\n")


def classify_with_review(
    texts, labels, definitions=None, threshold=0.75, quiet=False, log_path=None
):
    """Classify posts and mark predictions that need a human check."""
    from transformers import pipeline

    started = time.perf_counter()
    if log_path:
        log_record(log_path, {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "run_started",
            "input_count": len(texts),
            "threshold": threshold,
        })

    try:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("review threshold must be between 0 and 1")

        if not quiet:
            print(f"Loading {ZERO_SHOT_MODEL} (first run downloads ~1.6 GB)…", flush=True)

        model_started = time.perf_counter()
        classifier = pipeline("zero-shot-classification", model=ZERO_SHOT_MODEL)
        model_load_ms = round((time.perf_counter() - model_started) * 1000, 3)
        definitions = definitions or {}
        candidates = [definitions.get(label, label) for label in labels]
        back = {candidate: label for candidate, label in zip(candidates, labels)}
        records = []
        prediction_total_ms = 0.0

        for i, text in enumerate(texts, 1):
            prediction_started = time.perf_counter()
            try:
                if not quiet:
                    print(f"  {i}/{len(texts)}", end="\r", flush=True)
                result = classifier(
                    str(text),
                    candidate_labels=candidates,
                    hypothesis_template=HYPOTHESIS,
                )
                confidence = float(result["scores"][0])
                record = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": "prediction",
                    "input": str(text),
                    "output": back[result["labels"][0]],
                    "confidence": confidence,
                    "needs_review": confidence < threshold,
                    "duration_ms": round(
                        (time.perf_counter() - prediction_started) * 1000, 3
                    ),
                }
                prediction_total_ms += record["duration_ms"]
                records.append({
                    "text": str(text),
                    "predicted": record["output"],
                    "confidence": confidence,
                    "needs_review": record["needs_review"],
                })
            except Exception as error:
                record = {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": "prediction_error",
                    "input": str(text),
                    "error_type": type(error).__name__,
                    "error": str(error),
                    "duration_ms": round(
                        (time.perf_counter() - prediction_started) * 1000, 3
                    ),
                }
                if log_path:
                    log_record(log_path, record)
                raise
            if log_path:
                log_record(log_path, record)

        if not quiet:
            print(" " * 30, end="\r")
        if log_path:
            total_duration_ms = round((time.perf_counter() - started) * 1000, 3)
            log_record(log_path, {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": "run_completed",
                "output_count": len(records),
                "duration_ms": total_duration_ms,
                "model_load_duration_ms": model_load_ms,
                "prediction_duration_ms": round(prediction_total_ms, 3),
                "logging_and_other_duration_ms": round(
                    total_duration_ms - model_load_ms - prediction_total_ms, 3
                ),
            })
        return records
    except Exception as error:
        if log_path:
            log_record(log_path, {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": "run_error",
                "error_type": type(error).__name__,
                "error": str(error),
                "duration_ms": round((time.perf_counter() - started) * 1000, 3),
            })
        raise


def score(gold, predicted, labels):
    """
    Accuracy and per-label precision / recall / F1.

    Pure arithmetic, no model — which is why the smoke test can check it.
    """
    n = len(gold)
    correct = sum(1 for g, p in zip(gold, predicted) if g == p)

    per_label = {}
    for label in labels:
        tp = sum(1 for g, p in zip(gold, predicted) if g == label and p == label)
        fp = sum(1 for g, p in zip(gold, predicted) if g != label and p == label)
        fn = sum(1 for g, p in zip(gold, predicted) if g == label and p != label)

        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0

        per_label[label] = {
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "support": sum(1 for g in gold if g == label),
        }

    macro_f1 = sum(v["f1"] for v in per_label.values()) / len(labels) if labels else 0.0

    return {
        "n": n,
        "accuracy": correct / n if n else 0.0,
        "f1_macro": macro_f1,
        "per_label": per_label,
    }


def markdown_table(baseline_scores, labels, trained=None):
    """
    The Baseline vs. Trained table your README asks for.

    Pass `trained` — the per-label block out of results.json — to get both
    columns side by side.
    """
    rows = ["| Measure | Baseline | Trained | Difference |",
            "|---|---|---|---|"] if trained else ["| Measure | Baseline |", "|---|---|"]

    def line(name, base, fine=None):
        if fine is None:
            return f"| {name} | {base:.3f} |"
        return f"| {name} | {base:.3f} | {fine:.3f} | {fine - base:+.3f} |"

    rows.append(line("Overall accuracy", baseline_scores["accuracy"],
                     trained["accuracy"] if trained else None))
    rows.append(line("Macro F1", baseline_scores["f1_macro"],
                     trained["f1_macro"] if trained else None))
    for label in labels:
        rows.append(line(
            f"F1 — `{label}`",
            baseline_scores["per_label"][label]["f1"],
            trained["per_label"][label]["f1"] if trained else None,
        ))
    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Zero-shot baseline for TakeMeter. Runs locally, no API key.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--data", default="labels.csv", help="your labelled CSV")
    parser.add_argument("--definitions", default="label_definitions.txt",
                        help="your label definitions, one per line")
    parser.add_argument("--held-out", default="test_split.csv",
                        help="the notebook's held-out posts (written by section 5)")
    parser.add_argument("--n", type=int, default=None,
                        help="cap the number of posts (default: every held-out post)")
    parser.add_argument("--seed", type=int, default=42,
                        help="only used if there's no held-out file to read")
    parser.add_argument("--out", default="baseline_results.json")
    parser.add_argument("--trained", default=None,
                        help="results.json from the notebook, to compare against")
    parser.add_argument("--review-threshold", type=float, default=None,
                        help="also flag predictions below this confidence (0 to 1)")
    parser.add_argument("--review-out", default="review_results.json",
                        help="JSON file for confidence review results")
    parser.add_argument("--log", default="run_log.jsonl",
                        help="append structured run records to this JSONL file")
    args = parser.parse_args()

    try:
        import pandas as pd
    except ImportError:
        print("pandas isn't installed. Run: pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)

    if not Path(args.data).exists():
        print(f"No file at {args.data}. Point --data at your labelled CSV.", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(args.data)
    for column in ("text", "label"):
        if column not in df.columns:
            print(f"{args.data} has no '{column}' column.", file=sys.stderr)
            sys.exit(1)

    labels = sorted(df["label"].dropna().astype(str).str.strip().unique())
    definitions = load_definitions(args.definitions)

    if definitions:
        print(f"Using your definitions from {args.definitions}.")
    else:
        print(f"No {args.definitions} found — using bare label names.")
        print("That's a weaker prompt than the definitions you wrote. Say so in")
        print("your README, or create the file. See --help for the format.\n")

    # Score the posts the notebook tested your trained model on, so both columns
    # of the Baseline vs. Trained table come from the same set. Section 5 writes
    # them to test_split.csv.
    held_out = Path(args.held_out)
    like_for_like = held_out.exists()

    if like_for_like:
        posts = pd.read_csv(held_out)
        available = len(posts)
        print(f"Reading the held-out posts from {held_out} — the same ones your")
        print("trained model was scored on.")
        if args.n and args.n < available:
            posts = posts.head(args.n)
            print()
            print(f"[note] Capped at {args.n} of {available} held-out posts, so your")
            print("       trained numbers cover more posts than this does. The two")
            print("       columns aren't scored on the same set. Drop --n to fix it.")
    else:
        posts = df.sample(n=min(args.n or 30, len(df)), random_state=args.seed)
        print(f"[warn] No {held_out} here, so this is a random sample of {args.data} —")
        print("       mostly posts your model trained on. Baseline vs. Trained then")
        print("       compares two different sets of posts, which is not a")
        print("       comparison. Run the notebook's section 5 to get the file, or")
        print("       say plainly in your README that yours isn't like-for-like.")

    texts = posts["text"].tolist()
    gold = posts["label"].astype(str).str.strip().tolist()

    print(f"\nClassifying {len(texts)} posts across {len(labels)} labels.")
    print("A few seconds each — this is what no fine-tuning costs at runtime.\n")

    review_records = None
    if args.review_threshold is None:
        predicted = classify(texts, labels, definitions)
    else:
        try:
            review_records = classify_with_review(
                texts,
                labels,
                definitions,
                threshold=args.review_threshold,
                log_path=args.log,
            )
        except ValueError as error:
            parser.error(str(error))
        predicted = [record["predicted"] for record in review_records]
    scores = score(gold, predicted, labels)

    print(f"accuracy  {scores['accuracy']:.3f}")
    print(f"macro F1  {scores['f1_macro']:.3f}\n")
    for label, values in scores["per_label"].items():
        print(f"  {label:<16} F1 {values['f1']:.3f}   (n={values['support']})")

    trained = None
    if args.trained and Path(args.trained).exists():
        trained = json.loads(Path(args.trained).read_text())

    print("\n\nPaste this into your README under **Baseline vs. Trained**:\n")
    print(markdown_table(scores, labels, trained))

    output = {
        "model": ZERO_SHOT_MODEL,
        "n": len(texts),
        "seed": args.seed,
        "held_out": like_for_like,
        "used_definitions": bool(definitions),
        "scores": scores,
        "predictions": [
            {"text": t, "gold": g, "predicted": p}
            for t, g, p in zip(texts, gold, predicted)
        ],
    }
    if review_records is not None:
        output["review_threshold"] = args.review_threshold
        output["review_predictions"] = review_records
        Path(args.review_out).write_text(json.dumps({
            "model": ZERO_SHOT_MODEL,
            "review_threshold": args.review_threshold,
            "predictions": review_records,
        }, indent=2), encoding="utf-8")

    Path(args.out).write_text(json.dumps(output, indent=2), encoding="utf-8")

    print(f"\nWrote {args.out}. Commit it.")
    if review_records is not None:
        review_count = sum(record["needs_review"] for record in review_records)
        print(f"Review queue: {review_count}/{len(review_records)} posts")
        print(f"Wrote {args.review_out}.")
    print("\nBefore you look at your trained model's numbers: write one sentence")
    print("predicting where it will beat this. Milestone 1 asks for it, and a")
    print("prediction made after the fact isn't one.")


if __name__ == "__main__":
    main()
