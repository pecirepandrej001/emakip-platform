import asyncio
from src.agents.graph import run_agent
from src.mlops.evaluation import evaluate_example

DATASET = [
    {"question": "According to the uploaded policy, what is the retention period?"},
    {"question": "How many documents are in the platform?"},
]

async def main():
    scores = []
    for item in DATASET:
        state = await run_agent(item["question"], "evaluation@emakip.local")
        result = evaluate_example(item["question"], state.get("answer",""), state.get("evidence",[]))
        scores.append(result)
        print(item["question"], result)
    if scores:
        print("Average groundedness:", sum(s.groundedness for s in scores)/len(scores))

if __name__ == "__main__":
    asyncio.run(main())
