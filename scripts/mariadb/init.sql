# for grafana
create database grafana;
create user 'grafana' identified by 'changeafterinstall';
grant all privileges ON `grafana`.* to 'grafana'@'%' with grant option;

# for poc
create database poc;
create user 'poc' identified by 'poc';
grant all privileges ON `poc`.* to 'poc'@'%' with grant option;