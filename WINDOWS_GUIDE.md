# Windows Quick Test Commands - test-ssl-pinning.up.railway.app

## 🧪 PowerShell/CMD cURL Commands (Windows)

### Test endpoints using curl (available in Windows 10+)
```powershell
# Test /api/test endpoint
curl https://test-ssl-pinning.up.railway.app/api/test

# Test /api/user endpoint
curl https://test-ssl-pinning.up.railway.app/api/user

# Health check
curl https://test-ssl-pinning.up.railway.app/health
```

### Using PowerShell Invoke-WebRequest
```powershell
# Test /api/test endpoint
Invoke-WebRequest -Uri "https://test-ssl-pinning.up.railway.app/api/test" | Select-Object -ExpandProperty Content

# Test /api/user endpoint
Invoke-WebRequest -Uri "https://test-ssl-pinning.up.railway.app/api/user" | Select-Object -ExpandProperty Content

# Get full response details
$response = Invoke-WebRequest -Uri "https://test-ssl-pinning.up.railway.app/api/test"
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 🔐 METHOD 1: Get SSL Certificate via Browser (EASIEST!)

### Using Chrome/Edge:
1. Open: **https://test-ssl-pinning.up.railway.app/api/test**
2. Click the 🔒 **lock icon** in the address bar
3. Click **"Connection is secure"**
4. Click **"Certificate is valid"**
5. In the certificate window:
   - Go to **"Details"** tab
   - Click **"Copy to File"** button
   - Choose **"Base-64 encoded X.509 (.CER)"**
   - Save as `certificate.cer` or `certificate.pem`

### Using Firefox:
1. Open: **https://test-ssl-pinning.up.railway.app/api/test**
2. Click the 🔒 **lock icon**
3. Click **"Connection secure"** → **"More information"**
4. Click **"View Certificate"**
5. Scroll down and click **"Download"** → **"PEM (cert)"**
6. Save as `certificate.pem`

---

## 🔐 METHOD 2: PowerShell Script to Get Certificate

### Save this as `get-certificate.ps1`:
```powershell
# Get SSL certificate for test-ssl-pinning.up.railway.app
$hostname = "test-ssl-pinning.up.railway.app"
$port = 443

# Create TCP connection
$tcpClient = New-Object System.Net.Sockets.TcpClient($hostname, $port)
$sslStream = New-Object System.Net.Security.SslStream($tcpClient.GetStream(), $false)

# Authenticate
$sslStream.AuthenticateAsClient($hostname)

# Get certificate
$cert = $sslStream.RemoteCertificate

# Convert to X509Certificate2
$cert2 = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($cert)

# Display certificate information
Write-Host "`n=== Certificate Information ===" -ForegroundColor Green
Write-Host "Subject: $($cert2.Subject)"
Write-Host "Issuer: $($cert2.Issuer)"
Write-Host "Valid From: $($cert2.NotBefore)"
Write-Host "Valid Until: $($cert2.NotAfter)"
Write-Host "Thumbprint (SHA1): $($cert2.Thumbprint)"
Write-Host "Serial Number: $($cert2.SerialNumber)"

# Get SHA-256 thumbprint
$sha256 = [System.Security.Cryptography.SHA256]::Create()
$hash = $sha256.ComputeHash($cert2.RawData)
$sha256Thumbprint = [System.BitConverter]::ToString($hash).Replace("-", "")
Write-Host "Thumbprint (SHA256): $sha256Thumbprint" -ForegroundColor Yellow

# Get Public Key Hash (for SSL Pinning)
$publicKey = $cert2.PublicKey.EncodedKeyValue.RawData
$publicKeyHash = $sha256.ComputeHash($publicKey)
$publicKeyHashBase64 = [System.Convert]::ToBase64String($publicKeyHash)
Write-Host "`n=== Public Key Hash (for SSL Pinning) ===" -ForegroundColor Cyan
Write-Host "sha256/$publicKeyHashBase64" -ForegroundColor Yellow

# Export certificate to file
$certPath = "certificate.cer"
$certBytes = $cert2.Export([System.Security.Cryptography.X509Certificates.X509ContentType]::Cert)
[System.IO.File]::WriteAllBytes($certPath, $certBytes)
Write-Host "`nCertificate saved to: $certPath" -ForegroundColor Green

# Export to PEM format
$pemPath = "certificate.pem"
$pemContent = @"
-----BEGIN CERTIFICATE-----
$([System.Convert]::ToBase64String($certBytes, [System.Base64FormattingOptions]::InsertLineBreaks))
-----END CERTIFICATE-----
"@
$pemContent | Out-File -FilePath $pemPath -Encoding ASCII
Write-Host "Certificate (PEM) saved to: $pemPath" -ForegroundColor Green

# Cleanup
$sslStream.Close()
$tcpClient.Close()

Write-Host "`nDone!`n" -ForegroundColor Green
```

### Run the script:
```powershell
# Run in PowerShell
powershell -ExecutionPolicy Bypass -File get-certificate.ps1
```

---

## 🔐 METHOD 3: Python Script (Cross-platform)

### Save this as `get_certificate.py`:
```python
import ssl
import socket
import hashlib
import base64
from datetime import datetime

hostname = "test-ssl-pinning.up.railway.app"
port = 443

