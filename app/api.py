from fastapi import FastAPI
from .assistant_service import run_assistant, chat_history, router

app = FastAPI()


@app.post("/chat")
def chat(msg: str):
    return run_assistant(msg)


@app.get("/history")
def history():
    return {"history": chat_history}


@app.get("/reminders")
def get_reminders():
    return {"reminders": router.reminders}