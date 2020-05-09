
# Trigger the scraping job

Assuming we have gone through all steps of the AWS Deployment Walkthrough (see below). If we want to start the scraping job ourselves, instead of through the scheduled event, we just:

```bash
aws ecs run-task --cli-input-json file://deployment/ecs/run-task/kinoprogramm-scraper.json
```

When the task is completed, json files should have been written to S3. See [athena queries](athena/README.md) for accessing the scraped data.

Alternatively, for debugging purposes, the scraping job can be triggered to be run locally, and, by providing the AWS credentials, the scraped jsons will be written to S3.

Assuming you have built the `kinoprogramm-scraper:latest` image:

```bash
docker run -e AWS_ACCESS_KEY_ID=<your AWS access key ID> -e AWS_SECRET_ACCESS_KEY=<your AWS secret access key> kinoprogramm-scraper:latest
```

# New deployment

To start over with the complete deployment in AWS, see next section (AWS Deployment Walkthrough).

If we have only introduced a modification in the code (e.g. needed to adapt the scraping to changes in the website), then we just need to push our new docker image:

&#8594; Retrieve the login command to use to authenticate your Docker client to your registry:

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 287094319766.dkr.ecr.eu-central-1.amazonaws.com
```

&#8594; After successful authentication, build, tag, and push the docker image:

```bash
docker build -t kinoprogramm-scraper scrapy
docker tag kinoprogramm-scraper:latest 287094319766.dkr.ecr.eu-central-1.amazonaws.com/kinoprogramm-scraper:dev
docker push 287094319766.dkr.ecr.eu-central-1.amazonaws.com/kinoprogramm-scraper:dev
```

No need to update the event rule or event target. The next event will trigger the job in the newly pushed image. 

&#8594; Verify everything runs as expected by starting the task manually:

```bash
aws ecs run-task --cli-input-json file://deployment/ecs/run-task/kinoprogramm-scraper.json
```

When the task is completed, json files should have been written to S3. See [athena queries](athena/README.md) for accessing the scraped data.


# AWS Deployment Walkthrough

These are all steps for the deployment in my personal AWS account, with ID `287094319766`, where my username is `Laura`.

Basically, we deploy a Docker container with our scraper to Amazon Elastic Container Service (ECS) and create a task to run the scrapping job. We can start this task anytime from the command line, or establish a rule to trigger the task.

Assuming that:
* The [AWS CLI version 2](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) has already been installed and configured with the corresponding `Access key ID`, `Secret access key`, and `region` for the AWS account to deploy to.
* User has at least the following policies: `AmazonS3FullAccess`, `AmazonECS_FullAccess`, `CloudWatchEventsFullAccess`


## S3

&#8594; Create bucket `kinoprogramm-scraper` and path `berlin-de` where we will store the scraped data

```bash
aws s3 mb s3://kinoprogramm-scraper --region eu-central-1 --endpoint-url https://s3.eu-central-1.amazonaws.com
```

```bash
aws s3api put-object --bucket kinoprogramm-scraper --key berlin-de
```


## ECR

&#8594; Create policy `ecrDeveloper` to allow users access to ecr:

```bash
aws iam create-policy --policy-name ecrDeveloper --policy-document file://deployment/policies/ecr_developer.json
```
`"Arn": "arn:aws:iam::287094319766:policy/ecrDeveloper"`

&#8594; Attach created policy to user (in this case, my username is `Laura`):

```bash
aws iam attach-user-policy --user-name Laura --policy-arn arn:aws:iam::287094319766:policy/ecrDeveloper
```

&#8594; Create docker registry repository:

```bash
aws ecr create-repository --repository-name kinoprogramm-scraper
```
`"repositoryArn": "arn:aws:ecr:eu-central-1:287094319766:repository/kinoprogramm-scraper"`
`"repositoryUri": "287094319766.dkr.ecr.eu-central-1.amazonaws.com/kinoprogramm-scraper"`

To push our scraper image to this repository:

&#8594; Retrieve the login command to use to authenticate your Docker client to your registry:

```bash
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 287094319766.dkr.ecr.eu-central-1.amazonaws.com
```

&#8594; After successful authentication, build, tag, and push the docker image:

```bash
docker build -t kinoprogramm-scraper scrapy
docker tag kinoprogramm-scraper:latest 287094319766.dkr.ecr.eu-central-1.amazonaws.com/kinoprogramm-scraper:dev
docker push 287094319766.dkr.ecr.eu-central-1.amazonaws.com/kinoprogramm-scraper:dev
```


## ECS 

### Cluster

&#8594; Create a cluster to run scraper task:

```bash
aws ecs create-cluster --cluster-name scraperCluster
```
`"clusterArn": "arn:aws:ecs:eu-central-1:287094319766:cluster/scraperCluster"`

### Policies for task

&#8594; Create policy `writeScraped` for write access to our bucket in S3:

```bash
aws iam create-policy --policy-name writeScraped --policy-document file://deployment/policies/write_scraped.json 
```
`"Arn": "arn:aws:iam::287094319766:policy/writeScraped"`

&#8594; Create role `KinoprogrammScraperRole` to execute scraper and attach policies writeScraped and AmazonECSTaskExecutionRolePolicy to this role:

```bash
aws iam create-role --role-name KinoprogrammScraperRole --assume-role-policy-document file://deployment/policies/kinoprogramm_scraper_role.json
```
`"Arn": "arn:aws:iam::287094319766:role/KinoprogrammScraperRole"`

```bash
aws iam attach-role-policy --role-name KinoprogrammScraperRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
aws iam attach-role-policy --role-name KinoprogrammScraperRole --policy-arn arn:aws:iam::287094319766:policy/writeScraped
```

&#8594; Create generic role `ecsTaskExecutionRole` for executing ECS tasks and attach policy AmazonECSTaskExecutionRolePolicy to this role:

```bash
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://deployment/policies/ecs_task_execution_role.json
```
`"Arn": "arn:aws:iam::287094319766:role/ecsTaskExecutionRole"`

```bash
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

