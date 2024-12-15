import os
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.agents import Tool

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
if not OPENAI_API_KEY:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Ensure both localhost and 127.0.0.1 are allowed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup embeddings and vector store
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = Chroma(collection_name="course_materials", embedding_function=embedding, persist_directory="./embeddings")

# Check if we have any documents, if not, load them
docs = vectorstore.get()['documents']
if len(docs) == 0:
    # Load data from file and insert
    with open("data/sample_course_material.txt", "r", encoding="utf-8") as f:
        content = f.read()
    vectorstore.add_texts([content])

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Define a system prompt that instructs the LLM to answer even if retrieval doesn't help
system_template = """You are MentorBot, an AI assistant that can use the following documents as context. 
If the user asks something that is not well-covered by the documents, you may use your own reasoning and general knowledge to answer.
Always try to provide a helpful, correct, and factual answer. If the question is simple (like 'What is 1+1?'), just answer it directly without needing external context.
If you use information from the documents, cite it if possible."""

human_template = "{question}"

system_message = SystemMessagePromptTemplate.from_template(system_template)
human_message = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message, human_message])

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

def run_code_snippet(snippet: str):
    """
    Safely run a Python code snippet.
    CAUTION: Running arbitrary code is dangerous. This is for demonstration only.
    """
    try:
        result = subprocess.check_output(["python3", "-c", snippet], stderr=subprocess.STDOUT, timeout=3)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Error running code: {e.output.decode('utf-8')}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


code_tool = Tool(
    name="run_python_code",
    description="Executes Python code provided by the user and returns the output.",
    func=run_code_snippet
)

class UserQuery(BaseModel):
    query: str
    code_snippet: str = None

@app.post("/ask")
async def ask_question(user_query: UserQuery):
    code_result = ""
    if user_query.code_snippet:
        code_result = run_code_snippet(user_query.code_snippet)

    prompt_context = ""
    if code_result:
        prompt_context += f"The user ran the following code snippet and got this result:\n{code_result}\n\n"

    final_question = f"{prompt_context}{user_query.query}"

    # Retrieve documents
    retrieved_docs = retriever.get_relevant_documents(final_question)

    if len(retrieved_docs) == 0:
        # No documents found, fallback to direct LLM answer
        direct_answer = llm.predict(f"Question: {final_question}\nPlease answer using your general knowledge.")
        return {"answer": direct_answer.strip(), "code_result": code_result}
    else:
        # Use the QA chain with retrieval
        answer = qa_chain.run(final_question)
        return {"answer": answer.strip(), "code_result": code_result}
