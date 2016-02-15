from __future__ import print_function

# At some point, investigate ORMs so we're not creating and destroying cursors
# at a furious rate.

def render_user(user_id, template_dict, db_conn):
    # Get User from database based on user id
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT display_name FROM user WHERE id=%(user_id)s",
            {'user_id': user_id})
        results = db_conn.fetchall()
        # TODO Replace this logic once the database is integrated
        user = {'name': 'display_name'}
        cursor.close()
    except AttributeError:
        # To make it so the db being mocked out still works.
        user = {'name': 'Tom'}
    # Render user
    return template_dict['user'].render(user=user)

def render_comment(comment_id, template_dict, db_conn):
    # Get Comment from database based on comment id
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT user_id, comment_body, posted_date FROM " +
            "comment WHERE comment_id=%(comment_id)s", 
            {'comment_id': comment_id})
        results = db_conn.fetchall()
        # TODO Construct comment from results
        cursor.close()
    except AttributeError:
        comment = {'user_id': 1, 'comment_body': 'This is comment', 
        'posted_date': '$date_here'}
    comment['compiled_user'] = render_user(comment['user_id'], template_dict, 
        db_conn)
    return template_dict['comment'].render(comment=comment)

def render_post(post_id, template_dict, db_conn):
    # Get post from database based on post id
    # TODO Remove try blocks so I can use the same cursor twice.
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT user_id, title, body, posted_date FROM post" +
            "WHERE id=%(post_id)s",
            {'post_id': post_id})
        results = db_conn.fetchall()
        # TODO Construct post from results
        cursor.close()
    except AttributeError:
        post = {'user_id': 1, 'title': 'This is post title', 'body': 
        'This is a super long post body, and it can go on for a long way.',
        'posted_date': '$date_here'}

    # Get comment list from database based on post id
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT id FROM comment WHERE post_id=%(post_id)s",
            {'post_id': post_id})
        results = db_conn.fetchall()
        cursor.close()
    except AttributeError:
        results_transformed = [1,2,3]

    post['compiled_comments'] = map(
        lambda x: render_comment(x, template_dict, db_conn),
        results_transformed)

    # Get user based on user_id
    post['compiled_user'] = render_user(post['user_id'], template_dict, db_conn)
    return template_dict['post'].render(post=post)

def render_front_page_body(user_name, template_dict, db_conn):
    try:
        cursor = db_conn.cursor()
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
    
    return template_dict['main'].render(compiled_posts=posts, user=user_name)

def render_front_page_with_user(user_id, template_dict, db_conn):
    # Get User from database based on id
    try:
        cursor = db_conn.cursor()
        cursor.execute("SELECT display_name FROM user WHERE id=%(user_id)s",
            {'user_id': user_id})
        results = db_conn.fetchall()
        cursor.close()
    except AttributeError:
        user = {'name': 'Tom'}

    return render_front_page_body(user['name'], template_dict, db_conn)

def render_front_page_without_user(template_dict, db_conn):
    return render_front_page_body('Anonymous', template_dict, db_conn)

def render_login(template_dict):
    return template_dict['login'].render()

def render_nav_bar(current_page, template_dict):
    # TODO Make this better
    if current_page == 'home':
        return template_dict['nav_bar'].render(home='class="active"', 
            login='', contact='')
    elif current_page == 'login':
        return template_dict['nav_bar'].render(home='',
            login='class="active"', contact='')
    elif current_page == 'contact':
        return template_dict['nav_bar'].render(home='', login='',
            contact='class="active"')
    else:
        raise LookupError('Page lookup was outside expected values ' +
            '[home, main, contact]')
