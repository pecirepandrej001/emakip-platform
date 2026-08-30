from src.mlops.evaluation import evaluate_example

def test_evaluation_returns_bounded_scores():
    result = evaluate_example("What is the policy?", "The policy is active.", [{"text":"policy active"}])
    assert 0 <= result.groundedness <= 1
    assert 0 <= result.answer_relevance <= 1
    assert 0 <= result.retrieval_coverage <= 1
