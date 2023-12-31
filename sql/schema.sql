PRAGMA foreign_keys = ON;

CREATE TABLE users(
    username    VARCHAR(20)     NOT NULL,
    fullname    VARCHAR(40)     NOT NULL,
    email       VARCHAR(40)     NOT NULL,
    filename    VARCHAR(64)     NOT NULL,
    password    VARCHAR(256)    NOT NULL,
    created     DATETIME        DEFAULT     CURRENT_TIMESTAMP,
    
    PRIMARY KEY(username)
);

CREATE TABLE posts(
    postid      INTEGER         NOT NULL,
    filename    VARCHAR(64)     NOT NULL,
    owner       VARCHAR(20)     NOT NULL,
    created     DATETIME        DEFAULT     CURRENT_TIMESTAMP,
    
    PRIMARY KEY(postid),
    FOREIGN KEY(owner) references users(username)
      ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE following(
    username1   VARCHAR(20)     NOT NULL,
    username2   VARCHAR(20)     NOT NULL,
    created     DATETIME        DEFAULT     CURRENT_TIMESTAMP,
    
    PRIMARY KEY(username1, username2),
    FOREIGN KEY(username1) references users(username)
      ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(username2) references users(username)
      ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE comments(
    commentid   INTEGER         NOT NULL,
    owner       VARCHAR(20)     NOT NULL,
    postid      INTEGER         NOT NULL,
    text        VARCHAR(1024)   NOT NULL,
    created     DATETIME        DEFAULT     CURRENT_TIMESTAMP,

    PRIMARY KEY(commentid),
    FOREIGN KEY(owner) references users(username)
      ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(postid) references posts(postid)
      ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE likes(
    owner       VARCHAR(20)     NOT NULL,
    postid      INTEGER         NOT NULL,
    created     DATETIME        DEFAULT     CURRENT_TIMESTAMP,

    PRIMARY KEY(owner, postid),
    FOREIGN KEY(postid) references posts(postid)
      ON DELETE CASCADE ON UPDATE CASCADE
);
