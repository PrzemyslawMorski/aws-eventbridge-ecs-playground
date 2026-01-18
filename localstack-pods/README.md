# LocalStack Cloud Pods

This directory is for LocalStack Cloud Pods (state snapshots).

Cloud Pods allow you to save and restore the state of your LocalStack services.

## Usage

1. **Save a Cloud Pod:**
   ```bash
   awslocal pod save my-pod-name
   ```

2. **Load a Cloud Pod:**
   ```bash
   awslocal pod load my-pod-name
   ```

3. **Automatic Loading:**
   Place `.pod` files in this directory and they will be automatically loaded when LocalStack starts (if `AUTO_LOAD_POD=1` is set).

## Placeholder

This directory is set up for future use. No pods are currently configured.
