# Quick Test Commands - test-ssl-pinning.up.railway.app

## 🧪 cURL Commands (Ready to Copy & Paste)

### Test /api/test endpoint
```bash
curl -X GET https://test-ssl-pinning.up.railway.app/api/test
```

### Test /api/user endpoint
```bash
curl -X GET https://test-ssl-pinning.up.railway.app/api/user
```

### Health check endpoint
```bash
curl -X GET https://test-ssl-pinning.up.railway.app/health
```

### POST /api/login endpoint (Login with credentials)
```bash
# Login with admin user
curl -X POST https://test-ssl-pinning.up.railway.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Login with john user
curl -X POST https://test-ssl-pinning.up.railway.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"john123"}'

# Login with sarah user
curl -X POST https://test-ssl-pinning.up.railway.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"sarah","password":"sarah123"}'

# Login with demo user
curl -X POST https://test-ssl-pinning.up.railway.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"demo123"}'

# Test invalid credentials
curl -X POST https://test-ssl-pinning.up.railway.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"invalid","password":"wrong"}'
```

### Verbose output with SSL details
```bash
curl -v -X GET https://test-ssl-pinning.up.railway.app/api/test
```

### Pretty print JSON (with jq)
```bash
curl -X GET https://test-ssl-pinning.up.railway.app/api/test | jq
curl -X GET https://test-ssl-pinning.up.railway.app/api/user | jq
curl -X POST https://test-ssl-pinning.up.railway.app/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' | jq
```

---

## 🔐 SSL Certificate Extraction Commands

### Get public key hash (Base64) - For SSL Pinning
```bash
echo | openssl s_client -connect test-ssl-pinning.up.railway.app:443 2>/dev/null | \
  openssl x509 -pubkey -noout | \
  openssl pkey -pubin -outform der | \
  openssl dgst -sha256 -binary | \
  openssl enc -base64
```

### Get certificate fingerprint (SHA256)
```bash
echo | openssl s_client -connect test-ssl-pinning.up.railway.app:443 2>/dev/null | \
  openssl x509 -noout -fingerprint -sha256
```

### Save certificate to file (PEM format)
```bash
echo | openssl s_client -connect test-ssl-pinning.up.railway.app:443 2>/dev/null | \
  openssl x509 -outform PEM > certificate.pem
```

### View full certificate details
```bash
echo | openssl s_client -connect test-ssl-pinning.up.railway.app:443 2>/dev/null | \
  openssl x509 -text -noout
```

### Get all certificates in chain
```bash
openssl s_client -connect test-ssl-pinning.up.railway.app:443 -showcerts
```

### Extract issuer and subject
```bash
echo | openssl s_client -connect test-ssl-pinning.up.railway.app:443 2>/dev/null | \
  openssl x509 -noout -subject -issuer
```

---

## 📮 Postman Requests

### Request 1: Test SSL Pinning
- **Method:** GET
- **URL:** `https://test-ssl-pinning.up.railway.app/api/test`
- **Expected Response:**
```json
{
  "status": "success",
  "message": "SSL Pinning is working!",
  "data": {
    "timestamp": "2024-01-01",
    "server": "Python Flask"
  }
}
```

### Request 2: Get User
- **Method:** GET
- **URL:** `https://test-ssl-pinning.up.railway.app/api/user`
- **Expected Response:**
```json
{
  "id": 1,
  "name": "Test User",
  "email": "test@example.com"
}
```

### Request 3: Health Check
- **Method:** GET
- **URL:** `https://test-ssl-pinning.up.railway.app/health`
- **Expected Response:**
```json
{
  "status": "healthy",
  "service": "ssl-pinning-test"
}
```

### Request 4: Login (POST)
- **Method:** POST
- **URL:** `https://test-ssl-pinning.up.railway.app/api/login`
- **Headers:**
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "username": "admin",
  "password": "admin123"
}
```
- **Expected Response (Success):**
```json
{
  "status": "success",
  "message": "Login successful",
  "token": "mock_token_admin_12345",
  "user": {
    "id": 1,
    "username": "admin",
    "name": "Admin User",
    "email": "admin@example.com",
    "age": 30,
    "userType": "administrator",
    "role": "admin",
    "department": "IT",
    "joinDate": "2020-01-15",
    "isActive": true
  }
}
```

**Test Credentials:**
- Username: `admin` | Password: `admin123` (Administrator)
- Username: `john` | Password: `john123` (Regular Developer)
- Username: `sarah` | Password: `sarah123` (Premium Manager)
- Username: `demo` | Password: `demo123` (Trial User)

**Expected Response (Failed):**
```json
{
  "status": "error",
  "message": "Invalid username or password"
}
```

---

## 📱 SSL Pinning Implementation Examples

### Android (OkHttp + Kotlin)
```kotlin
import okhttp3.CertificatePinner
import okhttp3.OkHttpClient

