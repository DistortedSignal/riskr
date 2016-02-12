import hashlib
import random
import bcrypt
import time

def create_and_store_tmp_token(user_id, db_conn):
    # Get system time and a nonce
    now = time.time() # Seconds.milliseconds since epoch
    nonce = random.random()
    token = hashlib.sha256(str(now) + '|' + str(nonce) + '|' +
        str(user_id)).hexdigest()

    # Store the temporary token and the time the token will expire
    cursor = db_conn.cursor()
    # TODO Figure out how to dates with python, psycopg2, and Postgres
    cursor.execute("UPDATE user SET token=%(token)s, " + 
        "token_expire_date=%(token_expire_date)s " +
        "WHERE id=%(user_id)s",
        {'token': token, 
        'token_expire_date': now, # TODO now + 5 minutes
        'user_id': user_id}
        )
    db_conn.commit()
    cursor.close()

    # Return the temporary token
    return token

def create_new_user(user_name, email_address, password, db_conn):
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password, salt)
    # TODO Figure out how to id (either auto-generate or other)
    # TODO Should we pass in connections or cursors? Investigate.
    cursor = db_conn.cursor()
    # Caution, weird formatting ahead! I formatted the code like this to make
    # it easier to read and understand what all the args do. I would prefer to
    # leave this code as it is rather than changing it to named arguments.
    # TODO Wrap this in a try/except to ensure that email address is unique.
    cursor.execute("INSERT INTO user " +
        "(display_name, email_address, password_hash, salt) VALUES" +
        "(%s,           %s,            %s,            %s)",
        ( user_name,    email_address, pw_hash,       salt))
    db_conn.commit()
    cursor.close()

    return attempt_login(email_address, password, db_conn)

def attempt_login(email_address, password, db_conn):
    cursor = db_conn.cursor()
    cursor.execute("SELECT id, password_hash, salt FROM user WHERE " +
        "email_address=%(email)s",
        {'email': email_address})
    row_tuples = cursor.fetchall()
    cursor.close()
    # TODO Lots of stuff here

    if row_tuples == []:
        # There were no users in the db with that email address
        return False

    if bcrypt.hashpw(password, salt) == pw_hash:
        return [user_id, create_and_store_tmp_token(user_id, db_conn)]
    return False

def verify_logged_in_user(user_id, token, db_conn):
    # TODO Get user id and token from database based on email address
    cursor = db_conn.cursor()
    cursor.execute("SELECT token, token_expire_date FROM user " +
        "WHERE id=%(user_id)s",
        {'user_id': user_id})
    results = db_conn.fetchall()
    cursor.close()

    if token == stored_token: # TODO and $now < token_expire_date
        # TODO Generate a new temporary token and embed it in the return value
        return [user_id, create_and_store_tmp_token(user_id, db_conn)]
