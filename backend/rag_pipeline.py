import os
import numpy as np
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.prompts import PromptTemplate
from backend.config import OPENAI_API_KEY


def cosine_similarity(vec1, vec2):
    vec1, vec2 = np.array(vec1), np.array(vec2)
    if np.linalg.norm(vec1) == 0 or np.linalg.norm(vec2) == 0:
        return 0
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


SYSTEM_INSTRUCTIONS = """
You are an ERP Knowledge Assistant. You must answer user questions strictly using the information from the retrieved documents.

Rules:
1. Only use the provided context (documents) to answer.
2. If the answer is not found in the documents, say: "I don’t know. That question seems unrelated to the uploaded documents."
3. Do not hallucinate facts, definitions, or processes.
4. Be concise, clear, and accurate.
5. If multiple documents provide conflicting answers, indicate this and summarize.
"""


class RAGPipeline:
    def __init__(self):
        self.vectorstore = None
        self.qa_chain = None

    def load_documents(self, folder_path):
        print("[INFO] Loading documents from", folder_path)
        documents = []

        try:
            files = os.listdir(folder_path)
            print("[INFO] Found files:", files)
        except Exception as e:
            print("[ERROR] Could not list directory:", e)
            raise

        for file in files:
            path = os.path.join(folder_path, file)
            if not os.path.isfile(path):
                continue

            print("[INFO] Loading file:", path)
            if file.endswith(".pdf"):
                loader = PyMuPDFLoader(path)
            elif file.endswith(".txt"):
                loader = TextLoader(path)
            elif file.endswith(".docx"):
                loader = UnstructuredWordDocumentLoader(path)
            else:
                print("[WARNING] Unsupported file type:", file)
                continue

            try:
                documents.extend(loader.load())
            except Exception as e:
                print("[ERROR] Failed to load file:", file, "Error:", e)

        print("[INFO] Total documents loaded:", len(documents))

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.vectorstore = FAISS.from_documents(texts, embeddings)

        retriever = self.vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

        prompt = PromptTemplate(
            input_variables=["question", "context"],
            template=SYSTEM_INSTRUCTIONS + "\n\nContext:\n{context}\n\nQuestion:\n{question}\n\nAnswer:"
        )

        self.qa_chain = RetrievalQAWithSourcesChain.from_chain_type(
            llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={
                "prompt": prompt,
                "document_variable_name": "context"
            }
        )

    def answer_question(self, question: str) -> str:
        if not self.qa_chain or not self.vectorstore:
            return "RAG pipeline is not initialized with documents."

        try:
            embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
            question_vector = embeddings.embed_query(question)

            docs_with_scores = self.vectorstore.similarity_search_with_score(question, k=3)
            docs = [doc for doc, score in docs_with_scores]
            doc_texts = [doc.page_content for doc in docs]

            if not doc_texts:
                return "I don’t know. That question seems unrelated to the uploaded documents."

            doc_vectors = embeddings.embed_documents(doc_texts)
            similarities = [cosine_similarity(question_vector, vec) for vec in doc_vectors]

            if not similarities or max(similarities) < 0.75:
                return "I don’t know. That question seems unrelated to the uploaded documents."

            result = self.qa_chain.invoke({"question": question})
            answer = result.get("answer", "").strip()

            if not answer or answer.lower().startswith("i don't know"):
                return "I don’t know. That question seems unrelated to the uploaded documents."

            return answer  # ✅ Final answer, without "Answer generated..." suffix
        except Exception as e:
            print("[ERROR] Failed to answer question:", e)
            return "An error occurred while processing your question."
