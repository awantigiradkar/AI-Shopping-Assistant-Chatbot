from fastapi import FastAPI

app = FastAPI(title="Shop Assistant Chatbot")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Shop Assistant Chatbot"}


def main():
    print("Hello from shopassistantchatbot!")


if __name__ == "__main__":
    main()
