from __future__ import print_function

def render_user(user_id, template_dict, conn_db):
    # Get User from database based on user id
    try:
        cursor = conn_db.cursor()
        cursor.execute("SELECT display_name FROM user WHERE id=%(user_id)s",
            {'user_id': user_id})
        results = conn_db.fetchall()
        # TODO Replace this logic once the database is integrated
        user = {'name': 'display_name'}
    except AttributeError:
        # To make it so the db being mocked out still works.
        user = {'name': 'Tom'}
    # Render user
    return template_dict['user'].render(user=user)

def render_comment(comment_id, template_dict, conn_db):
    # Get Comment from database based on comment id
    try:
        cursor = conn_db.cursor()
        cursor.execute("SELECT user_id, comment_body, posted_date FROM " +
            "comment WHERE comment_id=%(comment_id)s", 
            {'comment_id': comment_id})
        results = conn_db.fetchall()
        # TODO Construct comment from results
        cursor.close()
    except AttributeError:
        comment = {'user_id': 1, 'comment_body': 'This is comment', 
        'posted_date': '$date_here'}
    comment['compiled_user'] = render_user(comment['user_id'], template_dict, 
        db_conn)
    return template_dict['comment'].render(comment=comment)

def render_post(post_id, template_dict, conn_db):
    # Get post from database based on post id
    # TODO Remove try blocks so I can use the same cursor twice.
    try:
        cursor = conn_db.cursor()
        cursor.execute("SELECT user_id, title, body, posted_date FROM post" +
            "WHERE id=%(post_id)s",
            {'post_id': post_id})
        results = conn_db.fetchall()
        # TODO Construct post from results
        cursor.close()
    except AttributeError:
        post = {'user_id': 1, 'title': 'This is post title', 'body': 
        'This is a super long post body, and it can go on for a long way.',
        'posted_date': '$date_here'}

    # Get comment list from database based on post id
    try:
        cursor = conn_db.cursor()
        cursor.execute("SELECT id FROM comment WHERE post_id=%(post_id)s",
            {'post_id': post_id})
        results = conn_db.fetchall()
        cursor.close()
    except AttributeError:
        results_transformed = [1,2,3]

    post['compiled_comments'] = map(
        lambda x: render_comment(x, template_dict, db_conn),
        results_transformed)

    # Get user based on user_id
    post['compiled_user'] = render_user(post['user_id'], template_dict, db_conn)
    return template_dict['post'].render(post=post)

def render_front_page(user_id, template_dict, conn_db):
    # Get User from database based on id
    try:
        cursor = conn_db.cursor()
        cursor.execute("SELECT display_name FROM user WHERE id=%(user_id)s",
            {'user_id': user_id})
        results = conn_db.fetchall()
        cursor.close()
    except AttributeError:
        user = {'name': 'Tom'}

    # Get a list of posts from the database
    try:
        cursor = conn_db.cursor()
        cursor.execute("SELECT id FROM post") # Limit this in some way, shape,
        #                                       or form
        results = db_conn.fetchall()
        # TODO
        cursor.close()
    except AttributeError:
        results_transformed = [1,2,3,4,5]

    posts = map(
        lambda x: render_post(x, template_dict, db_conn),
        results_transformed)
    
    return template_dict['main'].render(compiled_posts=posts, user=user)
