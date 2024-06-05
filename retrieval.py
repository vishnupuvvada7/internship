import subprocess
import os
import wmi
import winreg
import psutil
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(content):
    doc = SimpleDocTemplate("system_info.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create a list to hold the content
    elements = []
    
    for title, data in content.items():
        # Add title with bold and underline style
        elements.append(Paragraph("<u><b>{}</b></u>".format(title), styles['Title']))
        
        # Add data with normal style
        lines = data.split('\n')
        for line in lines:
            elements.append(Paragraph(line, styles['Normal']))
            elements.append(Spacer(1, 12))  # Add a spacer for a new line
    
    # Build the PDF
    doc.build(elements)


def execute_command(command):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout


def extract_network_info(ipconfig_output):
    lines = ipconfig_output.splitlines()
    info = ""
    for line in lines:
        if "IPv4 Address" in line or "IPv6 Address" in line or "Physical Address" in line or "Host Name" in line:
            info += line + "\n"
    return info



def check_antivirus():
    # PowerShell script content
    powershell_script = '''
    $antivirus = Get-WmiObject -Namespace "root\\SecurityCenter2" -Class AntiVirusProduct
    if ($antivirus) {
        Write-Output "Antivirus software is installed."
        foreach ($product in $antivirus) {
            Write-Output "Product Name: $($product.displayName)"
        }
    } else {
        Write-Output "No antivirus software is installed."
    }
    '''

    # Execute the PowerShell script
    result = subprocess.run(["powershell.exe", "-Command", powershell_script], capture_output=True, text=True)

    # Check if the script executed successfully
    if result.returncode == 0:
        antivirus_output = result.stdout
        return antivirus_output
    else:
        error_message = result.stderr
        return f"Error executing PowerShell script: {error_message}"


def get_last_update_date():
    c = wmi.WMI()
    last_update_date = ""
    for update in c.Win32_QuickFixEngineering():
        if update.InstalledOn is not None:
            last_update_date = update.InstalledOn
            break
    return f"Last Windows Update Installed On: {last_update_date}" if last_update_date else "No updates found or unable to retrieve the last update date."

def get_license_info():
    license_info = execute_command("cscript C:/Windows/System32/slmgr.vbs /dli")
    return license_info

def is_bios_password_set():
    c = wmi.WMI()
    for bios in c.Win32_BIOS():
        if bios.SerialNumber:
            return "Yes"
    return "No"

def get_user_information():
    user_info = ""
    c = wmi.WMI()
    for user in c.Win32_UserAccount():
        is_admin = "Yes" if user.AccountType in [544, 512] else "No"
        user_info += f"User: {user.Name} | Is Admin: {is_admin}\n"
    user_info += f"Total Users: {len(c.Win32_UserAccount())}\n"
    return user_info

def run_net_share_command():
    command_output = execute_command("cmd /c net share")
    return f"=== Shared Folders Data ===\n{command_output}"

def get_system_utilization():
    cpu_utilization = psutil.cpu_percent()
    memory_utilization = psutil.virtual_memory().percent
    return f"CPU Utilization: {cpu_utilization}%\nMemory Utilization: {memory_utilization}%\n"

def get_desktop_folder_count():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    if os.path.exists(desktop_path) and os.path.isdir(desktop_path):
        items_count = len(os.listdir(desktop_path))
        return f"Items on Desktop Folder: {items_count}"
    else:
        return "Desktop folder not found or inaccessible."
    


def run_powershell_command(command):
    try:
        # Execute the PowerShell command
        result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True, shell=True)
        
        # Check if the command executed successfully
        if result.returncode == 0:
            # Return the output
            return result.stdout.strip()
        else:
            # Return the error message
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        # Return the exception message
        return f"Error: {e}"

# Define the PowerShell command for USB logs
usb_logs_command = "Get-ItemProperty -Path 'HKLM:/SYSTEM/CurrentControlSet/Enum/USBSTOR/*/*' | Select FriendlyName"

# Run the PowerShell command for USB logs and get the output as a string
usb_logs_output = run_powershell_command(usb_logs_command)



def run_batch_file(file_path):
    try:
        result = subprocess.check_output([file_path], shell=True, text=True)
        return result.strip()  # Remove leading/trailing whitespace
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"


    

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
        
        result = subprocess.run(["powershell.exe", "-Command", "Get-WindowsOptionalFeature", "-Online", "-FeatureName", "TelnetClient"], capture_output=True, text=True, shell=False)
        output = result.stdout
        if "Disabled" in output:
            status_msg += "Telnet is disabled\n"
        elif "Enabled" in output:
            status_msg += "Telnet is enabled\n"
        else:   
            status_msg += "Telnet status unknown\n"

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


def check_ipv4():
    try:
        # Execute ipconfig command and capture the output
        result = subprocess.run(['ipconfig'], capture_output=True, text=True,shell=False)
        str_output = result.stdout

        # Split the output into lines
        arr_lines = str_output.split('\n')

        # Initialize IPv4 address variable
        str_ipv4 = ""

        # Loop through each line to find the IPv4 address
        for str_line in arr_lines:
            if "IPv4 Address" in str_line:
                # Extract the IPv4 address
                arr_ipv4 = str_line.split(":")
                str_ipv4 = arr_ipv4[1].strip()
                break  # Exit the loop once IPv4 address is found

        # Check conditions based on IPv4 address
        if str_ipv4:
            if str_ipv4.startswith("10.69."):
                return "drona"
            elif str_ipv4.startswith("10.86."):
                return "ciag"
            else:
                return "standalone/project"
        else:
            return "IPv4 address not found."

    except Exception as e:
        return e



# Execute ipconfig /all
ipconfig_output = execute_command("ipconfig /all")



# Execute winver
winver_output = execute_command("ver")

# Perform checks and retrieve information
network_info = extract_network_info(ipconfig_output)
Network_Type=check_ipv4()
antivirus_info = check_antivirus()
last_update_date = get_last_update_date()
license_info = get_license_info()
bios_password_info = is_bios_password_set()
user_information = get_user_information()
shared_folders_data = run_net_share_command()
system_utilization = get_system_utilization()
desktop_folder_count = get_desktop_folder_count()
services_status = print_service_status()
usb_logs = usb_logs_output

# Construct content dictionary
content = {
    "IP Configuration": network_info,
    "Type of Network":Network_Type,
    "Winver": winver_output,
    "Antivirus Check": antivirus_info,
    "Last Windows Update Date": last_update_date,
    "License Information": license_info,
    "BIOS PASSWORD CHECK": "BIOS password present: {}".format(bios_password_info),
    "Desktop Folder Check": desktop_folder_count,
    "User Accounts Information": user_information,
    "Shared Folders Data": shared_folders_data,
    "CPU And RAM Utilization": system_utilization,
    "Current Services Status": services_status,
    "USB Logs": usb_logs_output
}

# Generate PDF report
generate_pdf(content)

print("PDF report generated successfully.")