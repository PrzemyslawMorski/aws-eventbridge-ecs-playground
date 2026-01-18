# AWS EventBridge ECS Playground

A sample project to experiment with AWS services, focusing on **ECS (Elastic Container Service)**, **EventBridge**, and **Infrastructure-as-Code**. This playground is designed to be set up in minutes by pointing to your AWS account.

## 🎯 Project Goals

- **Quick Setup**: Deploy everything to AWS in minutes
- **Infrastructure-as-Code**: All infrastructure defined as code using Terraform
- **Event-Driven Architecture**: Explore EventBridge patterns with ECS tasks
- **Local Development**: Full LocalStack support for testing without AWS costs

## 🏗️ Architecture

This project demonstrates:

- **ECS Fargate**: Containerized applications running on AWS
- **EventBridge**: Event-driven communication between services
- **Infrastructure-as-Code**: Reproducible, version-controlled infrastructure
- **LocalStack**: Local AWS service emulation for development
- **Multi-Language Backend**: Implementations in .NET (initial), with Python, Golang, and Node.js alternatives planned

## 📋 Prerequisites

### For AWS Deployment
- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- Docker installed
- AWS account with appropriate permissions

### For Backend Development
- **.NET 10.0 SDK** (for initial implementation)
- **Python 3.11+** (for Python alternative - coming soon)
- **Go 1.21+** (for Golang alternative - coming soon)
- **Node.js 20+** (for Node.js alternative - coming soon)

### For LocalStack Development
- Docker and Docker Compose
- Python 3.8+ (for cross-platform scripts)
- LocalStack CLI (optional, but recommended)

## 🚀 Quick Start

### Option 1: Deploy to AWS

1. **Clone the repository**
   ```bash
   git clone https://github.com/PrzemyslawMorski/aws-eventbridge-ecs-playground
   cd aws-eventbridge-ecs-playground
   ```

2. **Configure AWS credentials**
   ```bash
   aws configure
   # Or set environment variables:
   # export AWS_ACCESS_KEY_ID=your-key
   # export AWS_SECRET_ACCESS_KEY=your-secret
   # export AWS_DEFAULT_REGION=us-east-1
   ```

3. **Deploy infrastructure**
   ```bash
   cd infrastructure/terraform
   terraform init
   terraform plan
   terraform apply
   ```

4. **Verify deployment**
   ```bash
   # Check ECS cluster
   aws ecs list-clusters

   # Check EventBridge rules
   aws events list-rules
   ```

### Option 2: Run Locally with LocalStack

1. **Start LocalStack (Automated)**
   ```bash
   # Cross-platform Python script
   python scripts/setup-localstack.py
   ```

   **Or manually:**
   ```bash
   # Using Docker Compose
   docker-compose up -d localstack

   # Or using LocalStack CLI
   localstack start
   ```

2. **Configure AWS CLI for LocalStack**
   ```bash
   # Linux/Mac
   export AWS_ENDPOINT_URL=http://localhost:4566
   export AWS_ACCESS_KEY_ID=test
   export AWS_SECRET_ACCESS_KEY=test
   export AWS_DEFAULT_REGION=us-east-1

   # Windows (PowerShell)
   $env:AWS_ENDPOINT_URL="http://localhost:4566"
   $env:AWS_ACCESS_KEY_ID="test"
   $env:AWS_SECRET_ACCESS_KEY="test"
   $env:AWS_DEFAULT_REGION="us-east-1"
   ```

3. **Deploy to LocalStack**
   ```bash
   # Same commands as AWS, but pointing to LocalStack
   cd infrastructure/terraform
   terraform init
   terraform plan
   terraform apply
   ```

4. **Verify LocalStack deployment**
   ```bash
   aws --endpoint-url=http://localhost:4566 ecs list-clusters
   aws --endpoint-url=http://localhost:4566 events list-rules
   ```

## 📁 Project Structure

```
aws-eventbridge-ecs-playground/
├── README.md
├── infrastructure/          # Infrastructure-as-Code definitions
│   └── terraform/          # Terraform modules and configurations
├── src/                    # Application code
│   ├── dotnet/             # .NET implementations (initial)
│   │   ├── EventProducer/  # .NET service that publishes events
│   │   ├── EventConsumer/  # .NET service that consumes events
│   │   └── SimpleLambda/   # Simple .NET Lambda function example
│   ├── python/             # Python alternatives (coming soon)
│   │   ├── event-producer/ # Python service that publishes events
│   │   └── event-consumer/ # Python service that consumes events
│   ├── golang/             # Golang alternatives (coming soon)
│   │   ├── event-producer/ # Go service that publishes events
│   │   └── event-consumer/ # Go service that consumes events
│   └── node/               # Node.js alternatives (coming soon)
│       ├── event-producer/ # Node.js service that publishes events
│       └── event-consumer/ # Node.js service that consumes events
├── docker-compose.yml      # LocalStack and local services
├── .env.example           # Environment variables template
└── scripts/               # Helper scripts for setup
    ├── setup-localstack.py           # Cross-platform LocalStack setup
    ├── teardown-localstack.py        # Cross-platform LocalStack teardown
    ├── deploy-lambda-localstack.py   # Cross-platform Lambda deployment
    └── requirements.txt              # Python dependencies (optional)
```

