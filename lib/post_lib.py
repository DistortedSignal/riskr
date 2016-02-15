def post(user_id, title, post_body, db_conn):
    cursor = db_conn.cursor()
    # TODO Teach me how to eye_dee / teach me, teach me how to eye_dee
    cursor.execute("INSERT INTO post " +
        "(user_id,  title,     body,     posted_date) VALUES " +
        "(%(user)s, %(title)s, %(body)s, %(date)s)",
        {'user': user_id,
        'title': title,
        'body': post_body,
        'date': now # TODO Date nonesense
        }
    )
    db_conn.commit()

    # TODO invalidate cache, send results to wherever results go when they die.

def comment(post_id, user_id, comment_body, db_conn):
    cursor = db_conn.cursor()
    # TODO Such id, so unique, very key, wow
    cursor.execute("INSERT INTO comment " +
        "(post_id,  user_id,  comment_body, posted_date) VALUES " +
        "(%(post)s, %(user)s, %(comment)s,  %(date)s)",
        {
            'post': post_id,
            'user': user_id,
            'comment': comment_body,
            'date': now # TODO Date nonesense
        }
    )
    db_conn.commit()

    # TODO My worst fear... cache invalidation