create user "elpino"@"%" identified by "Secret.123";
grant all privileges on *.* to "elpino"@"%" identified by "Secret.123";
create database elpino character set utf8 collate utf8_bin;
grant all on elpino.* to "elpino"@"%" identified by "Secret.123";
