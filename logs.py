import subprocess


def get_logs(log_name, output_file):
    try:
        # Use the 'wevtutil' command to query logs
        process = subprocess.run(['wevtutil', 'qe', log_name, '/rd:true', '/f:text'], capture_output=True, text=True)

        if process.returncode == 0:
            with open(output_file, "w") as file:
                file.write(process.stdout)
            print(f"{log_name} logs saved to '{output_file}'.")
        else:
            print(f"Error querying {log_name} logs:", process.stderr)
    except Exception as e:
        print(f"An error occurred while querying {log_name} logs:", str(e))

def execute_and_write_to_file(command, filename):
    try:
        # Execute the command
        process = subprocess.run(command, shell=True, capture_output=True, text=True)

        if process.returncode == 0:
            with open(filename, "w") as file:
                file.write(process.stdout)
            print(f"'{command}' output saved to {filename}.")
        else:
            print(f"Error executing '{command}':", process.stderr)
    except Exception as e:
        print(f"Error executing '{command}':", str(e))

if __name__ == "__main__":
    get_logs('System', 'system_logs.txt')
    get_logs('Setup', 'setup_logs.txt')
    get_logs('Application', 'application_logs.txt')
    execute_and_write_to_file("ipconfig /displaydns", "displaydns_output.txt")
