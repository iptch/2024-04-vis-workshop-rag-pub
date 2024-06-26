import os
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import LLMChain

import streamlit as st
from dotenv import load_dotenv

from langchain.globals import set_debug

set_debug(True)

st.set_page_config(page_title="Task 2", page_icon="ipt_logo.png", layout="wide")
st.markdown("# Task 2: Retrieval Augmented Generation")

load_dotenv()

llm = AzureChatOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    model="gpt-35-turbo",
    streaming=True,
)

embeddings = AzureOpenAIEmbeddings(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    model="text-embedding-ada-002",
)

# TODO [Task 2.2 Data Retrieval] Use different top_k parameters to steer the maximal number of documents retrieved.
# Also compare the vector search versus keywords search. Which one is better? Hint: vector_store_query_mode"""
vector_store = AzureSearch(
    azure_search_endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    azure_search_key=os.getenv("AZURE_SEARCH_KEY"),
    index_name=os.getenv("AZURE_SEARCH_INDEX"),
    embedding_function=embeddings.embed_query,
)
retriever = vector_store.as_retriever()

### Contextualize question ###
contextualize_q_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

### Answer question ###
# TODO [Task 2.3 Prompt Engineering] Add context information to the prompt."""
qa_system_prompt = """You are an assistant for question-answering tasks. \
Use the following pieces of retrieved context to answer the question. \
If you don't know the answer, just say that you don't know. \
Use three sentences maximum and keep the answer concise.\

Question: {input}

"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain_from_docs = (
    RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
    | qa_prompt
    | llm
    | StrOutputParser()
)

rag_chain = create_retrieval_chain(history_aware_retriever, rag_chain_from_docs)

msgs = StreamlitChatMessageHistory(key="chat_history")

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    lambda session_id: msgs,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


def get_response(prompt):
    citation_chunks = None
    for chunk in conversational_rag_chain.stream(
        {"input": prompt}, config={"configurable": {"session_id": "any"}}
    ):
        if "answer" in chunk:
            yield chunk["answer"]
        if "context" in chunk:
            citation_chunks = "" # TODO [Task 2.3 Prompt Engineering] Add Citation to the response"""

    if citation_chunks:
        yield format_citations(citation_chunks)


def format_citations(contexts):
    formatted_citations = []
    for citation in contexts:
        citation_dict = citation.metadata
        citation_dict['source'] = os.path.basename(citation_dict['source'])
        citation_dict['content'] = citation.page_content
        formatted_citations.append(citation_dict)
    return formatted_citations


if len(msgs.messages) == 0:
    msgs.add_ai_message("How can I help you?")

for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(get_response(prompt=prompt))
    if type(response) == str:
        if response not in msgs.messages[-1].content:
            msgs.add_ai_message(response)
    else: # we only take the message but remove any contexts 
        if response[0] not in msgs.messages[-1].content:
            msgs.add_ai_message(response[0])