# Get certificate
context = ssl.create_default_context()
with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        # Get certificate in DER format
        cert_der = ssock.getpeercert(binary_form=True)

        # Get certificate in dict format
        cert_dict = ssock.getpeercert()

        print("\n=== Certificate Information ===")
        print(f"Subject: {dict(x[0] for x in cert_dict['subject'])}")
        print(f"Issuer: {dict(x[0] for x in cert_dict['issuer'])}")
        print(f"Valid From: {cert_dict['notBefore']}")
        print(f"Valid Until: {cert_dict['notAfter']}")

        # Calculate SHA-256 fingerprint
        sha256_fingerprint = hashlib.sha256(cert_der).hexdigest()
        print(f"\nSHA-256 Fingerprint: {sha256_fingerprint.upper()}")

        # Get public key hash for SSL pinning
        import cryptography.x509
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives import serialization

        cert_obj = cryptography.x509.load_der_x509_certificate(cert_der, default_backend())
        public_key = cert_obj.public_key()
        public_key_der = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Calculate public key hash
        public_key_hash = hashlib.sha256(public_key_der).digest()
        public_key_hash_base64 = base64.b64encode(public_key_hash).decode('utf-8')

        print(f"\n=== Public Key Hash (for SSL Pinning) ===")
        print(f"sha256/{public_key_hash_base64}")

        # Save certificate to file
        with open("certificate.der", "wb") as f:
            f.write(cert_der)
        print("\nCertificate saved to: certificate.der")

        # Save as PEM
        pem_cert = ssl.DER_cert_to_PEM_cert(cert_der)
        with open("certificate.pem", "w") as f:
            f.write(pem_cert)
        print("Certificate (PEM) saved to: certificate.pem")

        print("\nDone!\n")
```

### Install dependencies and run:
```bash
pip install cryptography
python get_certificate.py
```

---

## 🔐 METHOD 4: Install OpenSSL on Windows

### Option A: Using Chocolatey
```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install OpenSSL
choco install openssl -y

# Restart terminal, then run:
openssl version
```

### Option B: Manual Download
1. Download from: **https://slproweb.com/products/Win32OpenSSL.html**
2. Install "Win64 OpenSSL v3.x.x Light"
3. Add to PATH: `C:\Program Files\OpenSSL-Win64\bin`
4. Restart CMD/PowerShell

### Then use OpenSSL commands:
```bash
# Get public key hash
openssl s_client -connect test-ssl-pinning.up.railway.app:443 -showcerts < NUL 2>&1 | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64

# Save certificate
openssl s_client -connect test-ssl-pinning.up.railway.app:443 -showcerts < NUL 2>&1 | openssl x509 -outform PEM > certificate.pem

# Get SHA-256 fingerprint
openssl s_client -connect test-ssl-pinning.up.railway.app:443 < NUL 2>&1 | openssl x509 -noout -fingerprint -sha256
```

---

## 🌐 METHOD 5: Online Tools (Quick but less secure)

### SSL Labs
- Check certificate: **https://www.ssllabs.com/ssltest/analyze.html?d=test-ssl-pinning.up.railway.app**
- View detailed SSL/TLS configuration
- Get certificate chain

### Certificate Decoder
- Go to: **https://www.sslshopper.com/ssl-certificate-decoder.html**
- Paste your certificate
- View all details

### What's My Chain Cert?
- Go to: **https://whatsmychaincert.com/**
- Enter: `test-ssl-pinning.up.railway.app`
- Download certificate chain

---

## 📮 Postman (EASIEST for API Testing!)

### Create Requests:
1. **New Request** → Method: `GET`
2. **URLs to test:**
   ```
   https://test-ssl-pinning.up.railway.app/api/test
   https://test-ssl-pinning.up.railway.app/api/user
   https://test-ssl-pinning.up.railway.app/health
   ```
3. Click **Send**

### View Certificate in Postman:
1. Click the 🔒 **lock icon** next to URL
2. View certificate details
3. See issuer, expiry, fingerprint

### Export Certificate from Postman:
1. Go to **Settings** → **Certificates**
2. Add your domain
3. View certificate details

---

## ✅ Quick Test in Browser

Just open these URLs in your browser:

1. **https://test-ssl-pinning.up.railway.app/api/test**
2. **https://test-ssl-pinning.up.railway.app/api/user**
3. **https://test-ssl-pinning.up.railway.app/health**

You should see JSON responses immediately! ✅

---

## 📱 For Mobile App Development

Once you have the certificate file (`certificate.pem`), use it in your mobile app:

### Android (OkHttp)
1. Place `certificate.pem` in `res/raw/` folder
2. Use CertificatePinner with the public key hash

### iOS (Swift)
1. Add `certificate.cer` to your Xcode project
2. Implement SSL pinning in URLSession delegate

### React Native
1. Place certificate in app bundle
2. Use `react-native-ssl-pinning` library

---

## 🎯 Recommended Approach for Windows Users

**For Quick Testing:**
→ Use **Postman** (easiest, no command line needed)

**For Getting Certificate:**
→ Use **Browser method** (Chrome/Edge) - just a few clicks!

**For SSL Pinning Hash:**
→ Run the **PowerShell script** above (copy-paste and run)

---

## 💡 Need Help?

If you encounter issues:
1. Make sure you have internet connection
2. Try opening the URL in browser first
3. Use Postman for the easiest experience
4. The PowerShell script should work on any Windows 10/11 machine

Happy Testing! 🚀
