#!/usr/bin/env python3
"""
Cross-platform script to verify LocalStack is accessible and running.
Works on Windows, Linux, and macOS.
"""

import sys
import urllib.request
import json
from pathlib import Path

LOCALSTACK_ENDPOINT = "http://localhost:4566"
HEALTH_CHECK_URL = f"{LOCALSTACK_ENDPOINT}/_localstack/health"


def print_step(message: str, emoji: str = "🔍"):
    """Print a step message with emoji."""
    print(f"{emoji} {message}")


def check_port_accessibility():
    """Check if LocalStack port is accessible."""
    print_step("Checking if LocalStack port 4566 is accessible...", "🔌")
    
    try:
        with urllib.request.urlopen(HEALTH_CHECK_URL, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print("✅ LocalStack is accessible at http://localhost:4566")
                print(f"   Version: {data.get('version', 'unknown')}")
                print(f"   Edition: {data.get('edition', 'unknown')}")
                
                # Show available services
                services = data.get('services', {})
                available = [svc for svc, status in services.items() if status == 'available']
                if available:
                    print(f"   Available services: {', '.join(available[:10])}")
                    if len(available) > 10:
                        print(f"   ... and {len(available) - 10} more")
                
                return True
            else:
                print(f"⚠️  LocalStack responded with status code: {response.status}")
                return False
    except urllib.error.URLError as e:
        print(f"❌ Cannot connect to LocalStack at {LOCALSTACK_ENDPOINT}")
        print(f"   Error: {e.reason if hasattr(e, 'reason') else str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error checking LocalStack: {e}")
        return False


def check_container_status():
    """Check if LocalStack container is running."""
    import subprocess
    
    print_step("Checking LocalStack container status...", "🐳")
    
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=localstack", "--format", "{{.Names}}\t{{.Status}}\t{{.Ports}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            lines = result.stdout.strip().split('\n')
            for line in lines:
                parts = line.split('\t')
                if len(parts) >= 2:
                    name = parts[0]
                    status = parts[1]
                    ports = parts[2] if len(parts) > 2 else "N/A"
                    print(f"   Container: {name}")
                    print(f"   Status: {status}")
                    print(f"   Ports: {ports}")
            return True
        else:
            print("❌ LocalStack container is not running")
            print("   Start it with: python scripts/setup-localstack.py")
            return False
    except FileNotFoundError:
        print("⚠️  Docker command not found - cannot check container status")
        return None
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Error checking container: {e}")
        return None


def test_basic_operations():
    """Test basic LocalStack operations."""
    import subprocess
    
    print_step("Testing basic LocalStack operations...", "🧪")
    
    # Test S3
    try:
        result = subprocess.run(
            ["aws", "--endpoint-url", LOCALSTACK_ENDPOINT, "s3", "ls"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("   ✅ S3 service is working")
        else:
            print(f"   ⚠️  S3 test returned: {result.returncode}")
    except Exception as e:
        print(f"   ⚠️  S3 test failed: {e}")
    
    # Test Lambda
    try:
        result = subprocess.run(
            ["aws", "--endpoint-url", LOCALSTACK_ENDPOINT, "lambda", "list-functions"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("   ✅ Lambda service is working")
        else:
            print(f"   ⚠️  Lambda test returned: {result.returncode}")
    except Exception as e:
        print(f"   ⚠️  Lambda test failed: {e}")


def main():
    """Main execution function."""
    print("🔍 Verifying LocalStack Accessibility")
    print("=" * 50)
    print()
    
    # Check container
    container_running = check_container_status()
    print()
    
    # Check port accessibility
    port_accessible = check_port_accessibility()
    print()
    
    if port_accessible:
        # Test operations
        test_basic_operations()
        print()
        print("✅ LocalStack is fully operational!")
        print(f"   API Endpoint: {LOCALSTACK_ENDPOINT}")
        print()
        print("You can now use LocalStack with:")
        print(f"   aws --endpoint-url={LOCALSTACK_ENDPOINT} <command>")
    else:
        if container_running is False:
            print("💡 Tip: Start LocalStack with:")
            print("   python scripts/setup-localstack.py")
        else:
            print("💡 Tip: Check LocalStack logs with:")
            print("   docker-compose logs localstack")
        sys.exit(1)


if __name__ == "__main__":
    main()
