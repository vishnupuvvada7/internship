import os

def search_files(root_dir, file_types):
    file_paths_by_type = {file_type: [] for file_type in file_types}  # Dictionary to store file paths by type
    file_types_lower = {file_type.lower() for file_type in file_types}  # Set of lowercase file types
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            file_type = os.path.splitext(filename)[1].lower()  # Get file extension and convert to lowercase
            if file_type in file_types_lower:
                filepath = os.path.join(dirpath, filename)
                file_paths_by_type[file_type].append(filepath)
    return file_paths_by_type

# Update file types as needed (remove ".exe" if a security risk)
file_types = {".mp3", ".mp4", ".pptx", ".pdf", ".apk",".gif"}

# Start search from the root directory of the system
root_path = "/"  # For Unix-like systems
# root_path = "C:\\"  # For Windows systems

file_paths_by_type = search_files(root_path, file_types)

# Save all file paths to a single text file, sorted by file type
output_filename = "all_files.txt"
with open(output_filename, "w") as f:  # Open in write mode
    for file_type in sorted(file_paths_by_type.keys()):  # Sort file types
        f.write(f"Files of type {file_type}:\n")
        for filepath in sorted(file_paths_by_type[file_type]):  # Sort file paths within each type
            f.write(filepath + "\n")  # Write filepath with newline
        f.write("\n")  # Add a newline after each type
    print(f"Saved files to {output_filename}")
