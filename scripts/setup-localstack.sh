#!/bin/bash

# Setup script for LocalStack development environment

set -e

echo "🚀 Setting up LocalStack development environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Start LocalStack
echo "📦 Starting LocalStack..."
docker-compose up -d localstack

# Wait for LocalStack to be ready
echo "⏳ Waiting for LocalStack to be ready..."
timeout=60
counter=0
until curl -s http://localhost:4566/_localstack/health > /dev/null; do
    if [ $counter -ge $timeout ]; then
        echo "❌ LocalStack failed to start within $timeout seconds"
        exit 1
    fi
    echo "   Waiting... ($counter/$timeout)"
    sleep 2
    counter=$((counter + 2))
done

echo "✅ LocalStack is ready!"

# Configure AWS CLI environment variables
echo ""
echo "📝 Configure your environment:"
echo "export AWS_ENDPOINT_URL=http://localhost:4566"
echo "export AWS_ACCESS_KEY_ID=test"
echo "export AWS_SECRET_ACCESS_KEY=test"
echo "export AWS_DEFAULT_REGION=us-east-1"
echo ""
echo "Or add these to your .env file:"
echo "LOCALSTACK_ENDPOINT=http://localhost:4566"
echo "USE_LOCALSTACK=true"
echo ""
echo "🎉 Setup complete! You can now deploy infrastructure to LocalStack."
