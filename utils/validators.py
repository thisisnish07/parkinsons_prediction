def validate_prediction_payload(payload, feature_names):
    errors = []

    if not isinstance(payload, dict):
        return False, ["Payload must be a JSON object."]

    missing = [name for name in feature_names if name not in payload]
    if missing:
        errors.append(f"Missing fields: {', '.join(missing)}")

    extra = [key for key in payload if key not in feature_names]
    if extra:
        errors.append(f"Unexpected fields: {', '.join(extra)}")

    for name in feature_names:
        if name not in payload:
            continue
        value = payload.get(name)
        if not isinstance(value, (int, float)):
            errors.append(f"Field '{name}' must be numeric.")

    return len(errors) == 0, errors
