import subprocess
import os
import wmi
import psutil
import check_services
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
    $antivirus = Get-WmiObject -Namespace "root\SecurityCenter2" -Class AntiVirusProduct
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
    



# Main script

# Execute ipconfig /all
ipconfig_output = execute_command("ipconfig /all")



# Execute winver
winver_output = execute_command("ver")

# Perform checks and retrieve information
network_info = extract_network_info(ipconfig_output)
antivirus_info = check_antivirus()
last_update_date = get_last_update_date()
license_info = get_license_info()
bios_password_info = is_bios_password_set()
user_information = get_user_information()
shared_folders_data = run_net_share_command()
system_utilization = get_system_utilization()
desktop_folder_count = get_desktop_folder_count()
services_status = check_services.print_service_status()

# Construct content dictionary
content = {
    "ipconfig /all": network_info,
    "Winver": winver_output,
    "Antivirus Check": antivirus_info,
    "Last Windows Update Date": last_update_date,
    "License Information": license_info,
    "BIOS PASSWORD CHECK": "BIOS password present: {}".format(bios_password_info),
    "Desktop Folder Check": desktop_folder_count,
    "User Accounts Information": user_information,
    "Shared Folders Data": shared_folders_data,
    "CPU And RAM Utilization": system_utilization,
    "Current Services Status": services_status
}

# Generate PDF report
generate_pdf(content)

print("PDF report generated successfully.")