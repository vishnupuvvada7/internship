import os, subprocess
del_dir = r'c:\windows\temp'
pObj = subprocess.Popen('del /S /Q /F %s\\*.*' % del_dir, shell=True, stdout = subprocess.PIPE, stderr= subprocess.PIPE)
rTup = pObj.communicate()
rCod = pObj.returncode
if rCod == 0:
    print ('Success: Cleaned Windows Temp Folder')
else:
    print ('Fail: Unable to Clean Windows Temp Folder')