#!/usr/bin/env python3
"""
Cross-platform script to tear down LocalStack development environment.
Works on Windows, Linux, and macOS.
"""

import os
import sys
import subprocess
from pathlib import Path


def print_step(message: str, emoji: str = "🧹"):
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
        print(f"⚠️  Warning: Command failed: {' '.join(cmd)}")
        if e.stderr:
            print(f"   {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"❌ Command not found: {cmd[0]}")
        print(f"Please ensure {cmd[0]} is installed and in your PATH")
        sys.exit(1)


def stop_localstack():
    """Stop LocalStack using docker-compose."""
    print_step("Stopping LocalStack...", "🛑")
    
    # Find docker-compose.yml in project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docker_compose_file = project_root / "docker-compose.yml"
    
    if not docker_compose_file.exists():
        print(f"⚠️  docker-compose.yml not found at {docker_compose_file}")
        return False
    
    # Change to project root and run docker-compose
    original_dir = Path.cwd()
    try:
        os.chdir(project_root)
        result = run_command(["docker-compose", "down"], check=False)
        if result and result.returncode == 0:
            print("✅ LocalStack stopped and containers removed")
            return True
        else:
            print("⚠️  LocalStack may not have been running")
            return False
    finally:
        os.chdir(original_dir)


def remove_volumes():
    """Optionally remove LocalStack volumes and data."""
    print_step("Checking for LocalStack data...", "📦")
    
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    localstack_data = project_root / "localstack-data"
    
    if localstack_data.exists():
        print(f"   Found data directory: {localstack_data}")
        response = input("   Remove LocalStack data? This will delete all persisted state. (y/N): ")
        if response.lower() == 'y':
            import shutil
            try:
                shutil.rmtree(localstack_data)
                print("✅ LocalStack data removed")
            except Exception as e:
                print(f"❌ Failed to remove data: {e}")
        else:
            print("   Skipping data removal")
    else:
        print("   No LocalStack data directory found")


def cleanup_containers():
    """Clean up any orphaned LocalStack containers."""
    print_step("Checking for orphaned containers...", "🔍")
    
    # Check for LocalStack containers
    result = run_command(
        ["docker", "ps", "-a", "--filter", "name=localstack", "--format", "{{.Names}}"],
        check=False,
        capture_output=True
    )
    
    if result and result.stdout.strip():
        containers = result.stdout.strip().split('\n')
        print(f"   Found containers: {', '.join(containers)}")
        response = input("   Remove orphaned LocalStack containers? (y/N): ")
        if response.lower() == 'y':
            for container in containers:
                run_command(["docker", "rm", "-f", container], check=False)
            print("✅ Orphaned containers removed")
        else:
            print("   Skipping container removal")
    else:
        print("   No orphaned containers found")


def cleanup_images():
    """Optionally remove LocalStack Docker images."""
    print_step("Checking for LocalStack images...", "🖼️")
    
    result = run_command(
        ["docker", "images", "localstack/localstack", "--format", "{{.ID}}"],
        check=False,
        capture_output=True
    )
    
    if result and result.stdout.strip():
        image_ids = set(result.stdout.strip().split('\n'))
        print(f"   Found {len(image_ids)} LocalStack image(s)")
        response = input("   Remove LocalStack Docker images? (y/N): ")
        if response.lower() == 'y':
            for image_id in image_ids:
                run_command(["docker", "rmi", image_id], check=False)
            print("✅ LocalStack images removed")
        else:
            print("   Skipping image removal")
    else:
        print("   No LocalStack images found")


def main():
    """Main execution function."""
    print("🧹 Tearing down LocalStack development environment")
    print("=" * 50)
    
    # Stop LocalStack
    stopped = stop_localstack()
    
    if not stopped:
        print("\n⚠️  LocalStack may not have been running")
        response = input("Continue with cleanup anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(0)
    
    # Ask about data removal
    print()
    remove_volumes()
    
    # Ask about orphaned containers
    print()
    cleanup_containers()
    
    # Ask about images (optional, usually skip)
    print()
    response = input("Remove LocalStack Docker images? Usually not needed. (y/N): ")
    if response.lower() == 'y':
        cleanup_images()
    else:
        print("   Skipping image removal (recommended to keep for faster restarts)")
    
    print()
    print_step("Teardown complete!", "✅")
    print()
    print("To start LocalStack again, run:")
    print("  python scripts/setup-localstack.py")


if __name__ == "__main__":
    main()
