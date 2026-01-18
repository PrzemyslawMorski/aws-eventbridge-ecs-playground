#!/usr/bin/env python3
"""
Deployment script for .NET Lambda functions using ZIP package.
"""

import os
import sys
import subprocess
import zipfile
import shutil
from pathlib import Path

# Configuration
LAMBDA_NAME = "simple-lambda"
LAMBDA_DIR = Path(__file__).parent.parent / "src" / "dotnet" / "SimpleLambda"
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
    """Check if prerequisites are available."""
    print_step("Checking prerequisites...", "🔍")
    
    # Check .NET SDK
    try:
        run_command(["dotnet", "--version"], capture_output=True)
    except SystemExit:
        print("❌ .NET SDK is not installed or not in PATH")
        sys.exit(1)
    
    # Check AWS CLI
    try:
        run_command(["aws", "--version"], capture_output=True)
    except SystemExit:
        print("❌ AWS CLI is not installed or not in PATH")
        sys.exit(1)
    
    # Check LocalStack
    import urllib.request
    try:
        with urllib.request.urlopen(f"{LOCALSTACK_ENDPOINT}/_localstack/health", timeout=2) as response:
            if response.status == 200:
                print("✅ Prerequisites check passed")
                return
    except Exception:
        pass
    
    print("❌ LocalStack is not accessible")
    print("   Start it with: python scripts/setup-localstack.py")
    sys.exit(1)


def build_and_package():
    """Build the .NET Lambda and create a ZIP package."""
    print_step("Building .NET Lambda...", "🔨")
    
    if not LAMBDA_DIR.exists():
        print(f"❌ Lambda directory not found: {LAMBDA_DIR}")
        sys.exit(1)
    
    original_dir = Path.cwd()
    try:
        os.chdir(LAMBDA_DIR)
        
        # Clean previous builds
        if (LAMBDA_DIR / "bin").exists():
            shutil.rmtree(LAMBDA_DIR / "bin")
        if (LAMBDA_DIR / "obj").exists():
            shutil.rmtree(LAMBDA_DIR / "obj")
        
        # Build and publish
        print("   Publishing Lambda function...")
        run_command(["dotnet", "publish", "-c", "Release", "-o", "publish"])
        
        # Create ZIP package
        print_step("Creating ZIP package...", "📦")
        zip_path = LAMBDA_DIR / "lambda.zip"
        if zip_path.exists():
            zip_path.unlink()
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            publish_dir = LAMBDA_DIR / "publish"
            for file in publish_dir.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(publish_dir)
                    zipf.write(file, arcname)
        
        print(f"✅ Package created: {zip_path}")
        return zip_path
        
    finally:
        os.chdir(original_dir)


def deploy_lambda(zip_path: Path):
    """Deploy the Lambda function using ZIP package."""
    print_step("Deploying Lambda function...", "📝")
    
    # Read the ZIP file
    with open(zip_path, 'rb') as f:
        zip_content = f.read()
    
    # Create Lambda function
    create_cmd = [
        "aws",
        "--endpoint-url", LOCALSTACK_ENDPOINT,
        "lambda", "create-function",
        "--function-name", LAMBDA_NAME,
        "--runtime", "provided.al2",  # Use provided runtime for custom .NET
        "--role", "arn:aws:iam::000000000000:role/lambda-role",
        "--handler", "SimpleLambda::SimpleLambda.Function::FunctionHandler",
        "--zip-file", f"fileb://{zip_path}",
        "--timeout", "30",
        "--memory-size", "512"
    ]
    
    result = run_command(create_cmd, check=False, capture_output=True)
    
    if result.returncode == 0:
        print("✅ Lambda function created!")
    else:
        # Function might already exist, try updating
        if "ResourceConflictException" in result.stderr or "already exists" in result.stderr.lower():
            print("⚠️  Lambda already exists, updating code...")
            update_cmd = [
                "aws",
                "--endpoint-url", LOCALSTACK_ENDPOINT,
                "lambda", "update-function-code",
                "--function-name", LAMBDA_NAME,
                "--zip-file", f"fileb://{zip_path}"
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
    print("🚀 Deploying .NET Lambda to LocalStack (ZIP package)")
    print("=" * 50)
    
    check_prerequisites()
    zip_path = build_and_package()
    deploy_lambda(zip_path)
    print_test_instructions()


if __name__ == "__main__":
    main()
