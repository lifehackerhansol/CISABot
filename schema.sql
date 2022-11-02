drop table if exists reminders;


create table reminders
(
	id BIGINT PRIMARY KEY,
	user_id BIGINT NOT NULL,
	channel_id BIGINT NOT NULL,
    time_expired BIGINT NOT NULL,
	content TEXT
);
