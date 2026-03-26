import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

BASE_PATH = "vectorstore"

class VectorStoreManager:

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.path = os.path.join(BASE_PATH, user_id)
        self.embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    def _exists(self):
        return os.path.exists(self.path)

    def load_or_create(self, texts=None):
        if self._exists():
            return FAISS.load_local(self.path, self.embedding, allow_dangerous_deserialization=True)
        
        if texts is None:
            raise ValueError("No existing index and no texts provided")

        db = FAISS.from_documents(texts, self.embedding)
        db.save_local(self.path)
        return db

    def save(self, db):
        db.save_local(self.path)

    def get_retriever(self, k=5):
        db = self.load_or_create()
        return db.as_retriever(search_kwargs={"k": k})