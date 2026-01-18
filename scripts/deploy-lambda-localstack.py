#!/usr/bin/env python3
"""
Cross-platform script to build and deploy .NET Lambda to LocalStack.
Works on Windows, Linux, and macOS.
"""

import os
import sys
import subprocess
import json
import urllib.request
from pathlib import Path

# Configuration
LAMBDA_NAME = "simple-lambda"
LAMBDA_DIR = Path(__file__).parent.parent / "src" / "dotnet" / "SimpleLambda"
IMAGE_NAME = "simple-lambda:latest"
REGISTRY = "localhost:4510"  # LocalStack container registry
LOCALSTACK_ENDPOINT = "http://localhost:4566"


def print_step(message: str, emoji: str = "🔨"):
    """Print a step message with emoji."""
    print(f"{emoji} {message}")


def run_command(cmd: list, check: bool = True, capture_output: bool = False) -> subprocess.CompletedProcess:
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=capture_output,
            text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {' '.join(cmd)}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print(f"Please ensure {cmd[0]} is installed and in your PATH")
        sys.exit(1)


def check_prerequisites():
    """Check if Docker, AWS CLI, and LocalStack are available."""
    print_step("Checking prerequisites...", "🔍")
    
    # Check Docker
    try:
        run_command(["docker", "--version"], capture_output=True)
    except SystemExit:
        print("❌ Docker is not installed or not in PATH")
        sys.exit(1)
    
    # Check AWS CLI
    try:
        run_command(["aws", "--version"], capture_output=True)
    except SystemExit:
        print("❌ AWS CLI is not installed or not in PATH")
        sys.exit(1)
    
    # Check if LocalStack is running
    result = run_command(
        ["docker", "ps", "--filter", "name=localstack", "--format", "{{.Names}}"],
        check=False,
        capture_output=True
    )
    if not result or not result.stdout.strip():
        print("❌ LocalStack container is not running")
        print("   Please start LocalStack first:")
        print("   python scripts/setup-localstack.py")
        print("   or")
        print("   docker-compose up -d")
        sys.exit(1)
    
    # Note: Registry check removed - Docker will handle the connection
    # If registry fails, Docker will provide the error message
    
    print("✅ Prerequisites check passed")


def build_docker_image():
    """Build the Docker image for the Lambda function."""
    print_step("Building .NET Lambda Docker image...", "🔨")
    
    if not LAMBDA_DIR.exists():
        print(f"❌ Lambda directory not found: {LAMBDA_DIR}")
        sys.exit(1)
    
    # Change to Lambda directory and build
    original_dir = Path.cwd()
    try:
        os.chdir(LAMBDA_DIR)
        run_command(["docker", "build", "-t", IMAGE_NAME, "."])
    finally:
        os.chdir(original_dir)


def tag_and_push_image():
    """Tag and push the image to LocalStack registry."""
    print_step("Tagging image for LocalStack registry...", "📦")
    run_command(["docker", "tag", IMAGE_NAME, f"{REGISTRY}/{IMAGE_NAME}"])
    
    print_step("Pushing image to LocalStack registry...", "📤")
    print("   Note: If this fails with 'connection refused', Docker may need to allow insecure registries")
    print("   Windows/Mac: Docker Desktop > Settings > Docker Engine > Add to JSON:")
    print('   "insecure-registries": ["localhost:4510"]')
    result = run_command(["docker", "push", f"{REGISTRY}/{IMAGE_NAME}"], check=False)
    if result and result.returncode != 0:
        print("\n⚠️  Push failed. Common solutions:")
        print("   1. Configure Docker insecure registry (see instructions above)")
        print("   2. Restart Docker Desktop after configuration change")
        print("   3. Check LocalStack logs: docker-compose logs localstack | grep -i registry")
        print("   4. Verify port 4510 is accessible: curl http://localhost:4510/v2/")
        sys.exit(1)


def create_or_update_lambda():
    """Create or update the Lambda function in LocalStack."""
    print_step("Creating Lambda function in LocalStack...", "📝")
    
    image_uri = f"{REGISTRY}/{IMAGE_NAME}"
    
    # Try to create the function
    create_cmd = [
        "aws",
        "--endpoint-url", LOCALSTACK_ENDPOINT,
        "lambda", "create-function",
        "--function-name", LAMBDA_NAME,
        "--package-type", "Image",
        "--code", f"ImageUri={image_uri}",
        "--role", "arn:aws:iam::000000000000:role/lambda-role",
        "--timeout", "30",
        "--memory-size", "512"
    ]
    
    result = run_command(create_cmd, check=False, capture_output=True)
    
    if result.returncode == 0:
        print("✅ Lambda function created!")
    else:
        # Function might already exist, try to update
        if "ResourceConflictException" in result.stderr or "already exists" in result.stderr.lower():
            print("⚠️  Lambda already exists, updating instead...", "⚠️")
            update_cmd = [
                "aws",
                "--endpoint-url", LOCALSTACK_ENDPOINT,
                "lambda", "update-function-code",
                "--function-name", LAMBDA_NAME,
                "--image-uri", image_uri
            ]
            run_command(update_cmd)
            print("✅ Lambda function updated!")
        else:
            print(f"❌ Failed to create Lambda function: {result.stderr}")
            sys.exit(1)


def print_test_instructions():
    """Print instructions for testing the Lambda."""
    print()
    print_step("Lambda function deployed!", "✅")
    print()
    print("🧪 Test the Lambda:")
    print(f"aws --endpoint-url={LOCALSTACK_ENDPOINT} lambda invoke \\")
    print(f"  --function-name {LAMBDA_NAME} \\")
    print('  --payload \'{"test":"data"}\' \\')
    print("  response.json")
    print()
    print("📄 View response:")
    if sys.platform == "win32":
        print("  type response.json")
    else:
        print("  cat response.json")


def main():
    """Main execution function."""
    print("🚀 Deploying .NET Lambda to LocalStack")
    print("=" * 50)
    
    check_prerequisites()
    build_docker_image()
    tag_and_push_image()
    create_or_update_lambda()
    print_test_instructions()


if __name__ == "__main__":
    main()
