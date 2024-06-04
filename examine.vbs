Option Explicit

Dim objFSO, objShell, objFolder, objSubfolder, objFile
Dim tempFolderPath, cacheFolderPath, recycleBinPath

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' Get paths
tempFolderPath = objShell.ExpandEnvironmentStrings("%temp%")
cacheFolderPath = objShell.SpecialFolders("Temporary Internet Files")
recycleBinPath = objShell.SpecialFolders("RecycleBin")

' Delete temporary files in %temp% folder
DeleteFilesInFolder tempFolderPath

' Delete cache
DeleteFilesInFolder cacheFolderPath

' Empty recycle bin
EmptyRecycleBin recycleBinPath

' Subroutine to delete files in a folder
Sub DeleteFilesInFolder(folderPath)
    If objFSO.FolderExists(folderPath) Then
        Set objFolder = objFSO.GetFolder(folderPath)
        For Each objFile In objFolder.Files
            objFile.Delete True
        Next
    End If
End Sub

' Subroutine to empty recycle bin
Sub EmptyRecycleBin(recycleBinPath)
    Dim objRecycleBin, objRecycleItem

    Set objRecycleBin = objFSO.GetFolder(recycleBinPath)
    For Each objRecycleItem In objRecycleBin.Files
        objRecycleItem.Delete True
    Next
End Sub