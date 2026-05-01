from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

class VectorMemory:
    def __init__(self):
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Separate stores
        # self.user_stores = {}      # persistent
        self.session_stores = {}   # temporary

        self.MAX_ITEMS = 50  # prevent unbounded growth

    def _get_store(self, store_dict, key):
        if key not in store_dict:
            store_dict[key] = FAISS.from_texts(
                texts=["init"],
                embedding=self.embedding
            )
        return store_dict[key]

    # Add memory with filtering
    # def add_user_memory(self, user_id: str, text: str):
    #     if not self._is_important(text):
    #         return

    #     store = self._get_store(self.user_stores, user_id)
    #     store.add_texts([text])

    def add_session_memory(self, user_id: str, text: str):
        store = self._get_store(self.session_stores, user_id)
        store.add_texts([text])

    # Retrieve
    def retrieve(self, user_id: str, query: str, k=3):
        results = []

        # if user_id in self.user_stores:
        #     results.extend(
        #         [d.page_content for d in self.user_stores[user_id].similarity_search(query, k=k)]
        #     )

        if user_id in self.session_stores:
            results.extend(
                [d.page_content for d in self.session_stores[user_id].similarity_search(query, k=k)]
            )

        return results

    # Simple importance filter
    # def _is_important(self, text: str):
    #     keywords = ["revenue", "profit", "growth", "preference", "risk"]
    #     return any(k in text.lower() for k in keywords)

    # Cleanup session memory
    def clear_session(self, session_id: str):
        if session_id in self.session_stores:
            del self.session_stores[session_id]