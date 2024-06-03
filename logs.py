import os
import subprocess


def execute_and_write_to_file(command, output_file):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            with open(output_file, 'w') as file:
                file.write(result.stdout.strip())
            return f"Output saved to {output_file}"
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    # Get the user's Desktop path
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    log_directory = os.path.join(desktop_path, "WindowsLogs")

    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    commands = [
        ("Get-WinEvent -LogName System", "system_logs.txt"),
        ("Get-WinEvent -LogName Setup", "setup_logs.txt"),
        ("Get-WinEvent -LogName Application", "application_logs.txt"),
        ("Get-ItemProperty -Path 'HKLM:/SYSTEM/CurrentControlSet/Enum/USBSTOR/*/*'", "usbstor_logs.txt"),
        ("ipconfig /displaydns", "displaydns_output.txt"),
        ("Get-WinEvent -LogName Security", "security_logs.txt")
    ]

    for command, output_file in commands:
        output_file_path = os.path.join(log_directory, output_file)
        result_message = execute_and_write_to_file(["powershell", "-Command", command], output_file_path)
        print(result_message)
