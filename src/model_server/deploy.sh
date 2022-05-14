#!/bin/sh

if [[ -z "$AWS_PROFILE" ]]; then
    echo "Set AWS_PROFILE before running this script" 1>&2
    exit 1
fi
echo AWS_PROFILE is $AWS_PROFILE

docker build . -t 745490699111.dkr.ecr.us-west-1.amazonaws.com/joke_detection_predict:latest
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 745490699111.dkr.ecr.us-west-1.amazonaws.com
docker push 745490699111.dkr.ecr.us-west-1.amazonaws.com/joke_detection_predict:latest