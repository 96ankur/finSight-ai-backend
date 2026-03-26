from .vectorstore import VectorStoreManager

def get_user_retriever(user_id: str, k=5):
    vs = VectorStoreManager(user_id)
    return vs.get_retriever(k=k)