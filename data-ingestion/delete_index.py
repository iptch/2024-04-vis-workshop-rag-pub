import os
from dotenv import load_dotenv
from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential

# load environment
load_dotenv()

# setup embedding model and search client
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
index_name = os.getenv("AZURE_SEARCH_INDEX")
key = os.getenv("AZURE_SEARCH_KEY")


def delete_index():
    # [START delete_index]
    client = SearchIndexClient(service_endpoint, AzureKeyCredential(key))
    client.delete_index(index_name)


if __name__ == "__main__":
    delete_index()
