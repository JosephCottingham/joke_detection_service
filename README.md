# Joke Detection ML Deployment

This project is a implimention of the following stack.
- Tensorflow: Nural Network Creation
- Tensorflow: Extended: Pipelines
- AWS S3: Model Deployment/Storage
- AWS Lamdba/API Gateway: Hosting endpoint that utlizes model to generate responses





## Deploy New Model Generated via Pipeline

```
cd src

python3 -m venv venv

source venv/bin/activate

pip3 install -r requirements.txt

./run_pipeline.sh
```

## Deploy Endpoint Lamdba.

***Note that we are deploying the lamdba within a custom container because of the size of the Tensorflow (and dependences) libaray exceedes aws max size for uplading via the lamdba CLI. (Custom contaienrs have a max size of 10 GB which allows all the space we need.)***

Apply the desired AWS profile
```
export AWS_PROFILE=<AWS-ENV>
```

```
# Login to the AWS container register
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 745490699111.dkr.ecr.us-west-1.amazonaws.com
# Build the lamdba docker image
docker build . -t 745490699111.dkr.ecr.us-west-1.amazonaws.com/joke_detection_predict:latest 
# Push the docker image to ECR
docker push 745490699111.dkr.ecr.us-west-1.amazonaws.com/joke_detection_predict:latest
``` 