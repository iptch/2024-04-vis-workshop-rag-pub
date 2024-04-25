import os
from glob import glob
from langchain.document_loaders import PyPDFLoader
from langchain.docstore.document import Document


def chunk_documents():
    # load pdf documents
    documents = []
    found_documents = glob(os.path.dirname(os.path.abspath(__file__)) + "/data/*pdf")
    if not found_documents:
        print("No PDF Documents found. Check your data.")
        return []
    for pdf in found_documents:
        document = PyPDFLoader(pdf).load()
        documents.append(document)

    # split documents into chunks
    """TODO [Task 1]: Split your documents into document chunks
    Use LangChain TextSplitters https://python.langchain.com/docs/modules/data_connection/document_transformers/ 
    """
    text_splitter = None

    chunks = []
    for document in documents:
        if text_splitter:
            document_chunks = text_splitter.split_documents(document)
            chunks.append(document_chunks)
        else:
            # fallback in case textsplitter was not implemented
            if 'summary' in document[0].metadata['source']:
                chunks.append(
                    [
                        Document(
                            page_content=document[0].page_content,
                            metadata={"source": "unprocessed", "page": 0},
                        )
                    ]
                )
    return chunks
