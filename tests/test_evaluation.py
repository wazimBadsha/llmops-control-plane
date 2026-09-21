from llmops_control_plane.evaluation import evaluate_output


def test_evaluation_passes_for_expected_content():
    result = evaluate_output(
        "Version the prompt and keep the model output observable and testable.",
        ["observable", "testable"],
        ["version the prompt"],
        0.75,
    )
    assert result.passed
    assert result.score == 1.0


def test_evaluation_fails_for_missing_phrase():
    result = evaluate_output(
        "The model answered the request.", [], ["version the prompt"], 0.75
    )
    assert not result.passed
