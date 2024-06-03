import subprocess
import os
import tkinter as tk

# Function to disable Telnet Client
def disable_telnet():
    try:
        subprocess.Popen(["powershell.exe", "-Command", "Disable-WindowsOptionalFeature", "-Online", "-FeatureName", "TelnetClient"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        return "Telnet disabled"
    except Exception as e:
        return f"Error occurred while disabling Telnet: {e}"

# Function to enable Windows Firewall
def enable_firewall():
    try:
        firewall_state = subprocess.run(["netsh", "advfirewall", "show", "allprofiles", "state"], capture_output=True, text=True)
        if "State: ON" not in firewall_state.stdout:
            subprocess.Popen(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            return "Windows Firewall has been enabled."
        else:
            return "Windows Firewall is already enabled."
    except Exception as e:
        return f"Error occurred while enabling Windows Firewall: {e}"

# Function to disable selected services
def disable_services():
    services = ["bthserv", "lfsvc", "PlugPlay", "HvHost", "RpcLocator", "WFDSConMgrSvc", "RemoteAccess", "XblGameSave", "SessionEnv"]
    status = ""
    for service in services:
        try:
            subprocess.Popen(["sc", "config", service, "start=", "disabled"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            status += f"Changed startup type to Disabled for service: {service}\n"
        except Exception as e:
            status += f"Error occurred while changing startup type for service {service}: {e}\n"
    return status

# Function to set password policies
def set_password_policies():
    try:
        # Set password complexity policy
        subprocess.Popen(["secedit", "/configure", "/db", os.path.join(os.environ['windir'], 'security', 'new.sdb'), "/cfg", os.path.join(os.environ['windir'], 'security', 'templates', 'setup security.inf'), "/areas", "SECURITYPOLICY", "/log", os.path.join(os.environ['windir'], 'security', 'logs', 'secpol.log'), "/overwrite", "/quiet", "/p", "PasswordComplexity=1"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        # Set other password policies
        subprocess.Popen(["secedit", "/configure", "/db", os.path.join(os.environ['windir'], 'security', 'new.sdb'), "/cfg", os.path.join(os.environ['windir'], 'security', 'templates', 'setup security.inf'), "/areas", "SECURITYPOLICY", "/log", os.path.join(os.environ['windir'], 'security', 'logs', 'secpol.log'), "/overwrite", "/quiet"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["net", "accounts", "/uniquepw:3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["net", "accounts", "/maxpwage:45"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["net", "accounts", "/minpwage:0"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["net", "accounts", "/minpwlen:10"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["net", "accounts", "/lockoutthreshold:5"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        subprocess.Popen(["net", "accounts", "/lockoutduration:30"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        return "All password policies have been configured successfully!"
    except Exception as e:
        return f"Error occurred while setting password policies: {e}"

# Main script
def main():
    # Call functions to perform actions and collect their status
    telnet_status = disable_telnet()
    firewall_status = enable_firewall()
    services_status = disable_services()
    password_policies_status = set_password_policies()

    # Return all status information as a single string
    return f"{telnet_status}\n{firewall_status}\n{services_status}\n{password_policies_status}"

# If this script is run directly
if __name__ == "__main__":
    # Run the main function and collect the status information
    status_info = main()
    # Print the status information
    print(status_info)
