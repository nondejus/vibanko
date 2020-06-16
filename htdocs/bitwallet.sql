CREATE SEQUENCE users_user_id_sequence;

CREATE TABLE users (
    user_id bigint DEFAULT NEXTVAL('users_user_id_sequence') PRIMARY KEY NOT NULL,
    user_handle varchar(50) NOT NULL UNIQUE,
    password_hash bytea NOT NULL,
    password_salt bytea NOT NULL,
    password_iterations smallint NOT NULL,
    email varchar(500) NOT NULL,
    balance NUMERIC(26,8) NOT NULL
);

CREATE TABLE bitcoin_addresses (
    user_id bigint REFERENCES users(user_id),
    bitcoin_address varchar(35) NOT NULL UNIQUE
);

CREATE SEQUENCE withdrawal_requests_withdrawal_request_id_sequence;

CREATE TABLE withdrawal_requests (
    withdrawal_request_id bigint DEFAULT NEXTVAL('withdrawal_requests_withdrawal_request_id_sequence'),
    withdrawal_amount NUMERIC(26,8) NOT NULL,
    bitcoin_address varchar(35) NOT NULL,
    user_id bigint REFERENCES users(user_id),
    status varchar(8) DEFAULT 'PENDING' NOT NULL
);

CREATE SEQUENCE deposits_deposit_id_sequence;

CREATE TABLE deposits (
    deposit_id bigint DEFAULT NEXTVAL('deposits_deposit_id_sequence'),
    amount NUMERIC(26,8) NOT NULL,
    bitcoin_address varchar(35) NOT NULL REFERENCES bitcoin_addresses(bitcoin_address),
    transaction_id char(64) NOT NULL,
    user_id bigint REFERENCES users(user_id),
    UNIQUE (transaction_id,bitcoin_address)
);

CREATE TABLE login_attempts (
    attempt_ip inet,
    attempt_timestamp timestamp DEFAULT CURRENT_TIMESTAMP,
    attempt_username varchar(50)
);
