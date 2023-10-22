from dotenv import load_dotenv, find_dotenv
from langchain.document_loaders import DirectoryLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Milvus
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain import hub
import os


MILVUS_HOST = 'localhost'
MILVUS_PORT = '19530'

_ = load_dotenv(find_dotenv())

# set `<your-endpoint>` and `<your-key>` variables with the values from the Azure portal
openai_api_key = os.getenv("OPEN_API_KEY")

# loader = DirectoryLoader('../data', glob='**/*.csv')
loader = CSVLoader(file_path='../data/data-2.csv')
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = splitter.split_documents(documents=documents)

# Set up an embedding model to convert document chunks into vector embeddings.
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Set up a vector store used to save the vector embeddings. Here we use Milvus as the vector store.
store = Milvus.from_documents(
    documents=splits,
    embedding=embeddings,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT}
)
retriever = store.as_retriever()

rag_prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)
rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
)

response = rag_chain.invoke("")
print(response)






