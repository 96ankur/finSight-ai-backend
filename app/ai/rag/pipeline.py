from .retriever import get_user_retriever

def run_rag(query: str, user_id: str, llm):

    retriever = get_user_retriever(user_id)
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    return context