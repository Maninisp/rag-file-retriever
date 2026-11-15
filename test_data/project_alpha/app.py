from fastapi import FastAPI

app = FastAPI()

@app.get("/appointments")
def get_appointments():
    return {"message": "Pet appointments"}