# LocalStack Init Scripts

This directory contains initialization scripts that run when LocalStack is ready.

Scripts in this directory will be executed automatically when LocalStack starts up.

## Example Use Cases

- Create S3 buckets
- Create DynamoDB tables
- Set up SQS queues
- Configure IAM roles and policies
- Create EventBridge rules

## Script Format

Scripts should be executable shell scripts (`.sh`) or any executable file.

Example:
```bash
#!/bin/bash
awslocal s3 mb s3://my-bucket
awslocal dynamodb create-table --table-name my-table ...
```
