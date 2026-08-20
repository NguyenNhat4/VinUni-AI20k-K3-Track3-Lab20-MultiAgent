from multi_agent_research_lab.services.search_client import SearchClient


def test_search_client_reads_default_offline_corpus() -> None:
    results = SearchClient().search("single agent multi-agent research architecture", 3)

    assert results
    assert len(results) <= 3
    assert results[0].metadata["source"] == "offline_corpus"
