from fastapi import FastAPI

app = FastAPI(title="Complaint Chatbot API")

@app.get("/")
def root():
    return {"message": "Chatbot Service is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
