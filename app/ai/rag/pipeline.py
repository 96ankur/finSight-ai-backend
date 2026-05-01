import json
import asyncio
from typing import List, Dict
from collections import defaultdict
from .retriever import Retriever
from .vectorstore import VectorStoreManager

## This implementation is for RAG as memory context not as a tool
class MultiQueryRAG:
    def __init__(self, llm):
        vectoreStoreManager = VectorStoreManager()
        self.vectorestore = vectoreStoreManager 
        self.retriever = Retriever(vectoreStoreManager )
        self.llm = llm

    # Step 1: Query Expansion
    def expand_query(self, query: str):
        prompt = f"""
            Generate 4 diverse search queries for financial retrieval.

            Rules:
            - Each query must be different in intent
            - Include:
            1. specific version
            2. broad version
            3. keyword-style
            4. rephrased version

            Return STRICT JSON:
            ["query1", "query2", "query3", "query4"]

            Query: {query}
        """

        response = self.llm.invoke(prompt)

        try:
            queries = json.loads(response.content)
            queries = list(set([q.strip() for q in queries if q.strip()]))
            return queries[:4]
        except Exception:
            return [query]  # fallback

    # Step 2: Parallel Retrieval
    # def retrieve(self, queries, k=5, filters=None):
    #     all_results = []

    #     for q in queries:
    #         docs = self.vectorstore.similarity_search(q, k=k, filters=filters)
    #         all_results.append(docs)

    #     return all_results

    async def retrieve_async(self, queries, k=5):
        tasks = [
            asyncio.to_thread(self.vectorstore.similarity_search, q, k)
            for q in queries
        ]

        return await asyncio.gather(*tasks)

    # Step 3: Reciprocal Rank Fusion (RRF)
    def reciprocal_rank_fusion(self, results: List[List], k: int = 60):
        scores = defaultdict(float)
        doc_map = {}

        for docs in results:
            for rank, doc in enumerate(docs):
                doc_id = hash(doc.page_content)
                score = 1 / (k + rank)

                scores[doc_id] += score
                doc_map[doc_id] = doc

        # sort by score
        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [doc_map[doc_id] for doc_id, _ in ranked_docs]

    # Step 4: Deduplication (simple)
    def deduplicate(self, docs):
        seen = set()
        unique_docs = []

        for doc in docs:
            content = doc.page_content.strip()
            if content not in seen:
                seen.add(content)
                unique_docs.append(doc)

        return unique_docs

    def compress_docs(self, docs):
        compressed = []

        for doc in docs:
            prompt = f"""
                Summarize the following financial text in 2-3 lines.
                Keep only key facts.

                Text:
                {doc.page_content}
            """

            response = self.llm.invoke(prompt)
            doc.page_content = response.content.strip()
            compressed.append(doc)

        return compressed

    # Final Pipeline
    def run(self, query: str, top_k: int = 5):
        expanded_queries = self.expand_query(query)

        retrieved = self.retrieve(expanded_queries, k=top_k)

        fused = self.reciprocal_rank_fusion(retrieved)

        deduped = self.deduplicate(fused)

        compressed = self.compress_docs(deduped[:top_k])

        return compressed[:top_k]