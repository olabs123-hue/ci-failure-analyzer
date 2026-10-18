"""Evaluate predicted categories against hand-labelled examples."""
def evaluate(examples, predict):
    labels = sorted(set(x["label"] for x in examples))
    counts = {label: {"tp": 0, "fp": 0, "fn": 0} for label in labels}
    correct = 0
    for example in examples:
        predicted = predict(example["log"]).category
        truth = example["label"]
        correct += predicted == truth
        if predicted == truth:
            counts[truth]["tp"] += 1
        else:
            counts[truth]["fn"] += 1
            if predicted in counts:
                counts[predicted]["fp"] += 1
    metrics = {}
    for label, c in counts.items():
        precision = c["tp"] / (c["tp"] + c["fp"]) if c["tp"] + c["fp"] else 0.0
        recall = c["tp"] / (c["tp"] + c["fn"]) if c["tp"] + c["fn"] else 0.0
        metrics[label] = {"precision": round(precision, 4), "recall": round(recall, 4)}
    return {"samples": len(examples), "accuracy": round(correct / len(examples), 4) if examples else None,
            "per_class": metrics}
