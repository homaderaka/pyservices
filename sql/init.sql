-- Create the usersdb database if it does not exist
create database if not exists usersDB;

-- Switch to the usersdb database
use usersDB;

-- Create a user with the given username and password
-- Replace 'your_username' and 'your_password' with actual credentials
create user if not exists 'user'@'%' identified by 'password';

-- Grant necessary privileges to the user (adjust privileges as needed)
grant all privileges on usersDB.* to 'user'@'%';

-- Create the 'users' table
create table if not exists users (
    id int not null auto_increment,
    name varchar(20) not null unique,
    passwordHash varchar(128) not null,
    primary key (id)
);

-- Optionally, you can insert initial data into the 'users' table here
