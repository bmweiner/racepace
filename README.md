# Race Pace

Alexa Skills - Health & Fitness

A Pace Calculator for Amazon Alexa. Enable this skill on the Race Pace homepage
on [Amazon][rp].

## Deployment

The package must be built in the Amazon Linux AMI, this can be done with
[docker][docker].

1. Configure interaction model on Alexa page in the Amazon Developer Console
2. run `sh build.sh` in Amazon Linux AMI
3. Upload `dist\lambda.zip` to Lambda
4. Set an environment variable in Lambda for `APPLICATION_ID` to the skills
   ID to enforce verification.

[rp]: https://www.amazon.com/dp/B072HC713N
[docker]: https://hub.docker.com/_/amazonlinux/
