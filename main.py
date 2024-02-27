from fastapi import FastAPI
import sqlite3

app = FastAPI()
connection = sqlite3.connect("database.db")


@app.get("/")
async def ping():
    return {"success": True}


