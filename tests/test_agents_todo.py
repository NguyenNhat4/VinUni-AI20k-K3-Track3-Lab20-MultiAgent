from multi_agent_research_lab.agents import SupervisorAgent
from multi_agent_research_lab.core.schemas import ResearchQuery
from multi_agent_research_lab.core.state import ResearchState


def test_supervisor_routes_missing_sources_to_researcher() -> None:
    state = ResearchState(request=ResearchQuery(query="Explain multi-agent systems"))
    result = SupervisorAgent().run(state)
    assert result.route_history == ["researcher"]


def test_supervisor_routes_ready_state_to_writer() -> None:
    state = ResearchState(
        request=ResearchQuery(query="Explain multi-agent systems"),
        sources=[{"title": "Source", "snippet": "Evidence"}],
        analysis_notes="Evidence is relevant.",
    )
    result = SupervisorAgent().run(state)
    assert result.route_history == ["writer"]
