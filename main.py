from fastapi import FastAPI
import util
import sqlite3

app = FastAPI()
connection = sqlite3.connect("database.db")
cursor = connection.cursor()


@app.get("/")
async def ping():
    return {"success": True}


# <editor-fold desc="List management">
@app.get("/list/create")
async def create_list(flag: int = 0, count_before_flag: int = 0):
    # Get list code
    list_code = util.get_random_string(8)
    # Add it to database
    cursor.execute("CREATE TABLE IF NOT EXISTS listcodes (list_code TEXT);")
    cursor.execute(f"INSERT INTO listcodes VALUES ('{list_code}', {flag}, {count_before_flag});")
    connection.commit()
    print(f"Created list {list_code}")
    # Respond
    return {"success": True, "list_code": list_code}


@app.get("/list/check")
async def check_list(list_code: str = None):
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


@app.get("/list/delete")
async def delete_list(list_code: str = None):
    # Check if list exists
    cursor.execute(f"SELECT list_code FROM listcodes WHERE list_code='{list_code}'")
    result = cursor.fetchone()
    if result is None:
        return {"success": False}
    # Delete list
    cursor.execute(f"DELETE FROM listcodes WHERE list_code='{list_code}'")
    cursor.execute(f"DELETE FROM scans WHERE list_code='{list_code}'")
    connection.commit()
    # Respond
    return {"success": True}
# </editor-fold>


@app.get("/scan/add")
async def add_scan(list_code: str = None, scan_value: str = None):
    if list_code is None or scan_value is None:
        return {"success": False}
    # Check if list is existing
    cursor.execute(f"SELECT list_code FROM listcodes WHERE list_code='{list_code}'")
    result = cursor.fetchone()
    if result is None:
        return {"success": False}
    # Create scans table (if needed)
    cursor.execute("CREATE TABLE IF NOT EXISTS 'scans' (list_code CHAR(8), value VARCHAR(255), scan_count INTEGER);")
    # Set scan count
    scan_count = 1
    cursor.execute(f"SELECT scan_count FROM scans WHERE value='{scan_value}' AND list_code='{list_code}'")
    result = cursor.fetchone()
    if result is not None:
        # Entry already exists
        scan_count = result[0] + 1
        cursor.execute(f"UPDATE scans SET scan_count = {scan_count} WHERE value='{scan_value}' AND list_code='{list_code}'")
        connection.commit()
        return {"success": True, "scan_value": scan_value, "scan_count": scan_count}
    else:
        # Entry doesn't exist, so we need to create it
        cursor.execute(f"INSERT INTO scans VALUES ('{list_code}', {scan_value}, {scan_count});")
        connection.commit()
        return {"success": True, "scan_value": scan_value, "scan_count": scan_count}

