import dbconnect

def store_user(name, id, token, refresh_token, expires_at):
    userdb = dbconnect.connect_to_userdb()
    cursor = userdb.cursor()
    user = (id, name, token, refresh_token, expires_at)
    cursor.execute(
        "REPLACE INTO USERS (id, name, token, refresh_token, expires_at)"
        " VALUES (?, ?, ?, ?, ?)",
        user
    )
    userdb.close()

def fetch_user(user_id):
    userdb = dbconnect.connect_to_userdb()
    cursor = userdb.cursor()
    user = cursor.execute(
        "SELECT * FROM USERS "
        "WHERE id = ?",
        user_id
    )
    userdb.close()
    return user

def update_user(user_id, newuser):
    userdb = dbconnect.connect_to_userdb()
    cursor = userdb.cursor()

    userdb.close()