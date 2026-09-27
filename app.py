import streamlit as st

from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_chroma import Chroma

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from io import BytesIO


# -----------------------------
# PAGE TITLE
# -----------------------------

st.title("V46 Engine Components Chatbot")

st.write("Ask questions about V46 engine components.")


# -----------------------------
# EMBEDDING MODEL
# -----------------------------

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# -----------------------------
# CHROMA DATABASE
# -----------------------------

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)


# -----------------------------
# AI MODEL
# -----------------------------

llm = OllamaLLM(
    model="qwen2.5:1.5b"
)


# -----------------------------
# QUESTION BOX
# -----------------------------

question = st.text_input(
    "Ask your V46 engine question:"
)


# -----------------------------
# WHEN USER ENTERS QUESTION
# -----------------------------

if question:

    # Search V46 documents
    results = db.similarity_search(
        question,
        k=2
    )

    # Get text from documents
    context = "\n\n".join(
        document.page_content
        for document in results
    )


    # AI prompt
    prompt = f"""
You are a V46 engine technical assistant.

Answer the user's question using ONLY the information
provided in the V46 documents.

If the information is not available in the documents,
say:

"I could not find this information in the V46 documents."

Do not invent technical specifications.

V46 DOCUMENT INFORMATION:

{context}

USER QUESTION:

{question}

Give a clear and simple answer.
"""


    # -----------------------------
    # SHOW ANSWER
    # -----------------------------

    st.subheader("Answer")


    # Empty box for streaming
    response_box = st.empty()

    full_response = ""


    # Stream AI response
    for chunk in llm.stream(prompt):

        full_response += chunk

        response_box.markdown(full_response)


    # -----------------------------
    # CREATE PDF
    # -----------------------------

    pdf = BytesIO()

    document = SimpleDocTemplate(
        pdf,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    content = []


    # PDF title
    content.append(
        Paragraph(
            "V46 Engine Components Chatbot",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )


    # Question
    content.append(
        Paragraph(
            "<b>Question:</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            question,
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 15)
    )


    # Answer
    content.append(
        Paragraph(
            "<b>Answer:</b>",
            styles["Heading2"]
        )
    )

    # Convert line breaks
    pdf_answer = full_response.replace(
        "\n",
        "<br/>"
    )

    content.append(
        Paragraph(
            pdf_answer,
            styles["Normal"]
        )
    )


    # Build PDF
    document.build(content)

    pdf.seek(0)


    # -----------------------------
    # DOWNLOAD BUTTON
    # -----------------------------

    st.download_button(
        label="📄 Download Answer as PDF",

        data=pdf,

        file_name="V46_Chatbot_Answer.pdf",

        mime="application/pdf"
    )