// First, run the command above to get the public key hash
// Then replace "YOUR_PUBLIC_KEY_HASH" below

val hostname = "test-ssl-pinning.up.railway.app"
val certificatePinner = CertificatePinner.Builder()
    .add(hostname, "sha256/YOUR_PUBLIC_KEY_HASH")
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()

// Make request
val request = Request.Builder()
    .url("https://test-ssl-pinning.up.railway.app/api/test")
    .build()

client.newCall(request).execute().use { response ->
    println(response.body?.string())
}
```

### iOS (Swift)
```swift
import Foundation

class SSLPinningManager: NSObject, URLSessionDelegate {

    func urlSession(_ session: URLSession,
                   didReceive challenge: URLAuthenticationChallenge,
                   completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {

        guard let serverTrust = challenge.protectionSpace.serverTrust,
              let certificate = SecTrustGetCertificateAtIndex(serverTrust, 0) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Get the public key hash and compare
        let serverPublicKey = SecCertificateCopyKey(certificate)
        // Implement pinning logic here

        completionHandler(.useCredential, URLCredential(trust: serverTrust))
    }
}

// Usage
let config = URLSessionConfiguration.default
let session = URLSession(configuration: config, delegate: SSLPinningManager(), delegateQueue: nil)

let url = URL(string: "https://test-ssl-pinning.up.railway.app/api/test")!
let task = session.dataTask(with: url) { data, response, error in
    if let data = data {
        print(String(data: data, encoding: .utf8) ?? "")
    }
}
task.resume()
```

### React Native (react-native-ssl-pinning)
```javascript
import { fetch } from 'react-native-ssl-pinning';

// Place certificate.pem in your app bundle
fetch('https://test-ssl-pinning.up.railway.app/api/test', {
  method: 'GET',
  sslPinning: {
    certs: ['certificate'] // certificate.pem without extension
  }
})
  .then(response => response.json())
  .then(json => console.log(json))
  .catch(error => console.error(error));
```

### Flutter (http_certificate_pinning)
```dart
import 'package:http_certificate_pinning/http_certificate_pinning.dart';

// Get SHA-256 fingerprint from the command above
List<String> fingerprints = [
  "SHA-256 FINGERPRINT HERE"
];

try {
  final response = await HttpCertificatePinning.check(
    serverURL: "https://test-ssl-pinning.up.railway.app/api/test",
    headerHttp: {},
    sha: SHA.SHA256,
    allowedSHAFingerprints: fingerprints,
    timeout: 60
  );

  print(response.body);
} catch (e) {
  print("Certificate pinning failed: $e");
}
```

---

## 🔍 Testing SSL Certificate

### Test in Browser
1. Open: https://test-ssl-pinning.up.railway.app/api/test
2. Click the 🔒 lock icon in address bar
3. View certificate details

### Test with SSL Labs
Check SSL configuration quality:
```
https://www.ssllabs.com/ssltest/analyze.html?d=test-ssl-pinning.up.railway.app
```

### Test certificate expiry
```bash
echo | openssl s_client -connect test-ssl-pinning.up.railway.app:443 2>/dev/null | \
  openssl x509 -noout -dates
```

---

## 📋 Quick Copy-Paste for Postman

**Import this cURL command in Postman (File → Import → Raw text):**

```bash
curl -X GET https://test-ssl-pinning.up.railway.app/api/test
curl -X GET https://test-ssl-pinning.up.railway.app/api/user
curl -X GET https://test-ssl-pinning.up.railway.app/health
```

Or create a new request:
1. Click **New** → **HTTP Request**
2. Set method to **GET**
3. Enter URL: `https://test-ssl-pinning.up.railway.app/api/test`
4. Click **Send**
5. Click the 🔒 icon to view SSL certificate

---

## ✅ Expected Results

All endpoints should return:
- **Status Code:** 200 OK
- **Content-Type:** application/json
- **SSL/TLS:** ✅ Valid Let's Encrypt certificate
- **HTTPS:** ✅ Enabled

Happy Testing! 🚀