## 💻 Backend Implementations

This playground includes multiple backend implementations to experiment with different languages and their AWS SDKs:

- **.NET** (Initial): Full implementation with C# and AWS SDK for .NET
- **Python** (Planned): Alternative implementation using boto3
- **Golang** (Planned): Alternative implementation using AWS SDK for Go
- **Node.js** (Planned): Alternative implementation using AWS SDK for JavaScript/Node.js

Each implementation provides the same functionality, allowing you to compare:
- Language-specific AWS SDK patterns
- Containerization approaches
- Performance characteristics
- Developer experience across languages

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the **project root directory** (same level as `docker-compose.yml` and `README.md`) with the following configuration:

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your-account-id

# LocalStack Configuration (for local development)
LOCALSTACK_ENDPOINT=http://localhost:4566
USE_LOCALSTACK=false

# Application Configuration
LOG_LEVEL=INFO
```

**Location:** `aws-eventbridge-ecs-playground/.env`

**Note:** The `.env` file is already in `.gitignore`, so it won't be committed to version control. Create it locally for your development environment.

### AWS Permissions Required

- ECS: Create clusters, services, task definitions
- EventBridge: Create rules, targets, event buses
- IAM: Create roles and policies
- VPC: Create networking resources (if needed)
- CloudWatch: Create log groups

## 🧪 Testing

### Build and Test .NET Services

```bash
# Build .NET services
cd src/dotnet/EventProducer
dotnet build
dotnet test

cd ../EventConsumer
dotnet build
dotnet test
```

### Deploy and Test .NET Lambda in LocalStack

```bash
# Start LocalStack (if not already running)
docker-compose up -d

# Deploy the Lambda function
python scripts/deploy-lambda-localstack.py

# Invoke the Lambda
aws --endpoint-url=http://localhost:4566 lambda invoke \
  --function-name simple-lambda \
  --payload '{"test":"data"}' \
  response.json

# View the response
cat response.json  # Linux/Mac
# or
Get-Content response.json  # Windows PowerShell
```

See `src/dotnet/SimpleLambda/README.md` for more details.

### Using LocalStack

LocalStack provides AWS service emulation via the API endpoint at `http://localhost:4566`.

**Example commands:**
```bash
# List S3 buckets
aws --endpoint-url=http://localhost:4566 s3 ls

# List Lambda functions
aws --endpoint-url=http://localhost:4566 lambda list-functions

# List EventBridge rules
aws --endpoint-url=http://localhost:4566 events list-rules
```

### Test with LocalStack

```bash
# Start LocalStack
docker-compose up -d

# Deploy infrastructure
cd infrastructure/terraform
terraform apply

# Send test event
aws --endpoint-url=http://localhost:4566 events put-events \
  --entries '[{"Source":"test","DetailType":"Test Event","Detail":"{\"message\":\"Hello\"}"}]'

# Check logs
docker-compose logs -f
```

### Test with AWS

```bash
# Deploy to AWS
cd infrastructure/terraform
terraform apply

# Send test event
aws events put-events \
  --entries '[{"Source":"test","DetailType":"Test Event","Detail":"{\"message\":\"Hello\"}"}]'

# View CloudWatch logs
aws logs tail /aws/ecs/playground --follow
```

## 🧹 Cleanup

### AWS
```bash
cd infrastructure/terraform
terraform destroy
```

### LocalStack
```bash
# Using the teardown script (recommended)
python scripts/teardown-localstack.py

# Or manually
docker-compose down -v
# or
localstack stop
```

## 📚 Resources

### AWS Services
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS EventBridge Documentation](https://docs.aws.amazon.com/eventbridge/)
- [LocalStack Documentation](https://docs.localstack.cloud/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

### Language-Specific SDKs
- [AWS SDK for .NET](https://docs.aws.amazon.com/sdk-for-net/)
- [AWS SDK for Python (boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) - Coming soon
- [AWS SDK for Go](https://aws.github.io/aws-sdk-go-v2/docs/) - Coming soon
- [AWS SDK for JavaScript/Node.js](https://docs.aws.amazon.com/sdk-for-javascript/v3/latest/) - Coming soon

## 🤝 Contributing

This is a playground project - feel free to experiment and extend it!

## 📝 License

MIT License - feel free to use this for learning and experimentation.

---

**Note**: This is a sample/playground project. For production use, ensure proper security practices, error handling, and monitoring are implemented.
