# Shop Assistant Chatbot
An AI-powered smart shopping catalog with a conversational chatbot (RAG) to help users discover and explore footwear products. Powered by FastAPI, Streamlit, Pinecone Vector Database, Google Gemini, and MySQL.

---
## Live Application Links
* **Direct Application**: [https://ai-shopping-assistant-chatbot.streamlit.app/]
---
## Features
- **Product Catalog** — Browse a curated footwear catalog with filters by brand, gender, and price.
- **AI Chatbot** — Ask natural language questions like *"Show me Nike shoes under ₹5000"*.
- **Smart Catalog Filters** — Chat recommendations are dynamically filtered by the UI's brand and gender selections.
- **Shopping Cart** — Add products and simulate checkout with interactive toasts.
- **Google Images Link** — One-click search for any product's real images.
- **Premium UI** — Dark glassmorphic design built with Streamlit and styled with modern fonts.
---
## Project Structure
```text
ShopAssistantChatbot/
├── backend/            # FastAPI server (chat + products API)
│   ├── db/             # MySQL database connection adapter
│   ├── routes/         # API routes (chat, products)
│   └── services/       # Gemini LLM and Pinecone Vector Store integrations
├── frontend/           # Streamlit UI (app.py)
├── data/               # Product catalog CSV & database loader script
├── embedding/          # Scripts to sync embeddings to Pinecone index
├── requirements.txt    # Python dependencies for deployment
├── pyproject.toml      # Poetry/uv package manager configuration
└── run_servers.bat     # Windows batch script to launch servers locally
```
## Environment Variables

Create a `.env` file in the project root folder and add the following variables:

| Variable | Description | Default (Local) |
|----------|-------------|-----------------|
| `GOOGLE_API_KEY` | Google Gemini API key for chatbot and embeddings | **Required** |
| `PINECONE_API_KEY` | Pinecone API key for product catalog search | **Required** |
| `DB_PASSWORD` | Password for your MySQL database | **Required** |
| `DB_HOST` | Hostname of the MySQL server | `localhost` |
| `DB_PORT` | Port number of the MySQL server | `3306` |
| `DB_USER` | Username of the MySQL server | `root` |
| `DB_DATABASE` | Database name on the MySQL server | `shopassistantchatbot` |
| `BACKEND_URL` | URL of the API backend (used by the frontend) | `http://127.0.0.1:8001` |

### Example `.env`

```env
GOOGLE_API_KEY=your_google_api_key
PINECONE_API_KEY=your_pinecone_api_key

DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_DATABASE=shopassistantchatbot

BACKEND_URL=http://127.0.0.1:8001
```

> **Important:** Never commit your `.env` file to version control. It is excluded from Git using `.gitignore`.

## Local Development Setup

### Prerequisites

Before running the application locally, ensure the following are installed and configured:

- **Python 3.10+**
- **MySQL Server** running on `localhost:3306`
- A **Pinecone** index named `shop-product-catalog` populated with product embeddings

### Verify Prerequisites

```bash
python --version
mysql --version
```

Ensure your MySQL server is running and that the Pinecone index `shop-product-catalog` is available and contains the required embeddings before starting the application.

## Setup Steps

### 1. Clone the Repository

```bash
git clone https://github.com/awantigiradkar/AI-Shopping-Assistant-Chatbot.git
cd AI-Shopping-Assistant-Chatbot
```

### 2. Install Dependencies

Using **uv**:

```bash
uv sync
```

Or using **pip**:

```bash
pip install -r requirements.txt
```

### 3. Populate the Local MySQL Database

1. Create a local MySQL database named `shopassistantchatbot`.
2. Configure your `.env` file and set the `DB_PASSWORD` value.
3. Run the data insertion script:

```bash
python data/data_insertion.py
```

### 4. Launch the Application

You can either double-click `run_servers.bat` on Windows or start the services manually in separate terminals.

#### Terminal 1 — Backend API

```bash
uv run uvicorn backend.main:app --port 8001 --reload
```

#### Terminal 2 — Frontend (Streamlit)

```bash
uv run streamlit run frontend/app.py
```

### 5. Access the Application

Open your browser and navigate to:

```text
http://localhost:8501
```

---

## Cloud Deployment Configuration

This project is pre-configured for cloud deployment.

### Infrastructure

| Component | Service |
|------------|---------|
| Database | Aiven MySQL (Free Tier) |
| Backend API | Render Web Service |
| Frontend UI | Streamlit Cloud |

---

## Render Configuration

### Build Command

```bash
uv pip install -r requirements.txt
```

### Start Command

```bash
uv run uvicorn backend.main:app --host 0.0.0.0 --port 10000
```

## Streamlit Cloud Configuration

### Main File Path

```text
frontend/app.py
```

### Advanced Settings (Secrets)

```toml
BACKEND_URL = "https://your-backend-api.onrender.com"
```

Replace the URL with the public endpoint of your deployed Render backend service.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install foobar
```

## Usage

```python
import foobar

# returns 'words'
foobar.pluralize('word')

# returns 'geese'
foobar.pluralize('goose')

# returns 'phenomenon'
foobar.singularize('phenomena')
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
