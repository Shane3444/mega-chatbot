from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from box import Box
import yaml
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import ollama
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#Loading Environment variables
load_dotenv()

#Getting paths from yamlfile
with open("chatbot/config.yml", 'r', encoding='utf-8') as yamlfile:
    cfg = Box(yaml.safe_load(yamlfile))   


def create_vectordb():
    loader = DirectoryLoader(cfg.DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    docs = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name = "hkunlp/instructor-base", model_kwargs = {"device" : "cpu"}) 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                    chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(texts, embeddings, persist_directory=cfg.DB_CHROMA_PATH).as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT})
    return vectorstore
    # print("Vector DB setup successfully!")

retriever = create_vectordb()

def ollama_llm(question, context, messages):
    prompt = f"""Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Answer with a maximum of 7 sentences and atleast 3 sentences.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""
    messages.append({"role" : "system", "content" : prompt})
    response = ollama.chat(model = "gemma2:2b", 
                           messages= messages
    )
    return response["message"]["content"]

def rag_chain(question, messages):
    retriever = create_vectordb()    
    context = retriever.invoke(question)
    return ollama_llm(question, context, messages)