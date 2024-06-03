import tkinter as tk
from tkinter import PhotoImage
import os
import sys
import subprocess


def get_executable_directory():
    """Get the directory where the executable is located."""
    if getattr(sys, 'frozen', False):
        # If the script is running as a bundled executable
        return os.path.dirname(sys.executable)
    else:
        # If the script is running as a Python script
        return os.path.dirname(os.path.realpath(__file__))


def run_audit():
    try:
        executable_dir = get_executable_directory()
        py_script_path = os.path.join(executable_dir, "retrieval.py")
        result = subprocess.check_output(["python", py_script_path], shell=True)

        # Update the result_text widget with the output
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result.decode("utf-8"))
        result_text.config(state=tk.DISABLED)
    except Exception as e:
        # If an exception occurs, display the error message
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {e}")
        result_text.config(state=tk.DISABLED)


def open_result_file():
    try:
        executable_dir = get_executable_directory()
        file_path = os.path.join(executable_dir, "system_info.pdf")
        if os.path.exists(file_path):
            os.startfile(file_path)
        else:
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, "File not found!")
            result_text.config(state=tk.DISABLED)
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {e}")
        result_text.config(state=tk.DISABLED)


def disable_services():
    try:
        executable_dir = get_executable_directory()
        bat_file_path = os.path.join(executable_dir, "services.bat")
        subprocess.run([bat_file_path], shell=True)
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Services enabled/disabled successfully.")
        result_text.config(state=tk.DISABLED)
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {e}")
        result_text.config(state=tk.DISABLED)


def logs_generation():
    try:
        executable_dir = get_executable_directory()
        batch_file_path = os.path.join(executable_dir, "logs_generation.bat")
        subprocess.run([batch_file_path], shell=True)
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Logs Generated successfully")
        result_text.config(state=tk.DISABLED)
    except Exception as e:
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Error: {e}")
        result_text.config(state=tk.DISABLED)


about_frame_visible = False
about_frame = None


def open_about_window():
    global about_frame_visible, about_frame

    if not about_frame_visible:
        headers = ["General Audit", "Logs", "Services"]
        general_audit_data = {
            "IP Configuration": "Ip address",
            "Mac address": "Mac Address",
            "Windows version": "Windows version",
            "Users Information": "No of users",
            "Antivirus Details": "Antivirus Check",
            "Last updated": "Last Updated Date",
            "OS last updated": "Last OS updated date",
            "Licensed OS": "License Details of OS",
            "Clean Desktop": "Desktop Clean/Not",
            "Last Updated": "Last Updated Details",
            "BIOS Password Check": "BIOS Password Check",
            "Shared Folders": "Shared Folders details"
        }
        logs_data = {
            "Windows Logs": "Windows Logs",
            "USB Logs": "USB Logs",
            "Personal files": "Personal media files"
        }
        services_data = {
            "Bluetooth": "Bluetooth Service Status",
            "Geo Location": "Location Service Status",
            "Xbox": "Xbox Services Status",
            "Plug and Play": "Plug and Play Status",
            "Wi-fi": "Wi-fi Status",
            "password policy": "Passowrd Policy",
            "Audit logon policy": "Audit Logon policy",
            "Remote Disabled": "RDP remote disabled",
            "Telnet Service": "Telnet Service status"
        }

        # Clear existing about frame if it exists
        if about_frame:
            about_frame.destroy()

        # Create new about frame
        about_frame = tk.Frame(root, bg=bg_color)
        about_frame.pack(pady=20)

        # Create header labels
        for col, header in enumerate(headers):
            label = tk.Label(about_frame, text=header, bg="lightgray", fg="black", font=("Arial", 10, "bold"),
                             borderwidth=1, relief="solid", width=20)
            label.grid(row=0, column=col, padx=1, pady=1)

        max_rows = max(len(general_audit_data), len(logs_data), len(services_data))

        for row in range(1, max_rows + 1):
            general_audit_label = tk.Label(about_frame, text=list(general_audit_data.values())[row - 1] if row <= len(
                general_audit_data) else "", bg="white", fg="black", font=("Arial", 10), borderwidth=1, relief="solid",
                                           width=20)
            general_audit_label.grid(row=row, column=0, padx=1, pady=1)

            logs_label = tk.Label(about_frame, text=list(logs_data.values())[row - 1] if row <= len(logs_data) else "",
                                  bg="white", fg="black", font=("Arial", 10), borderwidth=1, relief="solid", width=20)
            logs_label.grid(row=row, column=1, padx=1, pady=1)

            services_label = tk.Label(about_frame,
                                      text=list(services_data.values())[row - 1] if row <= len(services_data) else "",
                                      bg="white", fg="black", font=("Arial", 10), borderwidth=1, relief="solid",
                                      width=20)
            services_label.grid(row=row, column=2, padx=1, pady=1)

        about_frame_visible = True
    else:
        # Hide the about frame
        about_frame.destroy()
        about_frame_visible = False


# Create main window
root = tk.Tk()
root.title("CAS AUDIT TOOL")

# Define custom colors
bg_color = "#283046"
button_bg_color = "#404e5c"

# Set background color for the root window
root.config(bg=bg_color)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg=bg_color)
button_frame.pack(pady=20)

# Create buttons
audit_button = tk.Button(button_frame, text="Run Audit", command=run_audit, bg=button_bg_color, fg="white", padx=10,
                         pady=5)
audit_button.grid(row=0, column=0, padx=10)

result_button = tk.Button(button_frame, text="Open Result File", command=open_result_file, bg=button_bg_color,
                          fg="white", padx=10, pady=5)
result_button.grid(row=0, column=1, padx=10)

disable_button = tk.Button(button_frame, text="Disable Services", command=disable_services, bg=button_bg_color,
                           fg="white", padx=10, pady=5)
disable_button.grid(row=0, column=2, padx=10)

logs_button = tk.Button(button_frame, text="Generate Logs", command=logs_generation, bg=button_bg_color, fg="white",
                        padx=10, pady=5)
logs_button.grid(row=0, column=4, padx=10)

about_button = tk.Button(button_frame, text="About", command=open_about_window, bg=button_bg_color, fg="white", padx=10,
                         pady=5)
about_button.grid(row=0, column=5, padx=10)

# Create a frame for the result text
result_frame = tk.Frame(root, bg=bg_color)
result_frame.pack(pady=20)

# Create a text box for displaying results
result_text = tk.Text(result_frame, height=5, width=80, bg=button_bg_color, fg="white")
result_text.pack(padx=20, pady=20)

# Create a frame for the about information
about_frame = tk.Frame(root, bg=bg_color)
about_frame.pack(pady=20)

# Disable text box by default
result_text.config(state=tk.DISABLED)

root.mainloop()
