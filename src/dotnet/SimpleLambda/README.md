# Simple .NET Lambda

A simple .NET Lambda function that can be deployed to LocalStack for testing.

## Prerequisites

* Docker installed and running
* LocalStack running (via `docker-compose up -d`)
* AWS CLI configured for LocalStack

## Quick Start

### 1. Start LocalStack

```bash
docker-compose up -d
```

### 2. Deploy the Lambda

**ZIP Package (recommended for LocalStack)**

```bash
python ../../../scripts/deploy-lambda-localstack-zip.py
```

### 3. Test the Lambda

**Using Python script (recommended - works everywhere):**

```bash
# Use defaults (simple-lambda with {"test":"data"})
python ../../../scripts/invoke-lambda-localstack.py

# Specify custom payload
python ../../../scripts/invoke-lambda-localstack.py simple-lambda '{"key":"value"}'

# Save response to file
python ../../../scripts/invoke-lambda-localstack.py simple-lambda '{"test":"data"}' --output response.json
```

## Building Locally

```bash
dotnet build
dotnet publish -c Release
```

## Dockerfile Details

The Dockerfile uses a multi-stage build:

1. **Build stage**: Uses .NET SDK to build and publish the Lambda
2. **Runtime stage**: Uses .NET runtime with Lambda Runtime Interface Emulator (RIE) for LocalStack compatibility

The Lambda Runtime Interface Emulator allows LocalStack to invoke the Lambda function locally.
