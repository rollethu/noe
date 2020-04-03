Project Noe is founded to help people and government(s) to prevent the spread of COVID19.

To see the projects full documentation see the [wiki](https://gitlab.com/rollet/project-noe/-/wikis/Home).

Build:
* Prerequisites:
  * Backend
    * Non sensitive variables to be put into `code/backend/terraform/non_sensitive.noe.tfvars`
    * Sensitive variables to be put into [AWS Parameter Store](https://eu-central-1.console.aws.amazon.com/systems-manager/parameters?region=eu-central-1).  
    The values should be encrypted with KMS (noe-secrets-key), and their ARN should be put in as a variable into the tfvars file above. See example below:
```
                env_vars = {
                    DJANGO_DATABASE_HOST = "dev-db.cwcdru6hbnif.eu-west-1.rds.amazonaws.com"
                    DJANGO_DATABASE_PORT = "5432"
                    DJANGO_DATABASE_USER = "admin"
                }

                env_secrets = {
                    DJANGO_SECRET_KEY        = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_secret_key"
                    DJANGO_DATABASE_PASSWORD = "arn:aws:ssm:eu-central-1:074164835766:parameter/noe/backend/django_database_password"
                }
```

* Frontend
  * No separate build process, the deploy process will make the bundle first. Use `code/frontend/Jenkinsfile`
* Backend
  * Use `code/backend/Jenkinsfile` to build the application and push it to the registry
  * Use `code/backend/terraform/Jenkinsfile` to deploy the application to a preexisting cluster  