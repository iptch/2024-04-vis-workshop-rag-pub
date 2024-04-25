import os
from dotenv import load_dotenv
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchField,
    SearchFieldDataType,
    SearchableField,
)
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from langchain_openai import AzureOpenAIEmbeddings
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
)

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

search_client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
vector_search = VectorSearch(
    profiles=[
        VectorSearchProfile(
            name="my-vector-config", algorithm_configuration_name="my-algorithms-config"
        )
    ],
    algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config")],
)

# define index fields
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchField(name="metadata", type=SearchFieldDataType.String),
    SearchableField(
        name="content", type=SearchFieldDataType.String, analyzer_name="en.lucene"
    ),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="my-vector-config",
    ),
]

# create index
index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
search_client.create_index(index)

print("Yay, you created your own search index! Called ", index_name)
