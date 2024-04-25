import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from langchain_community.vectorstores.azuresearch import AzureSearch
from azure.search.documents import SearchClient
from langchain_openai import AzureOpenAIEmbeddings
from chunk_documents import chunk_documents
from openai import AzureOpenAI

# load environment
load_dotenv()

# setup embedding model and search client
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
index_name = os.getenv("AZURE_SEARCH_INDEX")
key = os.getenv("AZURE_SEARCH_KEY")

embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_EMBEDDING_MODEL"),
    openai_api_version=os.getenv("OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
)

search_client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))

# openai client
azure_openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("OPENAI_API_VERSION"),
    azure_deployment=os.getenv("AZURE_EMBEDDING_MODEL"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

# setup vector store
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=service_endpoint,
    azure_search_key=key,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)

# chunk documents
chunked_documents = chunk_documents()

# prepare ingestion
for doc in chunked_documents:
    vector_store.add_documents(documents=doc)

print("You have ingested %s pdf resources" % len(chunked_documents))
