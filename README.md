# Joke Detection ML Deployment

This project is a implimention of the following stack.
- Tensorflow: Nural Network Creation
- Tensorflow: Extended: Pipelines
- AWS S3: Model Deployment/Storage
- AWS Lamdba/API Gateway: Hosting endpoint that utlizes model to generate responses

## Setup

If the below functions are to work you need to provide your amazong api access to the srcipts via modifying the `.env.example` files in both `src` and `src/model_server`. These files must be copyed to .env in the same directory and the values need to be replaced with your own AWS keys.


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
# Run Deploy script that will generate the docker image and push to ECR where it can be used to launch a lamdba function
cd src/model_server
./deploy
```


This model is currently deployed at the following URL with the joke being passed as a `query prameter` in a `GET` request. The prameter key is `joke`.
[https://ya7kfyqg06.execute-api.us-west-1.amazonaws.com/joke_predict?joke=%22What%20do%20kids%20play%20when%20their%20mom%20is%20using%20the%20phone?%20Bored%20games.%22](https://ya7kfyqg06.execute-api.us-west-1.amazonaws.com/joke_predict?joke=%22What%20do%20kids%20play%20when%20their%20mom%20is%20using%20the%20phone?%20Bored%20games.%22)