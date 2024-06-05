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
