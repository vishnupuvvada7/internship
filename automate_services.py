import subprocess
import os


# Disable Telnet Client
def disable_telnet():
    try:
        subprocess.Popen(["powershell.exe", "-Command", "Disable-WindowsOptionalFeature", "-Online", "-FeatureName", "TelnetClient"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
        print("Telnet disabled")
    except Exception as e:
        print("Error occurred while disabling Telnet:", e)

# Enable Windows Firewall
def enable_firewall():
    try:
        firewall_state = subprocess.run(["netsh", "advfirewall", "show", "allprofiles", "state"], capture_output=True, text=True)
        if "State: ON" not in firewall_state.stdout:
            subprocess.Popen(["netsh", "advfirewall", "set", "allprofiles", "state", "on"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Windows Firewall has been enabled.")
        else:
            print("Windows Firewall is already enabled.")
    except Exception as e:
        print("Error occurred while enabling Windows Firewall:", e)

# Disable selected services
def disable_services():
    services = ["bthserv", "lfsvc", "PlugPlay", "HvHost", "RpcLocator", "WFDSConMgrSvc", "RemoteAccess", "XblGameSave", "SessionEnv"]
    for service in services:
        try:
            subprocess.Popen(["sc", "config", service, "start=", "disabled"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            print("Changed startup type to Disabled for service:", service)
        except Exception as e:
            print("Error occurred while changing startup type for service", service, ":", e)

# Set password policies
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
        print("All password policies have been configured successfully!")
    except Exception as e:
        print("Error occurred while setting password policies:", e)

# Main script
def main():
    disable_telnet()
    enable_firewall()
    disable_services()
    set_password_policies()

if __name__ == "__main__":
    main()
