INSERT INTO app_user(username, user_password)
VALUES
	('mjover', 'password123'),
	('bsamuel4', 'anotherpassword123'),
	('ccastrog', 'pass123'),
	('hbalu', 'password942'),
	('vyarabad', 'password456')
;

INSERT INTO scratch(caption, author_id, is_comment)
VALUES
	('myfirstscratch :)', 1	, false),
	('Cesar made this scratch :)', 3, false),
	('Harshica replied to Cesar', 4, true)
;

INSERT INTO user_history(user_id, parent_scratch_id, user_created_parent_scratch, user_commented, user_comment_scratch_id, user_liked)
VALUES
	(1, 1, true, false, NULL, false), -- mjover created a scratch of id = 1
	(3, 2, true, false, NULL, false), -- ccastrog created a scratch of id = 2
	(4, 2, false, true, 3, false),  -- hbalu replied to scratch of id = 2 and their comment scratch has id = 3
	(1, 3, false, false, NULL, true) -- mjover liked hbalu's reply with an id = 3
;
