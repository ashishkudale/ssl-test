# Railway Deployment Guide

## Prerequisites
- Railway account (sign up at https://railway.app)
- GitHub repository (optional but recommended)
- Git installed locally

## Deployment Steps

### Method 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Railway deployment"
   git push origin main
   ```

2. **Connect to Railway**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account
   - Select your repository

3. **Configure the deployment**
   - Railway will auto-detect Python and use the Procfile
   - No additional configuration needed

4. **Generate Domain**
   - Go to your project settings
   - Click on "Networking" or "Domains"
   - Click "Generate Domain"
   - Railway will provide a domain like: `your-app.up.railway.app`
   - **Railway automatically provides SSL/TLS certificates via Let's Encrypt**

### Method 2: Deploy via Railway CLI

1. **Install Railway CLI**
   ```bash
   npm i -g @railway/cli
   # or
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and Deploy**
   ```bash
   railway init
   railway up
   ```

4. **Generate Domain**
   ```bash
   railway domain
   ```

## SSL Certificate Information

Railway automatically provisions SSL certificates using **Let's Encrypt** for all custom domains and generated Railway domains. You don't need to manually configure SSL certificates.

### Getting SSL Certificate Information

Once deployed, you can inspect the SSL certificate:

```bash
# Get SSL certificate details
openssl s_client -connect your-app.up.railway.app:443 -showcerts

# Extract certificate to a file for pinning
echo | openssl s_client -connect your-app.up.railway.app:443 2>/dev/null | openssl x509 -outform PEM > certificate.pem

# Get certificate fingerprint (SHA256)
echo | openssl s_client -connect your-app.up.railway.app:443 2>/dev/null | openssl x509 -noout -fingerprint -sha256

# Get public key hash for pinning (recommended for SSL pinning)
echo | openssl s_client -connect your-app.up.railway.app:443 2>/dev/null | openssl x509 -pubkey -noout | openssl pkey -pubin -outform der | openssl dgst -sha256 -binary | openssl enc -base64
```

## Testing the Deployment

### cURL Commands

Replace `your-app.up.railway.app` with your actual Railway domain.

#### 1. Test the /api/test endpoint
```bash
curl -X GET https://your-app.up.railway.app/api/test
```

**Expected Response:**
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

#### 2. Test the /api/user endpoint
```bash
curl -X GET https://your-app.up.railway.app/api/user
```

**Expected Response:**
```json
{
  "id": 1,
  "name": "Test User",
  "email": "test@example.com"
}
```

#### 3. Verbose cURL with SSL information
```bash
curl -v -X GET https://your-app.up.railway.app/api/test
```

This shows SSL handshake details, certificate information, and response.

### Postman Testing

1. **Import to Postman:**
   - Open Postman
   - Click "New" → "HTTP Request"

2. **Test /api/test endpoint:**
   - Method: `GET`
   - URL: `https://your-app.up.railway.app/api/test`
   - Click "Send"

3. **Test /api/user endpoint:**
   - Method: `GET`
   - URL: `https://your-app.up.railway.app/api/user`
   - Click "Send"

4. **View SSL Certificate in Postman:**
   - Click the lock icon next to the URL
   - View certificate details

### Postman Collection (JSON)

Create a new collection with these requests:

```json
{
  "info": {
    "name": "SSL Pinning Test API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Test SSL Pinning",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://your-app.up.railway.app/api/test",
          "protocol": "https",
          "host": ["your-app", "up", "railway", "app"],
          "path": ["api", "test"]
        }
      }
    },
    {
      "name": "Get User",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "https://your-app.up.railway.app/api/user",
          "protocol": "https",
          "host": ["your-app", "up", "railway", "app"],
          "path": ["api", "user"]
        }
      }
    }
  ]
}
```

## SSL Pinning Implementation

### For Android (Kotlin)

```kotlin
val hostname = "your-app.up.railway.app"
val certificatePinner = CertificatePinner.Builder()
    .add(hostname, "sha256/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=") // Replace with actual pin
    .build()

val client = OkHttpClient.Builder()
    .certificatePinner(certificatePinner)
    .build()
```

### For iOS (Swift)

```swift
func urlSession(_ session: URLSession, didReceive challenge: URLAuthenticationChallenge,
                completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void) {
    // Implement SSL pinning logic
}
```

### For React Native

```javascript
// Using react-native-ssl-pinning
import { fetch } from 'react-native-ssl-pinning';

fetch('https://your-app.up.railway.app/api/test', {
  method: 'GET',
  sslPinning: {
    certs: ['certificate'] // certificate.pem in your app bundle
  }
})
```

## Environment Variables (Optional)

If you need to add environment variables:

1. **Via Railway Dashboard:**
   - Go to your project
   - Click "Variables"
   - Add your variables

2. **Via CLI:**
   ```bash
   railway variables set KEY=VALUE
   ```

## Monitoring and Logs

View logs in real-time:
```bash
railway logs
```

Or view in Railway dashboard under "Deployments" → "View Logs"

## Custom Domain (Optional)

To use your own domain:

1. Go to Railway project settings
2. Click "Networking" → "Custom Domain"
3. Add your domain
4. Update DNS records as instructed
5. Railway will automatically provision SSL certificate via Let's Encrypt

## Troubleshooting

### Deployment fails
- Check logs: `railway logs`
- Verify requirements.txt includes all dependencies
- Ensure Procfile is correct

### SSL certificate issues
- Railway auto-provisions certificates; wait a few minutes after deployment
- Verify domain is accessible via HTTPS
- Check certificate using browser or openssl commands

### App not responding
- Verify the app is listening on `0.0.0.0` and Railway's assigned PORT
- Check environment variable: `PORT`

## Health Check Endpoint

The `/api/test` endpoint can be used as a health check for Railway.

---

**Note:** Railway's free tier may have limitations. Check https://railway.app/pricing for details.
