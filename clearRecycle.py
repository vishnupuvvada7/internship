import ctypes

def recycle():
    try:
        SHEmptyRecycleBin = ctypes.windll.shell32.SHEmptyRecycleBinW  
        SHEmptyRecycleBin.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_int]  
        SHEmptyRecycleBin.restype = ctypes.c_int  
    
        result = SHEmptyRecycleBin(None, None, 0x01)  
        if result == 0:  
            print("Successful emptying of the recycle bin.. ")  
        else:  
            print("Already empty")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    recycle()
