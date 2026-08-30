import pytest
from src.agents.nodes.router_agent import router_agent

@pytest.mark.asyncio
async def test_workflow_routing_without_external_services():
    state = router_agent({"question":"How many documents are in the platform?", "steps":[]})
    assert state["route"] == "sql"
    assert state["steps"]
