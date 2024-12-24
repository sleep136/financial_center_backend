import uvicorn
from fastapi import FastAPI
from db import  create_db_and_tables
app = FastAPI()

user_db = None


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
