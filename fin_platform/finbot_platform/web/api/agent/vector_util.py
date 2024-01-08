from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.schema import Document
from langchain.vectorstores import FAISS
import os
from finbot_platform.settings import settings

class VectorSupport:
    def __init__(self,vectordb_name:str="faiss_vectordb",embedding_fn=OpenAIEmbeddings(openai_api_key=settings.openai_api_key)):
        print(f"current: {os.getcwd()}")
        self.embeddings = embedding_fn
        self.vectordb_name = vectordb_name

    def create_vectordb(self,contents,metadatas) -> None:
        vector_dict = dict(zip(contents, metadatas))
        docs = [
            Document(page_content=vector_column, metadata=metadata)
            for vector_column,metadata in vector_dict.items()
        ]
        vector_db = FAISS.from_documents(docs, self.embeddings)
        if os.path.exists(self.vectordb_name):
            print("INFO: FAISS VECTOR DB ALREADY EXIST. INSERTING DATA....")
            db = FAISS.load_local(self.vectordb_name, self.embeddings)
            db.merge_from(vector_db)
            print("INFO: Vectors Created Successfully")
            db.save_local(self.vectordb_name)
            return None
        vector_db.save_local(self.vectordb_name)
        print("INFO: Vectors Created Successfully")

    def get_retriever(self):
        return FAISS.load_local(self.vectordb_name, self.embeddings).as_retriever()

    def query_vector(self,query) -> str | None:
        vector_db = FAISS.load_local(self.vectordb_name, self.embeddings)
        try:
            docs = vector_db.similarity_search_with_score(query,k=1)
        except TypeError as e:
            print(e)
            return None
        try:
            doc = docs[0]
        except TypeError as e:
            print(e)
            return None
        if doc[-1]<0.2:
            print(doc[0])
            print(doc[-1])
            return doc[0].metadata
        return None
