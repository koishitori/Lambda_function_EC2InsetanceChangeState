# EC2 Control Lambda Function

This AWS Lambda function allows you to start or stop EC2 instances based on tags. It can be utilized in various scenarios, such as scheduling nightly shutdowns with EventBridge or implementing irregular stop schedules using AWS Change Calendar, making it a versatile tool for EC2 instance management.

## Function Overview

The function takes a JSON payload with the following structure:

```json
{
  "region": string,  # target region
  "tagName": string, # tag-name of target EC2 instance 
  "action": string,  # start or stop
  "test": bool
}
```

### Functionality

1. The function retrieves EC2 instance IDs that have the specified `tagName` with a value of either the specified `action` or "true".
2. If the `action` is "start", it will display the instance IDs and start the instances (unless `test` is true).
3. If the `action` is "stop", it will display the instance IDs and stop the instances (unless `test` is true).

## Setup

1. Create a new Lambda function in your AWS account.
2. Use Python 3.12 as the runtime.
3. Copy the provided Python code into the Lambda function.
4. Set the appropriate IAM role with the minimum required permissions (see IAM Policy section).

## IAM Policy

Attach the following IAM policy to your Lambda function's execution role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

This policy grants the necessary permissions to describe EC2 instances, start/stop instances, and write logs.

## Usage

Invoke the Lambda function with a JSON payload. For example:

```json
{
  "region": "us-west-2",
  "tagName": "Environment",
  "action": "start",
  "test": false
}
```

This will start all EC2 instances in the us-west-2 region that have the tag "Environment" with a value of either "start" or "true".

## Testing

Set the `test` parameter to `true` in the payload to run the function without actually starting or stopping instances. This allows you to verify which instances would be affected by the function.

## Logging

The function logs instance IDs and actions to CloudWatch Logs. Check the Lambda function's log group in CloudWatch for detailed execution information.
