"""Supervisor / router skeleton."""

from multi_agent_research_lab.agents.base import BaseAgent
from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.state import ResearchState


class SupervisorAgent(BaseAgent):
    """Decides which worker should run next and when to stop."""

    name = "supervisor"

    def run(self, state: ResearchState) -> ResearchState:
        """Update `state.route_history` with the next route.

        TODO(student): Implement routing policy. Suggested steps:
        - Inspect request, current notes, and missing fields.
        - Choose one of: researcher, analyst, writer, done.
        - Enforce max iterations and failure fallback.
        """

        if state.final_answer:
            route = "done"
        elif state.iteration >= get_settings().max_iterations:
            state.errors.append("maximum iterations reached")
            route = "done"
        elif not state.sources:
            route = "researcher"
        elif not state.analysis_notes:
            route = "analyst"
        else:
            route = "writer"
        state.record_route(route)
        state.add_trace_event(self.name, {"next": route})
        return state
