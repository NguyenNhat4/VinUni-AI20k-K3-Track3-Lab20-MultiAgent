"""Researcher agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.search_client import SearchClient


class ResearcherAgent(BaseAgent):
    """Collects sources and creates concise research notes."""

    name = "researcher"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.sources` and `state.research_notes`.

        TODO(student): Implement search, source filtering, citation capture, and notes.
        """

        state.sources = SearchClient().search(state.request.query, state.request.max_sources)
        state.research_notes = "\n".join(
            f"[{i}] {source.title}: {source.snippet}"
            for i, source in enumerate(state.sources, 1)
        )
        state.agent_results.append(
            AgentResult(agent=AgentName.RESEARCHER, content=state.research_notes)
        )
        return state
