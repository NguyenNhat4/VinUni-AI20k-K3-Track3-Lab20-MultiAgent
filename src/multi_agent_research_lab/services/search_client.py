"""Search client abstraction for ResearcherAgent."""

import json
from urllib.request import Request, urlopen

from multi_agent_research_lab.core.config import get_settings
from multi_agent_research_lab.core.schemas import SourceDocument


class SearchClient:
    """Provider-agnostic search client skeleton."""

    def search(self, query: str, max_results: int = 5) -> list[SourceDocument]:
        """Search for documents relevant to a query.

        TODO(student): Implement with Tavily, Bing, SerpAPI, internal docs, or a local mock.
        """

        settings = get_settings()
        if settings.tavily_api_key:
            request = Request(
                "https://api.tavily.com/search",
                data=json.dumps(
                    {"api_key": settings.tavily_api_key, "query": query, "max_results": max_results}
                ).encode(),
                headers={"Content-Type": "application/json"}, method="POST",
            )
            with urlopen(request, timeout=settings.timeout_seconds) as response:
                results = json.load(response).get("results", [])
            return [
                SourceDocument(
                    title=item.get("title", "Untitled"),
                    url=item.get("url"),
                    snippet=item.get("content", ""),
                )
                for item in results
            ]
        return [
            SourceDocument(
                title="Local research note",
                snippet=f"No search provider configured. Research query: {query}",
            )
        ]
