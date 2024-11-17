##import docker
##
##client = docker.from_env()
##print(client.containers.run("alpine",["echo","hello","world"]))
##
##'''for i in client.containers.list():
##    print(i.id)
##'''
import docker
import os
import sys

# Initialize Docker client
client = docker.from_env()

# Define paths
script_path = "C:/Users/vskof/Onedrive/Desktop/hello_file.py"  # Path to the Python script you want to analyze
log_path = "C:/Users/vskof/Onedrive/Desktop/hello_logs"  # Directory to store logs and analysis output

# Ensure the paths are correct and accessible
if not os.path.exists(script_path):
    sys.exit("Script path does not exist.")

# Ensure log directory exists
os.makedirs(log_path, exist_ok=True)

# Define Docker container configurations
container_config = {
    "image": "python:3.9-slim",  # Slim image with Python pre-installed
    "command": f"python C:/Users/vskof/Onedrive/Desktop/hello_file.py",  # Command to run the script
    "volumes": {
        os.path.abspath(script_path): {
            "bind": "C:/Users/vskof/Onedrive/Desktop/hello_file.py",
            "mode": "ro",  # Read-only to prevent modifications
        },
        os.path.abspath(log_path): {
            "bind": "C:/Users/vskof/Onedrive/Desktop/hello_logs",
            "mode": "rw",  # Read-write to store logs
        },
    },
    "auto_remove": True,  # Clean up after execution
    "detach": True,
    "tty": True,
    "network_disabled": True,  # Disable network access for safety
}

# Run the container
try:
    container = client.containers.run(**container_config)
    print("Container started, analyzing the script...")

    # Wait for the container to finish execution
    result = container.wait()
    print("Analysis complete.")

    # Fetch logs from the container
    container_logs = container.logs().decode("utf-8")
    log_file_path = os.path.join(log_path, "analysis_log.txt")
    with open(log_file_path, "w") as log_file:
        log_file.write(container_logs)

    print(f"Analysis logs written to: {log_file_path}")

except docker.errors.ContainerError as e:
    print("Container error:", e)
except docker.errors.ImageNotFound:
    print("Docker image not found.")
except Exception as e:
    print("An error occurred:", e)

finally:
    # Cleanup
    if 'container' in locals():
        container.remove(force=True)

