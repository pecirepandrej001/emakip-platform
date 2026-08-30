from dataclasses import dataclass

@dataclass
class EvaluationResult:
    groundedness: float
    answer_relevance: float
    retrieval_coverage: float

def evaluate_example(question: str, answer: str, evidence: list[dict]) -> EvaluationResult:
    q_terms = {t.lower().strip(".,!?") for t in question.split() if len(t) > 3}
    a_terms = {t.lower().strip(".,!?") for t in answer.split() if len(t) > 3}
    evidence_text = " ".join(str(e.get("text", "")) for e in evidence).lower()

    relevance = len(q_terms & a_terms) / max(len(q_terms), 1)
    supported = sum(1 for term in a_terms if term in evidence_text) / max(len(a_terms), 1)
    coverage = min(len(evidence) / 4, 1.0)
    return EvaluationResult(
        groundedness=round(supported, 4),
        answer_relevance=round(relevance, 4),
        retrieval_coverage=round(coverage, 4),
    )
