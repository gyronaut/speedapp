import dbconnect

def store_user(name, id, token, refresh_token, expires_at):
    userdb = dbconnect.connect_to_userdb()
    cursor = userdb.cursor()
    user = (id, name, token, refresh_token, expires_at)
    cursor.execute(
        "REPLACE INTO USERS (id, name, token, refresh_token, expires_at)"
        " VALUES (%s, %s, %s, %s, %s)",
        user
    )
    userdb.close()

def fetch_user(user_id):
    userdb = dbconnect.connect_to_userdb()
    cursor = userdb.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM USERS "
        "WHERE id = %s",
        (user_id,)
    )
    user = cursor.fetchone()
    userdb.close()
    return user

def update_user(user_id, newuser):
    userdb = dbconnect.connect_to_userdb()
    cursor = userdb.cursor()

    userdb.close()