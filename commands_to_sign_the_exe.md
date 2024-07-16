## Run these commands in powershell

```powershell
$cert = New-SelfSignedCertificate -Subject "your_exe" -CertStoreLocation "cert:\CurrentUser\My" -HashAlgorithm sha256 -type CodeSigning
```
```powershell
$pwd = ConvertTo-SecureString -String "your_password" -Force -AsPlainText
```
```powershell
Export-PfxCertificate -cert $cert -Filepath your_exe_certificate.pfx -Password $pwd
```

## Run these commands in terminal after running it as administrator

```terminal
signtool.exe sign /f your_exe_certificate.pfx /fd SHA256 /p your_password your_exe.exe
```
```terminal
signtool.exe timestamp -t http://timestamp.digicert.com your_exe.exe
```