&#8594; Create generic role `ecsEventsRole` for starting tasks from events, and attach policy AmazonEC2ContainerServiceEventsRole to this role:

```bash
aws iam create-role --role-name ecsEventsRole --assume-role-policy-document file://deployment/policies/ecs_events_role.json
```
`"Arn": "arn:aws:iam::287094319766:role/ecsEventsRole"`

```bash
aws iam attach-role-policy --role-name ecsEventsRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceEventsRole
```

### Task Definition

&#8594; Create the log group for the scraper:

```bash
aws logs create-log-group --log-group-name scraperLogs
```

&#8594; Register task definition for scraper:

```bash
aws ecs register-task-definition --cli-input-json file://deployment/ecs/register-task-definition/kinoprogramm-scraper.json
```
`"taskDefinitionArn": "arn:aws:ecs:eu-central-1:287094319766:task-definition/KinoprogrammScraper:1"`

### Events

&#8594; Put rule for scraper (e.g. scraping once a day):

```bash
aws events put-rule --cli-input-json file://deployment/events/put-rule/kinoprogramm-scraper.json
```
`"RuleArn": "arn:aws:events:eu-central-1:287094319766:rule/kinoprogrammScraperRule"`

&#8594; Assign target to be triggered by the event. Using the default Security Group and the default Subnet corresponding to Availability Zone eu-central-1a. 

```bash
aws events put-targets --cli-input-json file://deployment/events/put-targets/kinoprogramm-scraper.json
```

&#8594; Activate rule:

```bash
aws events enable-rule --name kinoprogrammScraperRule
```


# Start task "manually"

We do not need to wait for the task trigger, but we can also initiate it ourselves. Assuming all steps above have been completed.

&#8594; Run task. Using the default Security Group and the default Subnet corresponding to Availability Zone eu-central-1a.

```bash
aws ecs run-task --cli-input-json file://deployment/ecs/run-task/kinoprogramm-scraper.json
```

&#8594; See task ARN:

```bash
aws ecs list-tasks --cluster scraperCluster
```

When the task is completed, json files should have been written to S3. See [athena queries](athena/README.md) for accessing the scraped data.


# Lambda function to send email when json lands in S3

&#8594; Install [npm](https://nodejs.org/en/).

&#8594; Install the [serverless](https://serverless.com/cli/) package:

```bash
npm install -g serverless
```

&#8594; Create a serverless project:

```bash
cd deployment
serverless
```

* `AWS Python`
* name: `jsonEmail`

The `serverless.yml`, `handler.py`, and `.gitignore` files are created under the new folders (one for each of the created projects).

&#8594; Edit the files: `/jsonEmail/serverless.yaml`, `/jsonEmail/handler.py`.

Documentation: [send email with boto3](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-using-sdk-python.html), [add attachment](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/send-email-raw.html)

&#8594; Create policy that allows to work with SES, e.g. verify email addresses:

```bash
aws iam create-policy --policy-name emailSender --policy-document file://deployment/policies/email_sender.json
```
`"Arn": "arn:aws:iam::287094319766:policy/emailSender"`

&#8594; Attach created policy to user:

```bash
aws iam attach-user-policy --user-name Laura --policy-arn arn:aws:iam::287094319766:policy/emailSender
```

&#8594; [Verify](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/verify-email-addresses.html) the sender and recipient(s) email address:

```bash
aws ses verify-email-identity --email-address email_1@address.com
aws ses verify-email-identity --email-address email_2@address.com
```

A verification message is sent to the inbox of the email address to be verified. Need to click on the provided link to proceed.
Check that email address has been verified:

```bash
aws ses list-identities
aws ses get-identity-verification-attributes --identities "email_1@address.com"
```

&#8594; Deploy. Will bundle up and deploy the Lambda function.

```bash
cd  jsonEmail
sls deploy
```

To remove deployment:

```bash
sls remove
```
