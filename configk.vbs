Option Explicit

Dim objShell, objExec, strOutput, arrLines, strIPv4, arrIPv4,strLine

Set objShell = CreateObject("WScript.Shell")
Set objExec = objShell.Exec("ipconfig")

strOutput = objExec.StdOut.ReadAll()

' Split the output into lines
arrLines = Split(strOutput, vbCrLf)

' Loop through each line to find the IPv4 address
For Each strLine In arrLines
    If InStr(strLine, "IPv4 Address") > 0 Then
        ' Extract the IPv4 address
        arrIPv4 = Split(strLine, ":")
        strIPv4 = Trim(arrIPv4(1))
        Exit For ' Exit the loop once IPv4 address is found
    End If
Next

' Check conditions based on IPv4 address
If strIPv4 <> "" Then
    If InStr(strIPv4, "10.69.") = 1 Then
        WScript.Echo "drona"
    ElseIf InStr(strIPv4, "10.86.") = 1 Then
        WScript.Echo "ciag"
    Else
        WScript.Echo "standalone/project"
    End If
Else
    WScript.Echo "IPv4 address not found."
End If

' Clean up
Set objShell = Nothing
Set objExec = Nothing
