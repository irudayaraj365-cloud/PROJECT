# V46 Engine AI Chatbot

An offline AI chatbot for answering questions about V46 engine components using RAG.

## Technologies

- Python
- Streamlit
- LangChain
- Ollama
- ChromaDB
- RAG
- PDF Processing

## Features

- Ask questions about V46 engine components
- PDF-based knowledge retrieval
- Local/offline AI
- Streaming responses
- Download answers as PDF

## AI Model

- Qwen2.5 1.5B
- Nomic Embed Text

## How it works

PDF Documents → Text Splitting → Embeddings → ChromaDB → RAG → Ollama → Answer
