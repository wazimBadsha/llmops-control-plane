from .schemas import EvaluationResult


def evaluate_output(
    output: str,
    expected_keywords: list[str],
    required_phrases: list[str],
    threshold: float,
) -> EvaluationResult:
    lowered = output.lower()
    keyword_checks = {keyword: keyword.lower() in lowered for keyword in expected_keywords}
    phrase_checks = {phrase: phrase.lower() in lowered for phrase in required_phrases}
    keyword_recall = sum(keyword_checks.values()) / len(keyword_checks) if keyword_checks else 1.0
    phrase_recall = sum(phrase_checks.values()) / len(phrase_checks) if phrase_checks else 1.0
    score = (keyword_recall + phrase_recall) / 2
    checks = {**{f"keyword:{k}": v for k, v in keyword_checks.items()}, **{f"phrase:{k}": v for k, v in phrase_checks.items()}}
    return EvaluationResult(
        score=score,
        passed=score >= threshold,
        keyword_recall=keyword_recall,
        phrase_recall=phrase_recall,
        checks=checks,
    )
