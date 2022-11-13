-- FromScratch SQL Schema here :)
CREATE TABLE IF NOT EXISTS user_scratch_history (
    user_id INT NOT NULL,
    scratch_id INT NOT NULL,
    PRIMARY KEY (user_id, scratch_id),
    FOREIGN KEY (user_id) REFERENCES app_user(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (scratch_id) REFERENCES scratch(scratch_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS app_user (
    user_id SERIAL NOT NULL,
    username VARCHAR(16) NOT NULL,
    user_password VARCHAR(32) NOT NULL,
    date_created DATE NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS scratch (
	scratch_id SERIAL NOT NULL,
	caption VARCHAR(30) NULL,
	author_id INT NOT NULL,
	is_comment BOOLEAN NOT NULL,
	date_created DATE NOT NULL DEFAULT CURRENT_DATE,
	PRIMARY KEY(scratch_id),
	FOREIGN KEY(author_id) REFERENCES app_user(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_history (
    parent_scratch_id INT NOT NULL,
    user_id INT NOT NULL,
    user_created_op_scratch BOOLEAN NOT NULL,
    user_commented BOOLEAN NOT NULL,
    user_comment_scratch_id INT NOT NULL,
    user_liked BOOLEAN NOT NULL,
    PRIMARY KEY (user_id, parent_scratch_id),
    FOREIGN KEY (user_id) REFERENCES app_user(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (parent_scratch_id) REFERENCES scratch(scratch_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_comment_scratch_id) REFERENCES scratch(scratch_id) ON UPDATE CASCADE ON DELETE SET NULL
);