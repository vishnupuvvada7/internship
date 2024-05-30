import subprocess


def get_service_startup_type(service_name):
    try:
        output = subprocess.run(['sc', 'qc', service_name], capture_output=True, text=True)
        startup_type_line = [line.strip() for line in output.stdout.split('\n') if "START_TYPE" in line]
        if startup_type_line:
            startup_type = startup_type_line[0].split(':')[1].strip()
            return startup_type
        else:
            return "Error: Startup type not found"
    except Exception as e:
        return f"Error: {str(e)}"

services = ["bthserv", "lfsvc", "PlugPlay", "HvHost", "RpcLocator", "WFDSConMgrSvc", "RemoteAccess", "XblGameSave", "SessionEnv"]





def get_max_password_age():
    try:
        output = subprocess.run(['net', 'accounts'], capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        for line in lines:
            if "Maximum password age" in line:
                return line.split(":")[-1].strip()
        return "Error: Policy not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_min_password_age():
    try:
        output = subprocess.run(['net', 'accounts'], capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        for line in lines:
            if "Minimum password age" in line:
                return line.split(":")[-1].strip()
        return "Error: Policy not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_min_password_length():
    try:
        output = subprocess.run(['net', 'accounts'], capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        for line in lines:
            if "Minimum password length" in line:
                return line.split(":")[-1].strip()
        return "Error: Policy not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_account_lockout_threshold():
    try:
        output = subprocess.run(['net', 'accounts'], capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        for line in lines:
            if "Lockout threshold" in line:
                return line.split(":")[-1].strip()
        return "Error: Policy not found"
    except Exception as e:
        return f"Error: {str(e)}"

def get_account_lockout_duration():
    try:
        output = subprocess.run(['net', 'accounts'], capture_output=True, text=True)
        lines = output.stdout.strip().split('\n')
        for line in lines:
            if "Lockout duration" in line:
                return line.split(":")[-1].strip()
        return "Error: Policy not found"
    except Exception as e:
        return f"Error: {str(e)}"

def is_bitlocker_enabled():
    try:
        output = subprocess.run(['manage-bde', '-status'], capture_output=True, text=True)
        output_lines = output.stdout.split('\n')

        protection_status = "Unknown"

        for line in output_lines:
            if "Protection Status:" in line:
                protection_status = line.split(":")[1].strip()

        if protection_status == "Protection Off":
            return "Disabled"
        else:
            return "Enabled"

    except Exception as e:
        return f"Error: {str(e)}"


def print_service_status():
    try:
        status_msg = ""  # Initialize an empty string to store service status messages
        
        # Iterate through each service and append its status message to status_msg
        for service in services:
            startup_type = get_service_startup_type(service)
            status_msg += f"Service: {service}, Startup Type: {startup_type}\n"

        # Retrieve other system status information
        max_password_age = get_max_password_age()
        min_password_age = get_min_password_age()
        min_password_length = get_min_password_length()
        account_lockout_threshold = get_account_lockout_threshold()
        account_lockout_duration = get_account_lockout_duration()
        bitlocker_status = is_bitlocker_enabled()
        
        # Append other system status information to status_msg
        status_msg += f"\nMaximum password age set to: {max_password_age}\n"
        status_msg += f"Minimum password age set to: {min_password_age}\n"
        status_msg += f"Minimum password length set to: {min_password_length}\n"
        status_msg += f"Account lockout threshold set to: {account_lockout_threshold}\n"
        status_msg += f"Account lockout duration set to: {account_lockout_duration}\n"
        status_msg += f"Bitlocker Status: {bitlocker_status}\n"

        return status_msg 
    except Exception as e:
        return f"Error: {str(e)}"



if __name__ == "__main__":
    print(print_service_status())
