from flask import Flask, render_template, request, jsonify
from backend.rag_pipeline import RAGPipeline
from backend.utils import save_uploaded_files
from werkzeug.exceptions import RequestEntityTooLarge
import os

app = Flask(__name__)

# ✅ Set maximum upload size to 100 MB
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB

UPLOAD_FOLDER = "uploads"
rag_pipeline = RAGPipeline()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        uploaded_files = request.files.getlist("files")
        if not uploaded_files:
            return jsonify({"error": "No files uploaded"}), 400

        save_uploaded_files(uploaded_files, UPLOAD_FOLDER)
        rag_pipeline.load_documents(UPLOAD_FOLDER)
        return jsonify({"message": "✅ Files uploaded and processed."})
    except Exception as e:
        return jsonify({"error": f"❌ Failed: {str(e)}"}), 500

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()
        if not question:
            return jsonify({"error": "❗ Empty question"}), 400

        answer = rag_pipeline.answer_question(question)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": f"❌ Error: {str(e)}"}), 500

# ✅ Handle file too large error
@app.errorhandler(RequestEntityTooLarge)
def handle_large_file_error(e):
    return jsonify({"error": "❌ File too large. Maximum allowed size is 100 MB."}), 413

if __name__ == "__main__":
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)

