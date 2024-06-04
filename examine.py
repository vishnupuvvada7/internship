import os
import subprocess

def main():
    file_size = os.path.getsize('C:\\Windows\\Temp')
    print("{} kb of data will be removed".format(file_size))
    del_dir = r'c:\\windows\\temp'


    process = subprocess.Popen('rmdir /S /Q {}'.format(del_dir), shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _ = process.communicate()
    return_code = process.returncode
    if return_code == 0:
        print('Success: Cleaned Windows Temp Folder')
    else:
        print('Fail: Unable to Clean Windows Temp Folder')

if __name__ == '__main__':
    main()