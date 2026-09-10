from langchain_community.document_loaders import DirectoryLoader, TextLoader
from agent.policy_sync import sync_policy
import os

loader = DirectoryLoader(
    "knowledge_base/",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={'encoding':'utf8'},
    show_progress=True
)

docs = loader.load()

for doc in docs:
    filename = os.path.basename(doc.metadata['source'])   # "return_policy.md"
    policy_id = filename.replace(".md", "")               
    title = policy_id.replace("_", " ").title()           
    sync_policy(policy_id, title, doc.page_content)