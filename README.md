# VIS Workshop 2024 RAG
Welcome to the VIS Workshop 2024! In this workshop, you will collect hands-on experience with large language model (LLM) and retrieval augemented generation (RAG). 

## Task 0: Setup
First things first, let's setup your system. 

#### Clone the repo and set up virtual environment
```bash
git clone git@github.com:iptch/2024-04-vis-workshop-rag.git
cd 2024-04-vis-workshop-rag
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Set the environment
Create a `.env` file and add the following variables
````
OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_ENDPOINT=https://oai-vis-workshop-genai-chn-001.openai.azure.com/
AZURE_OPENAI_API_KEY=<insert-openai-key>
AZURE_SEARCH_ENDPOINT=https://srch-vis-workshop-genai-chn-001.search.windows.net
AZURE_SEARCH_KEY=<insert-search-api-key>
AZURE_SEARCH_INDEX=<insert-your-index-name-of-choice>
AZURE_EMBEDDING_MODEL=text-embedding-ada-002
````

#### Start GUI
In this workshop we use StreamLit as a light-weighted GUI. In this way, you can focus mainly on coding and engineering on the AI task and visualize your results in a pretty GUI ;-)

````
streamlit run workshop.py
````
Then open the provided localhost url in the browser et voilà.

## Task 1: Prompt Engineering
Now that you are all set up, we can start with prompt engineering. Prompt engineering is the task to formulate your question optimally to receive your expected answer. Navigate to "Task 1" in your GUI. Click on `Submit` and see what ChatGPT responds. There is an mistake. Adapt the prompt, so that you get the correct answer.  

## Task 2: RAG
Now, we would want to advance and use RAG. We have provided you already some code to perform RAG, but it is not yet optimal. You have all RAG components: data ingestion, data retrieval and the LLM part. There are three subtasks, where you can individually improve your RAG. 

### 2.1 Data Ingestion
As a starting point, you need to have data. These are often unstructured, such as pdf document, as well as large. 
In this task, you will create a search index for RAG. An vector store will be created where you can ingest your data to. This data needs to be chunked to make it available for RAG. 

<b>a. create an search index</b>
An search index describes how the data stored in the vector store is structured. Each field of the search index can be configured, e.g. make it searchable, retrievable etc. 
To create your own search index go to your `.env` file and insert a name for `AZURE_SEARCH_INDEX` for example `knowledge-index-<ethz shortname>`

Then run
````bash
python data-ingestion/create_your_index.py
````

This is uploaded to Azure Sandbox and you should find your newly created index [here](https://portal.azure.com/#@ipt.ch/resource/subscriptions/da12d467-03ae-4675-aa29-d3b26fdbd2cc/resourceGroups/rg-vis-genai-workshop-chn-01/providers/Microsoft.Search/searchServices/srch-vis-workshop-genai-chn-001/indexes).

**b. chunk data**

**Task**: Your task is to write code to chunk your documents into smaller parts. For that check out `chunk_documents.py` (see the TODO). Try out different option. Which one is a good one? 

**c. ingest data to search index**
To upload document chunks to the search index, run
````bash
python data-ingestion/run_ingestion.py
````

You can check your chunks in your search index [here](https://portal.azure.com/#@ipt.ch/resource/subscriptions/da12d467-03ae-4675-aa29-d3b26fdbd2cc/resourceGroups/rg-vis-genai-workshop-chn-01/providers/Microsoft.Search/searchServices/srch-vis-workshop-genai-chn-001/indexes). To see the document chunks, you need to click "search".


### 2.2 Data Retrieval
Here, we have a closer look in the retrieval step, where we retrieve the relevant documents for answering the question solely based on a search. Investigate what the effect is if you change the maximal number of documents (parameter `k`) as well as compare different search methods (e.g. keyword search vs. vector search). 

**Task**: Go to `pages/task2.py` and search for `TODO [2.2 Data Retrieval]`. You can validate your changes in the langchain output in your terminal. You should also see difference in the results in the GUI. Just restart the GUI using `streamlit run workshop.py`.

### 2.3 Prompt Engineering
In this task, you should try to optimize the prompt in such a way, that the answer improves with the retrieved contexts. Change the prompt so that the contexts is provided. 

**Task**: Go to `pages/task2.py` and search for `TODO [2.3 Prompt Engineering]`. Again, you can see the results either in the console output or directly in the GUI using  `streamlit run workshop.py`.

## Bonus: Challenge
(TODO)
