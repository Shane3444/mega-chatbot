from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from box import Box
import yaml
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain, RetrievalQA
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import ollama
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#Loading Environment variables
load_dotenv()

#Getting paths from yamlfile
with open("config/config.yml", 'r', encoding='utf-8') as yamlfile:
    cfg = Box(yaml.safe_load(yamlfile))


def create_vectordb():
    loader = DirectoryLoader(cfg.DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)
    docs = loader.load()
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2", model_kwargs = {"device" : "cpu"}) 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=cfg.CHUNK_SIZE,
                                                    chunk_overlap=cfg.CHUNK_OVERLAP)
    texts = text_splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(texts, embeddings, persist_directory=cfg.DB_CHROMA_PATH)
    print("Vector DB setup successfully!")

def setup_rag_chain():
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    llm = Ollama(model = 'gemma2:2b')
    embeddings = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2", model_kwargs = {"device" : "cpu"}) 
    retriever = Chroma(persist_directory=cfg.DB_CHROMA_PATH, embedding_function=embeddings).as_retriever(search_kwargs={'k': cfg.VECTOR_COUNT})
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    print("RAG Chain created succesfully!")
    return rag_chain