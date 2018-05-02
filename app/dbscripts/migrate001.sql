update django_content_type set app_label='projects' where app_label='dashboard';
alter table dashboard_project rename to projects_project;

alter table project_trainingmodel rename to project_trainingmodel1;

CREATE TABLE "project_trainingModel" (
    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "user_id" varchar(200) NOT NULL, 
    "project_id" integer NOT NULL, "compute_server" varchar(200) NOT NULL, 
    "run_id" integer NOT NULL, "session_id" varchar(32) NOT NULL, 
    "started" datetime NOT NULL, "updated" datetime NOT NULL, 
    "status" varchar(10) NOT NULL, "compute_session" varchar(32) NOT NULL, 
    "run_name" varchar(200) NOT NULL, "compute_type" varchar(32) NOT NULL);

insert into project_trainingmodel(
    user_id,project_id,compute_server,run_id,session_id,started,updated,status,compute_session,run_name,compute_type
    ) select user_id,project_id,compute_server,run_id,session_id,started,updated,status,compute_session,run_name,compute_type 
    from project_trainingmodel1;

drop table project_trainingmodel1;