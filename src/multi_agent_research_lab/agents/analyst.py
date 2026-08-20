"""Analyst agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class AnalystAgent(BaseAgent):
    """Turns research notes into structured insights."""

    name = "analyst"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.analysis_notes`.

        TODO(student): Extract key claims, compare viewpoints, and flag weak evidence.
        """

        response = LLMClient().complete(
            "You are a careful research analyst.",
            f"Analyze these notes for: {state.request.query}\n{state.research_notes}",
        )
        state.analysis_notes = response.content
        state.agent_results.append(AgentResult(agent=AgentName.ANALYST, content=response.content))
        return state
