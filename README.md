# 🛍️ Shop Assistant Chatbot

An AI-powered smart shopping catalog with a conversational chatbot to help users discover and explore footwear products.

## ✨ Features

- **Product Catalog** — Browse a curated footwear catalog with filters by brand, gender, and price
- **AI Chatbot** — Ask natural language questions like *"Show me Nike shoes under ₹5000"*
- **Shopping Cart** — Add products and simulate checkout
- **Google Images Link** — One-click search for any product's real images
- **Premium UI** — Dark glassmorphic design built with Streamlit

## 🗂️ Project Structure

```
ShopAssistantChatbot/
├── backend/          # FastAPI server (chat + products API)
├── frontend/         # Streamlit UI (app.py)
├── data/             # Product catalog CSV
├── embedding/        # Vector embeddings for semantic search
├── main.py           # Entry point
├── run_servers.bat   # Start both backend and frontend
└── pyproject.toml    # Dependencies
```

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ShopAssistantChatbot.git
   cd ShopAssistantChatbot
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

4. **Run the app**
   ```bash
   run_servers.bat
   ```
   Or manually:
   ```bash
   # Terminal 1 — Backend
   uv run uvicorn backend.main:app --port 8001

   # Terminal 2 — Frontend
   uv run streamlit run frontend/app.py
   ```

5. Open your browser at `http://localhost:8501`

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GOOGLE_API_KEY` | Google Gemini API key for the AI chatbot |

> ⚠️ Never commit your `.env` file. It is already excluded in `.gitignore`.

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI |
| AI / LLM | Google Gemini |
| Embeddings | Sentence Transformers / FAISS |
| Data | CSV + Pandas |
