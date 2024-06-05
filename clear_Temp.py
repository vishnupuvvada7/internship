import os

def clear_temp_files():
    temp_dir = os.environ.get('TEMP')
    if temp_dir:
        print("Deleting temporary files...")
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")
        print("Temporary files deleted.")
    else:
        print("TEMP environment variable not found.")

# Call the function to clear temporary files
clear_temp_files()



"""@echo off
echo Deleting temporary files...
del /s /q %temp%\*.*
echo Temporary files deleted.
pause
"""