# sspo_db

Acesso ao SSPO's Database

## Migration
Steps:
## Create Migration File: 
 
 ```bash
 alembic init --template generic alembic
 ```

## Migrations


# dump:
mysqldump -h localhost -u root -p sspo_ontology > sspo_ontology.sql

## Reference
https://michaelheap.com/alembic-python-migrations-quick-start/
https://www.compose.com/articles/schema-migrations-with-alembic-python-and-postgresql/

https://woile.github.io/commitizen/
https://woile.github.io/commitizen/tutorials/gitlab_ci/

#Changelog
gitchangelog > CHANGELOG.md 

https://about.gitlab.com/blog/2017/11/02/automating-boring-git-operations-gitlab-ci/
https://stackoverflow.com/questions/55223622/gitlab-ci-error-loading-key-dev-fd-63-invalid-format-error-job-failed-exit