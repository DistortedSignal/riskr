from __future__ import print_function

def render_user(user_id, template_dict):
    # Get User from database based on user id
    # TODO Like, this.
    user = {'name': 'Tom'}
    # Render user
    return template_dict['user'].render(user=user)

def render_comment(comment_id, template_dict):
    # Get Comment from database based on comment id
    # TODO Also, this.
    comment = {'user_id': 1, 'comment_body': 'This is comment', 
    'posted_date': '$date_here'}
    comment['compiled_user'] = render_user(comment['user_id'], template_dict)
    return template_dict['comment'].render(comment=comment)

def render_post(post_id, template_dict):
    # Get post from database based on post id
    # TODO
    post = {'user_id': 1, 'title': 'This is post title',
    'body': 'This is a super long post body, and it can go on for a long way.',
    'posted_date': '$date_here'}

    # Get comment list from database based on post id
    # TODO
    # TODO Change this to a mapping function
    post['compiled_comments'] = [render_comment(1, template_dict),
    render_comment(2, template_dict), render_comment(3, template_dict)]

    # Get user based on user_id
    post['compiled_user'] = render_user(post['user_id'], template_dict)
    return template_dict['post'].render(post=post)

def render_front_page(user_id, template_dict):
    # Get User from database based on id
    user = {'name': 'Tom'}

    # Get a list of posts from the database
    posts = [render_post(1, template_dict), render_post(2, template_dict),
    render_post(3, template_dict), render_post(4, template_dict),
    render_post(5, template_dict)]
    return template_dict['main'].render(compiled_posts=posts, user=user)
