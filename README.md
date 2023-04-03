# Overview

python code to refresh an oauth2 token, or create a new one if it does not exist

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

