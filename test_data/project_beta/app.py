from fastapi import FastAPI

app = FastAPI()

@app.get("/tickets")
def get_tickets():
    return {"message": "Employee support tickets"}