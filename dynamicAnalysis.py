import docker
import win32evtlog
import time

# Import Sysmon Event IDs for tracking purposes
SYSMON_PROCESS_CREATE = 1      # Process Creation
SYSMON_FILE_CREATE = 11        # File Creation
SYSMON_NETWORK_CONNECT = 3     # Network Connection

# Docker client setup
client = docker.from_env()

def start_docker_container(image_name, container_name="test_container"):
    """
    Start a Docker container with the specified image and name.
    """
    try:
        # Run the container
        container = client.containers.run(
            image_name, 
            name=container_name, 
            detach=True
        )
        print(f"Container '{container_name}' started with ID: {container.id}")
        return container
    except docker.errors.ContainerError as e:
        print(f"Error starting container: {e}")
        return None

def monitor_sysmon_for_docker(container_name):
    """
    Monitor Sysmon events for suspicious activity related to the specified Docker container.
    """
    server = 'localhost'
    log_type = "Microsoft-Windows-Sysmon/Operational"
    handle = win32evtlog.OpenEventLog(server, log_type)
    flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    print(f"Monitoring Sysmon events for Docker container '{container_name}'...\n")

    try:
        while True:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
            if events:
                for event in events:
                    if event.EventID in [SYSMON_PROCESS_CREATE, SYSMON_FILE_CREATE, SYSMON_NETWORK_CONNECT]:
                        description = event.StringInserts
                        event_data = {
                            "RecordNumber": event.RecordNumber,
                            "TimeGenerated": event.TimeGenerated,
                            "EventID": event.EventID,
                            "ComputerName": event.ComputerName,
                            "Description": description
                        }

                        # Check if event is related to the Docker container
                        if container_name in str(description):
                            print("Potential malicious activity detected in Docker container:")
                            print(f"Record Number: {event_data['RecordNumber']}")
                            print(f"Event ID: {event_data['EventID']}")
                            print(f"Time Generated: {event_data['TimeGenerated']}")
                            print(f"Description: {event_data['Description']}")
                            print("\n-----------------------------\n")

            time.sleep(2)  # Avoid excessive CPU usage
    except KeyboardInterrupt:
        print("Stopping monitoring.")
    finally:
        win32evtlog.CloseEventLog(handle)

# Main Execution
if __name__ == "__main__":
    container_image = "your_docker_image"  # Replace with your Docker image
    container_name = "test_container"  # Specify your container name

    # Start Docker container
    container = start_docker_container(container_image, container_name)

    # Start monitoring Sysmon events if the container was started successfully
    if container:
        try:
            monitor_sysmon_for_docker(container_name)
        finally:
            # Stop and remove the container after monitoring
            print("Stopping and removing the container...")
            container.stop()
            container.remove()


##import docker
##import os
##import sys
##import win32evtlog
##import win32con
##
##def monitor_file():
##    
##
### Sysmon Event IDs for monitoring
##SYSMON_PROCESS_CREATE = 1  # Process Creation
##SYSMON_FILE_CREATE = 11    # File Creation
##SYSMON_NETWORK_CONNECT = 3  # Network Connection
##
##def monitor_sysmon_for_docker(container_name="test_container"):
##    # Connect to the Sysmon event log
##    server = 'localhost'
##    log_type = "Microsoft-Windows-Sysmon/Operational"
##
##    # Open the Event Log
##    handle = win32evtlog.OpenEventLog(server, log_type)
##    flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
##
##    print(f"Monitoring Sysmon events for Docker container '{container_name}'...\n")
##    
##    try:
##        while True:
##            events = win32evtlog.ReadEventLog(handle, flags, 0)
##            if events:
##                for event in events:
##                    if event.EventID in [SYSMON_PROCESS_CREATE, SYSMON_FILE_CREATE, SYSMON_NETWORK_CONNECT]:
##                        # Extract event data
##                        description = event.StringInserts
##                        event_data = {
##                            "RecordNumber": event.RecordNumber,
##                            "TimeGenerated": event.TimeGenerated,
##                            "EventID": event.EventID,
##                            "ComputerName": event.ComputerName,
##                            "Description": description
##                        }
##
##                        # Check if event is related to the Docker container
##                        if container_name in str(description):
##                            print("Potential malicious activity detected in Docker container:")
##                            print(f"Record Number: {event_data['RecordNumber']}")
##                            print(f"Event ID: {event_data['EventID']}")
##                            print(f"Time Generated: {event_data['TimeGenerated']}")
##                            print(f"Description: {event_data['Description']}")
##                            print("\n-----------------------------\n")
##    except KeyboardInterrupt:
##        print("Stopping monitoring.")
##    finally:
##        win32evtlog.CloseEventLog(handle)
##
### Run the monitor function
##monitor_sysmon_for_docker("test_container")
##
##
##def create_container():
##    # Initialize Docker client
##    client = docker.from_env()
##
##    # Define paths
##    script_path = "/path/to/malicious_script.py"  # Path to the Python script you want to analyze
##    log_path = "/path/to/output/logs"  # Directory to store logs and analysis output
##
##    # Ensure the paths are correct and accessible
##    if not os.path.exists(script_path):
##        sys.exit("Script path does not exist.")
##
##    # Ensure log directory exists
##    os.makedirs(log_path, exist_ok=True)
##
##    # Define Docker container configurations
##    container_config = {
##        "image": "python:3.9-slim",  # Slim image with Python pre-installed
##        "command": f"python /analyze/malicious_script.py",  # Command to run the script
##        "volumes": {
##            os.path.abspath(script_path): {
##                "bind": "/analyze/malicious_script.py",
##                "mode": "ro",  # Read-only to prevent modifications
##            },
##            os.path.abspath(log_path): {
##                "bind": "/analyze/logs",
##                "mode": "rw",  # Read-write to store logs
##            },
##        },
##        "auto_remove": True,  # Clean up after execution
##        "detach": True,
##        "tty": True,
##        "network_disabled": True,  # Disable network access for safety
##    }
##
##    # Run the container
##    try:
##        container = client.containers.run(**container_config)
##        print("Container started, analyzing the script...")
##
##        # Wait for the container to finish execution
##        result = container.wait()
##        print("Analysis complete.")
##
##        # Fetch logs from the container
##        container_logs = container.logs().decode("utf-8")
##        log_file_path = os.path.join(log_path, "analysis_log.txt")
##        with open(log_file_path, "w") as log_file:
##            log_file.write(container_logs)
##
##        print(f"Analysis logs written to: {log_file_path}")
##
##    except docker.errors.ContainerError as e:
##        print("Container error:", e)
##    except docker.errors.ImageNotFound:
##        print("Docker image not found.")
##    except Exception as e:
##        print("An error occurred:", e)
##
##    finally:
##        # Cleanup
##        if 'container' in locals():
##            container.remove(force=True)
