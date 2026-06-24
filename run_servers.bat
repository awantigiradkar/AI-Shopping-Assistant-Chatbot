@echo off
echo ===================================================
echo Starting Shop Assistant Chatbot Servers...
echo ===================================================
echo.

rem Start FastAPI Backend on Port 8001
echo [1/2] Launching FastAPI Backend on port 8001...
start "ShopAssistant-Backend" .venv\Scripts\uvicorn backend.main:app --port 8001 --reload

rem Start Streamlit Frontend on Port 8501
echo [2/2] Launching Streamlit Frontend on port 8501...
start "ShopAssistant-Frontend" .venv\Scripts\streamlit run frontend/app.py --server.port 8501

echo.
echo Both servers launched in separate terminal windows!
echo - Backend API: http://127.0.0.1:8001
echo - Frontend UI: http://localhost:8501
echo.
pause
