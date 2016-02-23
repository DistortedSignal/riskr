CREATE SCHEMA IF NOT EXISTS riskr;

CREATE TABLE riskr.user
(
    id                      SERIAL,
    display_name            VARCHAR(128) NOT NULL,
    email_address           VARCHAR(512) NOT NULL,
    password_hash           VARCHAR(64) NOT NULL,
    salt                    VARCHAR(32) NOT NULL,
    token                   VARCHAR(64),
    token_expire_date       TIMESTAMP WITH TIME ZONE,
    CONSTRAINT user_id      PRIMARY KEY (id),
    CONSTRAINT un_unique    UNIQUE (email_address)
);

-- This will be used for login
CREATE INDEX user_email_index ON riskr.user (email_address);

-- Currently this should be mated with PostgreSQL, so we're using TEXT. Make sure
-- that if we migrate databases that we change the column type to that DB's
-- chosen > 1 GB type.
-- Also, because we're using PostgreSQL, TIMESTAMP WITH TIME ZONE is our date
-- column.
CREATE TABLE riskr.post
(
    id                      SERIAL,
    user_id                 INTEGER NOT NULL,
    title                   VARCHAR(140),
    body                    TEXT,
    posted_date             TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT post_id      PRIMARY KEY (id),
    CONSTRAINT user_fk      FOREIGN KEY (user_id) REFERENCES riskr.user (id)
);

-- Used to look up users when we need to pair them with a comment
CREATE INDEX post_user_index ON riskr.post (user_id);

-- LEARN
CREATE TABLE riskr.comment
(
    id                      SERIAL,
    post_id                 INTEGER NOT NULL,
    user_id                 INTEGER NOT NULL,
    comment_body            TEXT NOT NULL,
    posted_date             TIMESTAMP WITH TIME ZONE NOT NULL,
    CONSTRAINT post_fk      FOREIGN KEY (post_id) REFERENCES riskr.post (id),
    CONSTRAINT user_fk      FOREIGN KEY (user_id) REFERENCES riskr.user (id)
);

-- Used when we need to get all comments on a certain post
CREATE INDEX comment_post_index ON riskr.comment (post_id);
-- Used to get all comments that a user has made
CREATE INDEX comment_user_index ON riskr.comment (user_id);

-- Create a user for Python to connect to the database with
-- MAKE SURE TO SET A PASSWORD FOR THE USER BEFORE STARTING THE SERVER
CREATE ROLE riskr_user WITH NOCREATEDB NOCREATEUSER PASSWORD 'password';

GRANT CONNECT ON DATABASE riskr TO riskr_user;

GRANT SELECT, UPDATE, INSERT ON riskr.user, riskr.post, riskr.comment
TO riskr_user;

