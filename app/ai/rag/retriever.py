from typing import List, Dict, Any


class Retriever:
    def __init__(self, vectorstore):
        """
        vectorstore: instance of VectorStore
        """
        self.vectorstore = vectorstore

    # Semantic Retrieval
    def semantic_search(
        self,
        query: str,
        k: int = 5,
        filters: Dict[str, Any] = None,
    ) -> List:
        return self.vectorstore.similarity_search(
            query=query,
            k=k,
            filters=filters,
        )

    # Keyword Retrieval (Fallback / Hybrid)
    def keyword_search(
        self,
        query: str,
        k: int = 5,
        filters: Dict[str, Any] = None,
    ) -> List:
        """
        NOTE:
        Currently using vector DB fallback.
        Later upgrade to BM25 / Elasticsearch.
        """

        try:
            # Simple fallback: reuse semantic search
            return self.vectorstore.similarity_search(
                query=query,
                k=k,
                filters=filters,
            )
        except Exception as e:
            print(f"[Retriever] keyword_search error: {e}")
            return []

    # 🔹 Hybrid Retrieval (CORE)
    def hybrid_search(
        self,
        query: str,
        k: int = 5,
        filters: Dict[str, Any] = None,
    ) -> List:
        """
        Combine semantic + keyword results
        """

        semantic_docs = self.semantic_search(query, k, filters)
        keyword_docs = self.keyword_search(query, k, filters)

        # Combine
        combined = semantic_docs + keyword_docs

        return combined

    # Multi-query Retrieval Helper
    def multi_query_search(
        self,
        queries: List[str],
        k: int = 5,
        filters: Dict[str, Any] = None,
    ) -> List[List]:
        """
        Returns list of results per query
        Used by RAG pipeline before fusion
        """

        all_results = []

        for q in queries:
            docs = self.hybrid_search(q, k=k, filters=filters)
            all_results.append(docs)

        return all_results

    # 🔹 Utility: Deduplicate Documents
    @staticmethod
    def deduplicate(docs: List) -> List:
        seen = set()
        unique_docs = []

        for doc in docs:
            content = doc.page_content.strip()

            if content not in seen:
                seen.add(content)
                unique_docs.append(doc)

        return unique_docs