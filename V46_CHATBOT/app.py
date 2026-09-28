from flask import Flask, request, render_template_string
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import requests
import traceback

app = Flask(__name__)

# -----------------------------
# LOAD CHROMA DATABASE
# -----------------------------

print("Starting V46 Chatbot...")
print("Loading Chroma database...")

try:
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    print("CHROMA DATABASE: OK")

except Exception as e:
    db = None
    print("CHROMA ERROR:")
    print(e)
    traceback.print_exc()


# -----------------------------
# HTML
# -----------------------------

HTML = """
<!DOCTYPE html>

<html>

<head>

<title>V46 Engine AI Chatbot</title>

<style>

body {
    background: #080808;
    color: white;
    font-family: Arial;
    padding: 40px;
}

.container {
    max-width: 900px;
    margin: auto;
}

h1 {
    color: #00ffff;
    text-align: center;
}

textarea {
    width: 100%;
    height: 120px;
    background: #111;
    color: white;
    border: 2px solid #00ffff;
    border-radius: 10px;
    padding: 15px;
    font-size: 16px;
}

button {
    margin-top: 15px;
    padding: 14px 30px;
    background: #00ffff;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
}

.answer {
    margin-top: 30px;
    padding: 20px;
    background: #111;
    border: 1px solid #00ffff;
    border-radius: 10px;
    white-space: pre-wrap;
}

.status {
    margin-top: 15px;
    color: #00ff88;
}

</style>

</head>

<body>

<div class="container">

<h1>V46 ENGINE AI CHATBOT</h1>

<form method="POST">

<textarea
name="question"
placeholder="Ask about V46 engine components..."
required>{{ question }}</textarea>

<br>

<button type="submit">ASK AI</button>

</form>

<div class="status">
{{ status }}
</div>

{% if answer %}

<div class="answer">

<h3>AI ANSWER</h3>

{{ answer }}

</div>

{% endif %}

</div>

</body>

</html>
"""


# -----------------------------
# HOME
# -----------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    question = ""
    answer = ""
    status = "Ready"

    if request.method == "POST":

        question = request.form.get("question", "").strip()

        if not question:

            return render_template_string(
                HTML,
                question="",
                answer="",
                status="Please enter a question."
            )

        print("\n==============================")
        print("QUESTION:")
        print(question)
        print("==============================")

        # -------------------------
        # CHECK CHROMA
        # -------------------------

        if db is None:

            answer = "Chroma database could not be loaded."

            return render_template_string(
                HTML,
                question=question,
                answer=answer,
                status="Database error"
            )

        try:

            print("Searching V46 documents...")

            results = db.similarity_search(
                question,
                k=0
            )

            print("Chroma search completed.")

            if not results:

                answer = (
                    "I could not find this information "
                    "in the V46 documents."
                )

                return render_template_string(
                    HTML,
                    question=question,
                    answer=answer,
                    status="No documents found"
                )

            # -------------------------
            # CREATE CONTEXT
            # -------------------------

            context = ""

            for document in results:

                context += document.page_content
                context += "\n\n"

            print("Context created.")

            # -------------------------
            # AI PROMPT
            # -------------------------

            prompt = f"""
You are a V46 engine technical assistant.

Answer the user's question using ONLY the V46
technical document information below.

If the information is not available, say:

I could not find this information in the V46 documents.

Do not invent technical specifications.

Do not use outside knowledge.

V46 DOCUMENT INFORMATION:

{context}

USER QUESTION:

{question}

Give a clear and simple answer.
"""

            print("Sending request to Ollama...")

            # -------------------------
            # OLLAMA
            # -------------------------

            response = requests.post(

                "http://127.0.0.1:11434/api/generate",

                json={
                    "model": "qwen2.5:1.5b",
                    "prompt": prompt,
                    "stream": False
                },

                timeout=300
            )

            print("Ollama response received.")

            response.raise_for_status()

            data = response.json()

            answer = data.get("response", "")

            if not answer:

                answer = "Ollama returned an empty answer."

            print("AI ANSWER:")
            print(answer)

            status = "AI response generated successfully."

        except requests.exceptions.ConnectionError:

            answer = """
Cannot connect to Ollama.

Please make sure Ollama is running.
"""

            status = "Ollama connection error"

            print("OLLAMA CONNECTION ERROR")

        except requests.exceptions.Timeout:

            answer = """
Ollama took too long to respond.

The model may still be processing the question.
"""

            status = "Ollama timeout"

            print("OLLAMA TIMEOUT")

        except Exception as e:

            answer = "An error occurred:\n\n" + str(e)

            status = "Error"

            print("\nERROR:")
            traceback.print_exc()

    return render_template_string(
        HTML,
        question=question,
        answer=answer,
        status=status
    )


# -----------------------------
# START FLASK
# -----------------------------

if __name__ == "__main__":

    print("\n================================")
    print("V46 ENGINE AI CHATBOT")
    print("================================")

    print("\nOpen:")
    print("http://127.0.0.1:5000")

    print("\nMake sure Ollama is running.")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )