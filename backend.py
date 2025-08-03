from fastapi import FastAPI, Request
from claude_client import call_claude
from messages.agreeable_message import AgreeeableMessage

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "active"}

@app.post("/review_document")
async def review_document(request: Request):
    data = await request.json()

    document_text = data.get("text", "")
    if not document_text:
        return {"error": "No 'text' field provided in JSON."}

    user_msg = AgreeeableMessage(document_text)

    result = call_claude([user_msg])

    return result
        
