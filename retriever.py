import chromadb
import os
from ingest import pdf_to_chunk

client = chromadb.PersistentClient(path='./my_local_db')

collection = None

def index_documents(pdf_path):

    global collection

    collection_name = os.path.basename(pdf_path).replace(".", "_").replace(" ", "_")
    collection = client.get_or_create_collection(name = collection_name)
    chunks = pdf_to_chunk(pdf_path)

    if collection.count() == 0:
        print("Indexing documents...")
        for chunk in chunks:
            collection.add(
                ids = str(chunk['chunk_id']),
                documents=chunk['text'],
                metadatas=[{"page_number":chunk['page'], "source": chunk['source']}],
            )
    else:
        print(f"Collection already has {collection.count()} chunks, skipping indexing.")


    return collection

def retrieve(query, k):

    result = collection.query(query_texts= query, n_results=k)

    return result