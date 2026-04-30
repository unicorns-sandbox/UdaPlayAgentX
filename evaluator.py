def evaluate(local_results):
    if not local_results:
        return 0.2
    if len(local_results) > 0:
        return 0.85
    return 0.5