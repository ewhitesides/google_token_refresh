#example template
#https://gallery.ecr.aws/lambda/python

FROM public.ecr.aws/lambda/python:3.9

#copy requirements.txt first to leverage Docker cache
COPY requirements.txt ${LAMBDA_TASK_ROOT}

#pip install dependencies
RUN pip3 install -r requirements.txt

#copy all files to the container
COPY . ${LAMBDA_TASK_ROOT}

#run the app
CMD [ "app.handler" ]
