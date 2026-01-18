#!/usr/bin/env python3
"""
Cross-platform script to set up LocalStack development environment.
Works on Windows, Linux, and macOS.
"""

import os
import sys
import subprocess
import time
import urllib.request
from pathlib import Path

LOCALSTACK_ENDPOINT = "http://localhost:4566"
HEALTH_CHECK_URL = f"{LOCALSTACK_ENDPOINT}/_localstack/health"
TIMEOUT = 60


def print_step(message: str, emoji: str = "🚀"):
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


def check_docker():
    """Check if Docker is running."""
    print_step("Checking if Docker is running...", "🔍")
    try:
        run_command(["docker", "info"], capture_output=True)
        print("✅ Docker is running")
    except SystemExit:
        print("❌ Docker is not running. Please start Docker and try again.")
        sys.exit(1)


def start_localstack():
    """Start LocalStack using docker-compose."""
    print_step("Starting LocalStack...", "📦")
    
    # Find docker-compose.yml in project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docker_compose_file = project_root / "docker-compose.yml"
    
    if not docker_compose_file.exists():
        print(f"❌ docker-compose.yml not found at {docker_compose_file}")
        sys.exit(1)
    
    # Change to project root and run docker-compose
    original_dir = Path.cwd()
    try:
        os.chdir(project_root)
        run_command(["docker-compose", "up", "-d", "localstack"])
    finally:
        os.chdir(original_dir)


def wait_for_localstack():
    """Wait for LocalStack to be ready."""
    print_step("Waiting for LocalStack to be ready...", "⏳")
    
    counter = 0
    while counter < TIMEOUT:
        try:
            with urllib.request.urlopen(HEALTH_CHECK_URL, timeout=2) as response:
                if response.status == 200:
                    print("✅ LocalStack is ready!")
                    return
        except (urllib.error.URLError, OSError, TimeoutError):
            pass
        
        print(f"   Waiting... ({counter}/{TIMEOUT})")
        time.sleep(2)
        counter += 2
    
    print(f"❌ LocalStack failed to start within {TIMEOUT} seconds")
    sys.exit(1)


def print_environment_setup():
    """Print instructions for environment setup."""
    print()
    print_step("Setup complete! Configure your environment:", "🎉")
    print()
    
    if sys.platform == "win32":
        print("Windows (PowerShell):")
        print(f'$env:AWS_ENDPOINT_URL="{LOCALSTACK_ENDPOINT}"')
        print('$env:AWS_ACCESS_KEY_ID="test"')
        print('$env:AWS_SECRET_ACCESS_KEY="test"')
        print('$env:AWS_DEFAULT_REGION="us-east-1"')
    else:
        print("Linux/Mac:")
        print(f"export AWS_ENDPOINT_URL={LOCALSTACK_ENDPOINT}")
        print("export AWS_ACCESS_KEY_ID=test")
        print("export AWS_SECRET_ACCESS_KEY=test")
        print("export AWS_DEFAULT_REGION=us-east-1")
    
    print()
    print("Or add these to your .env file:")
    print(f"LOCALSTACK_ENDPOINT={LOCALSTACK_ENDPOINT}")
    print("USE_LOCALSTACK=true")
    print()
    print("🎉 You can now deploy infrastructure to LocalStack.")


def main():
    """Main execution function."""
    print("🚀 Setting up LocalStack development environment")
    print("=" * 50)
    
    check_docker()
    start_localstack()
    wait_for_localstack()
    print_environment_setup()


if __name__ == "__main__":
    main()
