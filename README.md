# Race Pace

Alexa Skills - Health & Fitness

A Pace Calculator for Amazon Alexa. Enable this skill on the Race Pace homepage
on [Amazon][racepace].

## Deployment

This package is written for Amazon Lambda and must be built in a
[Amazon Linux AMI][amazonlinux]. A Dockerfile is include to create the necessary
machine image.

    docker build -t lambda racepace/image

    docker run -it -d --name racepace lambda

    docker cp racepace racepace:/.
    docker exec -ti racepace sh /racepace/build.sh
    docker cp racepace:/racepace/dist/lambda.zip .

    docker stop racepace

1. Configure interaction model on Alexa page in the Amazon Developer Console
2. Upload `lambda.zip` to Lambda
3. Set an environment variable in Lambda for `APPLICATION_ID` to the skills
   ID to enforce verification.

[racepace]: https://www.amazon.com/dp/B072HC713N
[amazonlinux]: http://docs.aws.amazon.com/lambda/latest/dg/current-supported-versions.html
