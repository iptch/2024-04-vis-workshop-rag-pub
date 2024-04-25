import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# load environment
load_dotenv()

# setup embedding model and search client
service_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
index_name = os.getenv("AZURE_SEARCH_INDEX")
key = os.getenv("AZURE_SEARCH_KEY")


def get_index():
    # [START get_index]
    client = SearchClient(service_endpoint, index_name, AzureKeyCredential(key))
    results = client.search(search_text="*")
    for result in results:
        print("Data Chunk: " + result["content"])


if __name__ == "__main__":
    get_index()
