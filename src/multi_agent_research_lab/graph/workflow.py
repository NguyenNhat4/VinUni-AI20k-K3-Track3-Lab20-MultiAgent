"""LangGraph workflow skeleton."""

from multi_agent_research_lab.agents import (
    AnalystAgent,
    ResearcherAgent,
    SupervisorAgent,
    WriterAgent,
)
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.state import ResearchState


class MultiAgentWorkflow:
    """Builds and runs the multi-agent graph.

    Keep orchestration here; keep agent internals in `agents/`.
    """

    def build(self) -> object:
        """Create a LangGraph graph.

        TODO(student): Implement nodes, edges, conditional routing, and stop condition.
        Suggested nodes: supervisor, researcher, analyst, writer, optional critic.
        """

        return self

    def run(self, state: ResearchState) -> ResearchState:
        """Execute the graph and return final state.

        TODO(student): Compile graph, invoke it, and convert result back to ResearchState.
        """

        agents = {
            "supervisor": SupervisorAgent(),
            "researcher": ResearcherAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
        }
        while not state.final_answer and state.iteration < get_settings().max_iterations:
            state = agents["supervisor"].run(state)
            route = state.route_history[-1]
            if route == "done":
                break
            state = agents[route].run(state)
        return state
