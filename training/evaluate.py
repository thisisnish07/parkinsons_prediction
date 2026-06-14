from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)


def evaluate_model(model, x_val, y_val):
    preds = model.predict(x_val)
    probas = None
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(x_val)[:, 1]

    precision, recall, f1, _ = precision_recall_fscore_support(
        y_val, preds, average="binary"
    )

    metrics = {
        "accuracy": accuracy_score(y_val, preds),
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc_score(y_val, probas) if probas is not None else None,
        "confusion_matrix": confusion_matrix(y_val, preds).tolist(),
        "classification_report": classification_report(y_val, preds, output_dict=True),
    }
    return metrics
