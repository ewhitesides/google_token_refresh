# Overview

python code to refresh a google oauth2 token, or create a new one if it does not exist

## Steps to create the initial oauth2 credential

in google, do the following

- in console.cloud.google.com, create a new project
- in APIs & Services, enable a google service
- in APIs & Services > Credentials > Create Credentials
  - choose OAuth client ID > Desktop App > Create
  - download the google oauth json file with the client id and client secret
- in APIs & Services > OAuth consent screen > Test users, add your gmail account as a test user

in aws console, do the following

- navigate to secrets manager
- click store a new secret with name 'ggloauthcred' > other type of secret > plaintext
- paste in the contents of the google oauth json file
- click store a new secret with name 'ggloauthtoken' (leave empty)

clone this repo locally, then in the repo
create .devcontainer/devcontainer.env file with contents:

```bash
AWS_SECRET_PATH_GOOGLE_CRED=path/to/ggloauthcred
AWS_SECRET_PATH_GOOGLE_TOKEN=path/to/ggloauthtoken
AWS_DEFAULT_REGION=your-region-here

#the following vars are used in boto3 in the python script
#when running in production the lambda function should have access to the locations in aws secretsmanager
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

- open the repo in vscode as a devcontainer
- run the debug task 'debug app.handler'
- on first run it should prompt you with a web browser to allow the app to access your google account
- future runs of the debug task should just refresh the token without requiring the web page consent

## Run lambda container locally

```bash
#change to app folder where lambda Dockerfile is
cd app

#build docker image
docker image build --tag google_token_refresh:0.0.1 .

#run docker image with env file from .devcontainer
docker container run --publish 9000:8080 --env-file ../.devcontainer/devcontainer.env google_token_refresh:0.0.1

#test by executing a test payload
curl 'http://localhost:9000/2015-03-31/functions/function/invocations' \
-d '{}'
```

## Steps to manually deploy lambda container to aws ecr

```bash
#get the aws registry url
REPO_URI='227821232291.dkr.ecr.us-east-2.amazonaws.com/abcs_token'

#login to aws ecr
aws ecr get-login-password | docker login --username AWS --password-stdin $REPO_URI

#cd to code folder with lambda Dockerfile
cd app

#build docker image
docker image build --tag google_token_refresh:0.0.1 .

#tag docker image
docker image tag google_token_refresh:0.0.1 $REPO_URI:0.0.1
docker image tag google_token_refresh:0.0.1 $REPO_URI:latest

#push the docker image to aws ecr
docker image push $REPO_URI:0.0.1
docker image push $REPO_URI:latest
```

