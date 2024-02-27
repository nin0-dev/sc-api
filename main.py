from fastapi import FastAPI
import util
import sqlite3

app = FastAPI()
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


@app.get("/")
async def ping():
    return {"success": True}


@app.get("/list/create")
async def create_list():
    # Get list code
    list_code = util.get_random_string(8)
    # Add it to database
    cursor.execute("CREATE TABLE IF NOT EXISTS listcodes (list_code TEXT);")
    cursor.execute(f"INSERT INTO listcodes VALUES ('{list_code}');")
    connection.commit()
    print(f"Created list {list_code}")
    # Respond
    return {"success": True, "list_code": list_code}


@app.get("/list/check")
async def check_list(list_code: str = "invalid"):
    # Query specific list code
    cursor.execute(f"SELECT list_code FROM listcodes WHERE list_code='{list_code}'")
    result = cursor.fetchone()
    # Respond
    if result is not None:
        # The list exists
        return {"success": True}
    else:
        # The list doesn't exist
        return {"success": False}
