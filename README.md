
# ERP Knowledge Assistant (GenAI + RAG)

An AI-powered assistant designed to help manufacturing or ERP-heavy organizations interact with their internal documents, such as:
- SAP or Oracle ERP manuals
- Company policies
- SOPs and production workflows

Built with: **Python, Flask, LangChain, FAISS, OpenAI GPT-4o**, and **Tailwind CSS**

---

## Motivation

This project was developed as part of the technical assessment for the GenAI Solutions Developer role at Syntax. The primary motivation for choosing this idea was its close alignment with Syntax’s core focus on enterprise technology and ERP systems.

Rather than building a generic GenAI demo, the goal was to address a real-world challenge that Syntax’s clients frequently encounter: extracting meaningful insights from large, unstructured ERP documentation. This assistant showcases how Retrieval-Augmented Generation (RAG) can be effectively combined with a lightweight Flask backend to deliver grounded, context-aware answers using client-specific content.

By strictly limiting responses to uploaded documents, the system reflects enterprise expectations around accuracy, traceability, and compliance — key factors in ERP and manufacturing domains. The result is a focused, deployable solution that demonstrates both technical proficiency and business relevance.

---

## Features

- Upload ERP-related documents (PDF, DOCX, TXT — up to 100MB)
- A sample PDF file is included in the `upload/` folder to test the functionality out-of-the-box.
- Example questions you can ask based on the sample document:
  - What are the three main segments of vendor master data?
  - What are the basic principles and objectives of General Ledger Accounting in SAP?
  - What is the difference between a company code and a controlling area?
- Responses are generated using GPT-4o, grounded strictly in the uploaded documents
- Clean and responsive chat-style user interface

---

## Tech Stack

- **Backend**: Flask, LangChain, FAISS, OpenAI
- **Frontend**: TailwindCSS, Vanilla JS
- **RAG Logic**: LangChain’s `RetrievalQA` over embedded document vectors

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/nadeem-aiengineer/erp_assistant.git
cd erp-assistant
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables

Create a `.env` file with your API keys:

```
OPENAI_API_KEY=your_openai_key_here
```

### 4. Run the App

```bash
python app.py
```

---

## Docker Support

To build and run the app with Docker:

```bash
docker compose up --build
```

---

## Notes

- The assistant will only respond if it finds answers grounded in the uploaded documents.
- File size limit: 100MB
- Supported file types: PDF, DOCX, TXT
