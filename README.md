
# 🧠 ERP Knowledge Assistant (GenAI + RAG)

An AI-powered assistant for manufacturing or ERP-heavy teams to interact with documents like:
- SAP or Oracle ERP documentation
- Company policy manuals
- SOPs and production processes

Built with: **Python, Flask, LangChain, FAISS, OpenAI GPT-4o**, and **Tailwind CSS**

---

## 📸 Features

- 📁 Upload ERP documents (PDF, DOCX, TXT — up to 100MB)
- 💬 Ask natural language questions like:
  - “What’s the SOP for downtime events?”
  - “Where do I file a BOM discrepancy?”
- 🧠 Answers come from GPT-4o using document-aware RAG (Retrieval-Augmented Generation)
- 💡 Modern, mobile-friendly UI with chat bubbles and dark mode

---

## 🔧 Tech Stack

- **Backend**: Flask, LangChain, FAISS, OpenAI
- **Frontend**: TailwindCSS, Vanilla JS
- **RAG Logic**: LangChain’s `RetrievalQA` over embedded docs

---

## 🖥️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/erp-knowledge-assistant.git
cd erp-knowledge-assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # (use venv\Scripts\activate on Windows)
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your OpenAI API key

Create a file named `.env` in the `backend` folder:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

> ✅ You can get your key from https://platform.openai.com/account/api-keys

### 5. Run the app

```bash
python app.py
```

The app will be available at: [http://localhost:5000](http://localhost:5000)

---

## ✅ How to Use

1. Upload one or more ERP documents
2. Ask questions in natural language (related to the uploaded content)
3. The assistant will answer ONLY from those documents
4. Clear chat or switch theme using the sidebar

---

## 📂 Folder Structure

```
erp-knowledge-assistant/
│
├── app.py                   # Flask app
├── backend/
│   ├── rag_pipeline.py      # RAG logic (LangChain)
│   ├── utils.py             # Helper functions
│   └── config.py            # OpenAI key config
│
├── templates/
│   └── index.html           # Frontend UI (Tailwind-based)
│
├── uploads/                 # Stores uploaded documents
├── requirements.txt
└── README.md
```

---

## 🙋 Need Help?

If anything breaks, contact `muhammad.nadeem@example.com` or open an issue on the repo.

---

## 📄 License

MIT License – free to use, modify, and deploy.
