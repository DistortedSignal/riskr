CREATE TABLE user
(
    id                      INTEGER NOT NULL,
    username                VARCHAR(256) NOT NULL,
    salt                    VARCHAR(31) NOT NULL,
    password_hash           VARCHAR(62) NOT NULL,
    display_name            VARCHAR(128) NOT NULL,
    CONSTRAINT user_id      PRIMARY KEY (id),
    CONSTRAINT un_unique    UNIQUE (username)
);

# Currently this should be mated with PostgreSQL, so we're using TEXT. Make sure
# that if we migrate databases that we change the column type to that DB's
# chosen > 1 GB type.
# Also, because we're using PostgreSQL, TIMESTAMP WITH TIME ZONE is our date
# column.
CREATE TABLE post
(
    id                      INTEGER NOT NULL,
    user_id                 INTEGER NOT NULL,
    title                   VARCHAR(140) NOT NULL,
    body                    TEXT,
    posted_date             TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT post_id      PRIMARY KEY (id),
    CONSTRAINT user_fk      FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE INDEX user_index ON post (user_id);

# LEARN
CREATE TABLE comment
(
    id                      INTEGER NOT NULL, # Necessary?
    post_id                 INTEGER NOT NULL,
    user_id                 INTEGER NOT NULL,
    comment_body            TEXT NOT NULL,
    posted_date             TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT post_fk      FOREIGN KEY (post_id) REFERENCES post (id),
    CONSTRAINT user_fk      FOREIGN KEY (user_id) REFERENCES user (id)
);

CREATE INDEX post_index ON comment (post_id);