from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorStore = Chroma(
      persist_directory="agent/vectorstore",
      embedding_function=embeddings,
      collection_name="policies"
    )


def sync_policy(policy_id: str, title: str, content: str):
   vectorStore.delete(where={"policy_id": policy_id}) 
   splitter = RecursiveCharacterTextSplitter(
      chunk_size = 600,
      chunk_overlap = 80,
      separators=['\n\n','\n'," ",""],
   )
   chunks = splitter.create_documents([content], metadatas=[{'policy_id':policy_id,'title':title}])
   vectorStore.add_documents(chunks);


def delete_policy(policy_id: str):
   vectorStore.delete(where={"policy_id":policy_id})
