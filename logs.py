import os
import subprocess

def execute_and_write_to_file(command, output_file):
    try:
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            # Save the output to the specified file
            with open(output_file, 'w') as file:
                file.write(result.stdout.strip())
            return f"Output saved to {output_file}"
        else:
            # Return the error message
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        # Return the exception message
        return f"Error: {e}"

if __name__ == "__main__":
    # Create a directory to store logs if it doesn't exist
    log_directory = "WindowsLogs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    
    # Define commands and output files
    commands = [
        ("Get-WinEvent -LogName System", "system_logs.txt"),
        ("Get-WinEvent -LogName Setup", "setup_logs.txt"),
        ("Get-WinEvent -LogName Application", "application_logs.txt"),
        ("Get-ItemProperty -Path 'HKLM:/SYSTEM/CurrentControlSet/Enum/USBSTOR/*/*'", "usbstor_logs.txt"),
        ("ipconfig /displaydns", "displaydns_output.txt"),
        ("Get-WinEvent -LogName Security", "security_logs.txt")
    ]
    
    # Execute each command and save output to file
    for command, output_file in commands:
        output_file_path = os.path.join(log_directory, output_file)
        print(execute_and_write_to_file(["powershell", "-Command", command], output_file_path))
