"""Writer agent skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.schemas import AgentName, AgentResult
from multi_agent_research_lab.core.state import ResearchState
from multi_agent_research_lab.services.llm_client import LLMClient


class WriterAgent(BaseAgent):
    """Produces final answer from research and analysis notes."""

    name = "writer"

    def run(self, state: ResearchState) -> ResearchState:
        """Populate `state.final_answer`.

        TODO(student): Synthesize a clear response with citations or source references.
        """

        citations = " ".join(f"[{i}]" for i, _ in enumerate(state.sources, 1))
        response = LLMClient().complete(
            "You are a concise technical writer. Cite sources by number.",
            f"Question: {state.request.query}\nResearch: {state.research_notes}\n"
            f"Analysis: {state.analysis_notes}",
        )
        state.final_answer = (
            f"{response.content}\n\nSources: {citations}" if citations else response.content
        )
        state.agent_results.append(
            AgentResult(agent=AgentName.WRITER, content=state.final_answer)
        )
        return state
