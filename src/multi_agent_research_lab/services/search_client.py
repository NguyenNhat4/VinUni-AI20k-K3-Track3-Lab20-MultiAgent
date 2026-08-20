"""Search client abstraction for ResearcherAgent."""

import json
from pathlib import Path
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
        corpus_path = Path(settings.offline_corpus_path)
        if settings.tavily_api_key and not corpus_path.exists():
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
        if corpus_path.exists():
            corpus = json.loads(corpus_path.read_text(encoding="utf-8"))
            terms = {term.lower() for term in query.split() if len(term) > 2}
            candidates = []
            knowledge_base = corpus.get("knowledge_base", {})
            for article in knowledge_base.get("knowledge_articles", []):
                haystack = f"{article.get('title', '')} {article.get('content', '')}".lower()
                score = sum(term in haystack for term in terms)
                if score:
                    candidates.append(
                        (score, SourceDocument(
                            title=article.get("title", "Untitled"),
                            snippet=article.get("content", "")[:1200],
                            metadata={"article_id": article.get("article_id"), "source": "offline_corpus"},
                        ))
                    )
            for document in knowledge_base.get("source_documents", []):
                haystack = f"{document.get('title', '')} {document.get('full_text', '')}".lower()
                score = sum(term in haystack for term in terms)
                if score:
                    candidates.append(
                        (score, SourceDocument(
                            title=document.get("title", "Untitled"),
                            url=document.get("provenance_url"),
                            snippet=document.get("full_text", "")[:1200],
                            metadata={"document_id": document.get("document_id"), "source": "offline_corpus"},
                        ))
                    )
            candidates.sort(key=lambda item: item[0], reverse=True)
            return [document for _, document in candidates[:max_results]]
        return [
            SourceDocument(
                title="Local research note",
                snippet=f"No search provider configured. Research query: {query}",
            )
        ]
