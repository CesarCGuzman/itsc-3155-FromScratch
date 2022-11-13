-- FromScratch SQL Schema here :)
CREATE TABLE IF NOT EXISTS user_scratch_history (
    user_id INT NOT NULL,
    scratch_id INT NOT NULL,
    PRIMARY KEY (user_id, scratch_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (scratch_id) REFERENCES scratch(scratch_id) ON UPDATE CASCADE ON DELETE CASCADE
);