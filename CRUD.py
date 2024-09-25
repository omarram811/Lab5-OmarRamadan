import sqlite3

def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn

def insert_user(user):
    inserted_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone,address,country) VALUES (?, ?, ?, ?, ?)", (user['name'],user['email'], user['phone'], user['address'],user['country']) )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except:
        conn().rollback()
    finally:
        conn.close()
    return inserted_user

def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)
    except:
        users = []
    return users


def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?",(user_id,))
        row = cur.fetchone()
        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]
    except:
        user = {}
    return user


def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?,phone=?, address = ?, country = ? WHERE user_id=?",(user["name"], user["email"], user["phone"],user["address"], user["country"],
        user["user_id"],))
        conn.commit()
        #return the user
        updated_user = get_user_by_id(user["user_id"])
    except:
        conn.rollback()
        updated_user = {}
    finally:
        conn.close()
    return updated_user

def patch_user(user):
    updated_user = {}
    try:
        user_id = user.get("user_id")
        if not user_id:
            return {"error": "User ID is required"}, 400
        existing_user = get_user_by_id(user_id)
        if not existing_user:
            return {"error": "User not found"}, 404
        # Only update the fields that were provided in the JSON request body
        updated_name = user.get("name", existing_user["name"])
        updated_email = user.get("email", existing_user["email"])
        updated_phone = user.get("phone", existing_user["phone"])
        updated_address = user.get("address", existing_user["address"])
        updated_country = user.get("country", existing_user["country"])
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id = ?", (updated_name, updated_email, updated_phone, updated_address, updated_country, user_id))
        conn.commit()
        updated_user = get_user_by_id(user_id)
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        updated_user = {"error": "Update failed"}
    finally:
        conn.close()
    return updated_user


def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?",(user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message
