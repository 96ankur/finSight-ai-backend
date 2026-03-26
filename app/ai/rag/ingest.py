from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from .vectorstore import VectorStoreManager


def ingest_pdf(file_path: str, user_id: str):

    # Load document
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Split
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    # Store
    vs = VectorStoreManager(user_id)

    if vs._exists():
        db = vs.load_or_create()
        db.add_documents(chunks)
        vs.save(db)
    else:
        vs.load_or_create(chunks)

    return {"status": "success", "chunks": len(chunks)}
