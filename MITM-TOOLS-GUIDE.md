# 🔍 MITM Tools Guide for Modern Systems

## Table of Contents
- [What is MITM?](#what-is-mitm)
- [Legal & Ethical Disclaimer](#legal--ethical-disclaimer)
- [Popular MITM Tools](#popular-mitm-tools)
- [Tool Comparison](#tool-comparison)
- [Setup Guides](#setup-guides)
- [Common Use Cases](#common-use-cases)
- [Bypassing Modern Security](#bypassing-modern-security)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

---

## What is MITM?

**Man-In-The-Middle (MITM)** attacks involve intercepting communications between two parties without their knowledge. In security testing, MITM tools allow you to:

- 🔍 **Analyze network traffic** - See what data applications are sending
- 🛡️ **Test encryption** - Verify SSL/TLS implementations
- 🐛 **Debug APIs** - Understand client-server communications
- 🔐 **Find vulnerabilities** - Discover security flaws in protocols
- 📱 **Test mobile apps** - Intercept app traffic for security analysis

### Why MITM Tools Matter for Modern Systems

Modern applications use:
- **HTTPS everywhere** - Encrypted traffic is the default
- **Certificate pinning** - Apps verify specific certificates
- **API security** - Token-based authentication needs testing
- **Mobile-first** - iOS/Android apps need special handling
- **Microservices** - Complex service-to-service communications

Traditional packet sniffers (like basic Wireshark) can't decrypt modern HTTPS traffic. **MITM tools bridge this gap** by acting as a trusted proxy.

---

## Legal & Ethical Disclaimer

⚠️ **CRITICAL: READ THIS FIRST**

MITM attacks can be **ILLEGAL** if performed without proper authorization.

### ✅ LEGAL USES:
- Testing your own applications and devices
- Authorized penetration testing with written permission
- Security research in controlled environments
- Educational purposes on isolated lab networks
- CTF competitions and bug bounty programs
- Corporate security assessments with approval

### ❌ ILLEGAL USES:
- Intercepting traffic on public networks without permission
- Spying on other people's communications
- Stealing credentials or sensitive data
- Unauthorized access to systems or networks
- Any activity without explicit written consent

**Always get written authorization before testing any system you don't own.**

---

## Popular MITM Tools

### 1. 🎯 **mitmproxy** (Recommended for Beginners)

**Best for:** HTTP/HTTPS traffic analysis, scripting, automation

**What it is:** A free, open-source interactive HTTPS proxy with a powerful Python API.

**Key Features:**
- ✨ Clean command-line and web interface
- 🐍 Python scripting for custom modifications
- 📝 Automatic SSL/TLS interception
- 🔄 Request/response modification in real-time
- 💾 Traffic capture and replay

**Platforms:** Linux, macOS, Windows

**Website:** https://mitmproxy.org/

---

### 2. 🔥 **Burp Suite** (Industry Standard)

**Best for:** Web application security testing, professional pentesting

**What it is:** The most popular web security testing toolkit used by professionals worldwide.

**Key Features:**
- 🕷️ Web application scanner (Pro version)
- 🔍 Powerful intercepting proxy
- 🛠️ Extensive extensions marketplace
- 🎨 Intuitive GUI with multiple tools
- 🔄 Repeater, Intruder, Sequencer tools

**Platforms:** Linux, macOS, Windows (Java-based)

**Versions:**
- **Community Edition** - Free, basic features
- **Professional** - $449/year, includes scanner
- **Enterprise** - For large organizations

**Website:** https://portswigger.net/burp

---

### 3. 🦈 **Wireshark** (Network Protocol Analyzer)

**Best for:** Deep packet inspection, network troubleshooting

**What it is:** The world's most widely-used network protocol analyzer.

**Key Features:**
- 📊 Capture and analyze 1000+ protocols
- 🔍 Deep inspection of hundreds of protocols
- 📈 Live capture and offline analysis
- 🎨 Rich VoIP analysis
- 🔓 Decryption with SSL keys

**Platforms:** Linux, macOS, Windows, BSD

**Website:** https://www.wireshark.org/

---

### 4. 🌐 **OWASP ZAP** (Zed Attack Proxy)

**Best for:** Automated security testing, CI/CD integration

**What it is:** Free, open-source web application security scanner.

**Key Features:**
- 🤖 Automated scanners
- 🔍 Intercepting proxy
- 🚀 API for automation
- 🆓 Completely free
- 👥 Active community

**Platforms:** Linux, macOS, Windows (Java-based)

**Website:** https://www.zaproxy.org/

---

### 5. 🦊 **Fiddler** (Windows/Web Debugging)

**Best for:** Windows environments, .NET applications

**What it is:** Web debugging proxy popular in Windows development.

**Key Features:**
- 🪟 Native Windows application
- 🎨 User-friendly GUI
- 🔧 Performance testing
- 📱 Mobile device support
- 💼 Enterprise features

**Platforms:** Windows (primary), macOS, Linux (Fiddler Everywhere)

**Website:** https://www.telerik.com/fiddler

---

### 6. 🐝 **Bettercap**

**Best for:** Network attacks, WiFi security testing

**What it is:** Swiss Army knife for WiFi, Bluetooth, and network attacks.

**Key Features:**
- 📡 WiFi networks monitoring and attacks
- 🔵 Bluetooth Low Energy monitoring
- 🌐 HTTP/HTTPS proxy
- 🎭 Spoofing and credential harvesting
- 🖥️ Web UI for monitoring

**Platforms:** Linux, macOS, Windows

**Website:** https://www.bettercap.org/

---

### 7. 📱 **Charles Proxy**

**Best for:** Mobile app testing, macOS users

**What it is:** HTTP proxy/monitor for viewing network traffic.

**Key Features:**
- 📱 Excellent mobile device support
- 🎨 Beautiful macOS-native interface
- 🔄 Request/response modification
- ⚡ Bandwidth throttling
- 🔁 Session replay

**Platforms:** macOS, Windows, Linux

**Cost:** $50 (30-day trial available)

**Website:** https://www.charlesproxy.com/

---

## Tool Comparison

| Tool | Difficulty | Best For | Price | SSL Interception | Scripting |
|------|-----------|----------|-------|------------------|-----------|
| **mitmproxy** | Beginner-Medium | API testing, automation | Free | ✅ Excellent | Python API |
| **Burp Suite** | Medium | Web app testing | Free/Paid | ✅ Excellent | Extensions (Java) |
| **Wireshark** | Advanced | Protocol analysis | Free | ⚠️ Manual | Lua |
| **OWASP ZAP** | Beginner-Medium | Automated scanning | Free | ✅ Good | Scripts/API |
| **Fiddler** | Beginner | Windows/.NET apps | Free | ✅ Good | .NET/JavaScript |
| **Bettercap** | Advanced | WiFi/Network attacks | Free | ✅ Good | JavaScript |
| **Charles** | Beginner | Mobile apps, macOS | $50 | ✅ Excellent | Limited |

---

## Setup Guides

### 🎯 Setting Up mitmproxy (Linux/macOS)

#### Step 1: Installation

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install mitmproxy

# macOS (Homebrew)
brew install mitmproxy

# Python pip (any platform)
pip install mitmproxy
```

#### Step 2: Start the Proxy

```bash
# Command-line interface
mitmproxy

# Web interface (recommended for beginners)
mitmweb

# Dump traffic to console
mitmdump
```

**Default proxy address:** `localhost:8080`

#### Step 3: Install CA Certificate

1. Start mitmproxy: `mitmweb`
2. Configure your browser to use proxy `localhost:8080`
3. Visit: `http://mitm.it`
4. Download and install the certificate for your OS

**Linux:**
```bash
# Copy certificate
sudo cp ~/.mitmproxy/mitmproxy-ca-cert.pem /usr/local/share/ca-certificates/mitmproxy.crt
sudo update-ca-certificates
```

**macOS:**
```bash
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/.mitmproxy/mitmproxy-ca-cert.pem
```

#### Step 4: Configure Your Application

**For browsers:**
- Firefox: Preferences → Network Settings → Manual Proxy
- Chrome/Edge: System proxy or use extensions like FoxyProxy

**For command-line tools:**
```bash
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080

# Test with curl
curl -x http://localhost:8080 https://example.com
```

**For mobile devices:**
1. Connect phone to same WiFi as computer
2. Find your computer's IP: `ifconfig` or `ip addr`
3. Phone Settings → WiFi → Configure Proxy → Manual
4. Enter your computer's IP and port 8080
5. Visit `http://mitm.it` on phone to install certificate

---

### 🔥 Setting Up Burp Suite

#### Step 1: Download and Install

1. Visit: https://portswigger.net/burp/communitydownload
2. Download for your OS (requires Java)
3. Install and launch

#### Step 2: Configure Browser

**Option A: Use Burp's Embedded Browser (Easiest)**
- Proxy → Intercept → Open Browser
- Pre-configured, no setup needed!

**Option B: Configure Your Browser**
1. Burp Suite → Proxy → Options
2. Default listener: `127.0.0.1:8080`
3. Browser → Proxy Settings → Manual → `localhost:8080`

#### Step 3: Install CA Certificate

1. With proxy configured, visit: `http://burpsuite`
2. Click "CA Certificate" to download
3. Import to your browser/OS certificate store

**Firefox:**
- Settings → Privacy & Security → Certificates → View Certificates
- Import → Select Burp certificate → Trust for websites

**Chrome/System:**
- Linux: Copy to `/usr/local/share/ca-certificates/` and run `update-ca-certificates`
- macOS: Double-click certificate, add to Keychain, set to "Always Trust"
- Windows: certmgr.msc → Trusted Root Certification Authorities → Import

#### Step 4: Start Intercepting

1. Proxy → Intercept → **Intercept is on**
2. Browse to any HTTPS site
3. Requests appear in Burp
4. Click "Forward" to send, or "Drop" to block

---

### 🦈 Setting Up Wireshark for HTTPS Decryption

Wireshark can decrypt HTTPS if you provide the SSL keys.

#### Method 1: Browser SSL Keylog (Easiest)

**For Chrome/Firefox:**

```bash
# Linux/macOS - add to ~/.bashrc or ~/.zshrc
export SSLKEYLOGFILE=~/ssl-keys.log

# Windows - System Environment Variables
SSLKEYLOGFILE=C:\Users\YourName\ssl-keys.log
```

**In Wireshark:**
1. Edit → Preferences → Protocols → TLS
2. (Pre-)Master-Secret log filename: Browse to your keylog file
3. Restart browser and Wireshark

Now Wireshark can decrypt browser HTTPS traffic!

#### Method 2: Server Private Key (Advanced)

If you control the server:
1. Edit → Preferences → Protocols → TLS
2. RSA keys list → Add key file
3. Specify IP, Port, Protocol, and Key file path

---

### 🌐 Setting Up OWASP ZAP

#### Step 1: Installation

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install zaproxy

# Or download from website
wget https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2_14_0_unix.sh
chmod +x ZAP_2_14_0_unix.sh
./ZAP_2_14_0_unix.sh
```

**macOS:**
```bash
brew install --cask owasp-zap
```

**Windows:** Download installer from https://www.zaproxy.org/download/

#### Step 2: Configure Proxy

1. Launch ZAP
2. Tools → Options → Local Proxies
3. Default: `localhost:8080`
4. Configure browser to use this proxy

#### Step 3: Install Certificate

1. Tools → Options → Dynamic SSL Certificates
2. Save certificate
3. Import to browser (same as Burp Suite)

#### Step 4: Automated Scanning

1. Enter target URL in Quick Start
2. Choose "Automated Scan"
3. Click "Attack"
4. Review results in Alerts tab

---

### 📱 Mobile Device Setup (iOS/Android)

#### Android MITM Setup

**Requirements:**
- Android device
- Computer running MITM tool
- Same WiFi network

**Steps:**

1. **Install CA Certificate:**
   ```
   Settings → Security → Encryption & credentials
   → Install from storage → Select certificate
   ```

2. **Configure WiFi Proxy:**
   ```
   Settings → WiFi → Long press network → Modify network
   → Advanced options → Proxy: Manual
   → Hostname: [Your Computer IP]
   → Port: 8080
   ```

3. **For Android 7+** (Apps ignore user certificates):

   **Option A: Use Magisk + MagiskTrustUserCerts** (Rooted)

   **Option B: Modify APK to allow user certs:**
   ```bash
   # Install apktool
   apktool d app.apk

   # Edit AndroidManifest.xml
   # Add to <application> tag:
   # android:networkSecurityConfig="@xml/network_security_config"

   # Create res/xml/network_security_config.xml:
   <network-security-config>
       <base-config cleartextTrafficPermitted="true">
           <trust-anchors>
               <certificates src="system" />
               <certificates src="user" />
           </trust-anchors>
       </base-config>
   </network-security-config>

   # Rebuild and sign
   apktool b app -o app-modified.apk
   ```

#### iOS MITM Setup

**Steps:**

1. **Configure WiFi Proxy:**
   ```
   Settings → WiFi → (i) icon → Configure Proxy → Manual
   → Server: [Your Computer IP]
   → Port: 8080
   ```

2. **Install Certificate:**
   - Visit `http://mitm.it` in Safari
   - Download iOS certificate
   - Settings → Profile Downloaded → Install
   - Enter passcode

3. **Trust Certificate:**
   ```
   Settings → General → About → Certificate Trust Settings
   → Enable full trust for your MITM certificate
   ```

**Certificate Pinning Bypass:**

For apps with certificate pinning, use:
- **SSL Kill Switch 2** (Jailbroken devices)
- **Objection** (Frida-based, no jailbreak needed)

```bash
# Install Frida
pip install frida-tools
pip install objection

# Connect device and run
objection --gadget "com.example.app" explore
> ios sslpinning disable
```

---

## Common Use Cases

### 1. 🔍 API Testing and Debugging

**Scenario:** You're developing a mobile app and need to see what API calls it's making.

**Tool:** mitmproxy

**Steps:**
1. Start mitmweb: `mitmweb`
2. Configure phone to use proxy
3. Open your app
4. View all API requests in web interface
5. Inspect request/response headers, JSON payloads

**Pro Tip:** Use filters in mitmweb to show only specific domains:
```
~d api.example.com
```

---

### 2. 🐛 Finding Security Vulnerabilities

**Scenario:** Testing a web application for common vulnerabilities.

**Tool:** Burp Suite Pro or OWASP ZAP

**Steps:**
1. Configure browser proxy
2. Browse the application normally (spider/crawl)
3. Run automated scanner
4. Review findings:
   - SQL injection
   - XSS vulnerabilities
   - CSRF issues
   - Security misconfigurations
5. Manual testing with Repeater/Intruder

---

### 3. 📱 Mobile App Security Testing

**Scenario:** Analyzing a mobile app for security issues.

**Tool:** mitmproxy + Frida (for certificate pinning bypass)

**Steps:**
1. Decompile APK to check for hardcoded secrets
2. Set up MITM proxy
3. Bypass certificate pinning if needed
4. Intercept and analyze traffic:
   - Authentication mechanisms
   - API endpoints
   - Data encryption
   - Token handling
5. Test for common vulnerabilities:
   - Insecure data storage
   - Weak authentication
   - Insufficient transport layer protection

---

### 4. 🔐 Testing Certificate Pinning

**Scenario:** Verify your app's certificate pinning implementation.

**Tool:** mitmproxy or Burp Suite

**Steps:**
1. Set up proxy without pinning bypass
2. Try to intercept app traffic
3. **Expected result:** App should refuse to connect
4. If traffic is intercepted, pinning is not working!

**Bypassing for testing (authorized only):**
- Android: Use Frida + objection
- iOS: Use SSL Kill Switch 2
- Alternative: Patch the APK/IPA

---

### 5. 🌐 Network Performance Testing

**Scenario:** Test how your app handles slow networks.

**Tool:** Charles Proxy or Burp Suite

**Steps:**
1. Enable throttling:
   - Charles: Proxy → Throttle Settings
   - Burp: Proxy → Options → Match and Replace
2. Set bandwidth limits (e.g., 3G: 780 kbps)
3. Test application responsiveness
4. Check for timeout handling
5. Verify loading states and error messages

---

### 6. 🔄 Request Manipulation Testing

**Scenario:** Test how the server handles modified requests.

**Tool:** Burp Suite Repeater

**Steps:**
1. Intercept a request
2. Send to Repeater (Ctrl+R)
3. Modify parameters:
   - Change user IDs (test authorization)
   - Inject SQL/XSS payloads
   - Modify prices/quantities
   - Add/remove headers
4. Observe responses
5. Document unexpected behaviors

---

## Bypassing Modern Security

### SSL/TLS Certificate Pinning Bypass

**What is Certificate Pinning?**
Apps hardcode expected certificates to prevent MITM attacks, even with trusted CAs.

#### Method 1: Frida + Objection (No Root/Jailbreak)

```bash
# Install
pip install frida-tools objection

# For Android - inject Frida gadget
objection patchapk --source app.apk

# Install patched APK
adb install app-patched.apk

# Start objection
objection explore

# Disable pinning
android sslpinning disable
```

#### Method 2: Magisk Module (Android Root)

```bash
# Install from Magisk Manager:
# - MagiskTrustUserCerts
# - Xposed + JustTrustMe/SSLUnpinning
```

#### Method 3: Manual APK Patching

```bash
# Decompile
apktool d app.apk

# Find pinning code and remove:
# Search for: "TrustManager", "CertificatePinner", "X509Certificate"
# Comment out or modify verification logic

# Rebuild
apktool b app
```

#### Method 4: Frida Script (Manual)

```javascript
// save as bypass-pinning.js
Java.perform(function() {
    var TrustManager = Java.use('javax.net.ssl.X509TrustManager');
    var SSLContext = Java.use('javax.net.ssl.SSLContext');

    var TrustManagers = [TrustManager.$new()];
    var SSLContext_init = SSLContext.init.overload(
        '[Ljavax.net.ssl.KeyManager;',
        '[Ljavax.net.ssl.TrustManager;',
        'java.security.SecureRandom'
    );

    SSLContext_init.implementation = function(keyManager, trustManager, secureRandom) {
        SSLContext_init.call(this, keyManager, TrustManagers, secureRandom);
    };
});

// Run: frida -U -f com.app.name -l bypass-pinning.js --no-pause
```

---

### HTTP Public Key Pinning (HPKP) Bypass

**Modern apps use HPKP instead of certificate pinning.**

**Bypass strategies:**
1. **Find pinned keys in code:**
   ```bash
   # Search in decompiled APK
   grep -r "sha256/" ./
   ```

2. **Replace with your proxy's key:**
   ```bash
   # Get your mitmproxy public key hash
   openssl x509 -in ~/.mitmproxy/mitmproxy-ca-cert.pem -pubkey -noout | \
   openssl pkey -pubin -outform der | \
   openssl dgst -sha256 -binary | \
   base64

   # Replace in app code
   ```

---

### Chrome/Firefox Certificate Transparency Bypass

**Chrome and Firefox may reject certificates without SCT logs.**

**Solution for testing:**
```bash
# Disable CT checking in Chrome
google-chrome --ignore-certificate-errors-spki-list=<your-cert-hash>

# Firefox: about:config
security.pki.certificate_transparency.mode = 0
```

---

### WebSocket Interception

**WebSockets are often forgotten in security testing.**

**With mitmproxy:**
```python
# save as websocket-intercept.py
from mitmproxy import http

def websocket_message(flow):
    # Intercept WebSocket messages
    message = flow.messages[-1]
    print(f"WebSocket: {message.content}")

    # Modify message
    if b"secret" in message.content:
        message.content = b"modified"
```

```bash
mitmproxy -s websocket-intercept.py
```

**With Burp Suite:**
- WebSockets are shown in Proxy history
- Use "WebSocket History" tab
- Intercept and modify with Repeater

---

### gRPC/Protocol Buffers Interception

**Modern microservices use gRPC instead of REST.**

**Setup:**
```bash
# Install mitmproxy with protobuf support
pip install mitmproxy protobuf

# Use mitmproxy addon for gRPC
# https://github.com/mitmproxy/mitmproxy/blob/main/examples/contrib/grpc.py
```

**Alternative: Use Wireshark with protobuf dissector:**
```bash
# Compile .proto files
protoc --descriptor_set_out=myapp.pb myapp.proto

# Load in Wireshark
# Edit → Preferences → Protocols → ProtoBuf
# Add protobuf search paths
```

---

## Best Practices

### ✅ Security Testing Checklist

**Before testing:**
- [ ] Get written authorization
- [ ] Define scope (what's in/out of bounds)
- [ ] Set up isolated test environment
- [ ] Document your testing methodology
- [ ] Prepare incident response plan

**During testing:**
- [ ] Keep detailed logs of all activities
- [ ] Don't test destructive attacks on production
- [ ] Respect rate limits and system resources
- [ ] Document all findings with evidence
- [ ] Communicate critical issues immediately

**After testing:**
- [ ] Securely delete captured sensitive data
- [ ] Provide detailed report with remediation steps
- [ ] Verify fixes with re-testing
- [ ] Archive evidence securely

---

### 🛡️ Protecting Yourself During Testing

1. **Use VPN or isolated network:**
   ```bash
   # Route all MITM traffic through VPN
   # Prevents accidental capture of non-target traffic
   ```

2. **Dedicated testing devices:**
   - Don't use your personal phone/laptop for testing
   - Use VMs or separate devices
   - Prevent cross-contamination

3. **Encrypt your captures:**
   ```bash
   # Encrypt Wireshark captures
   gpg -c capture.pcap

   # Decrypt when needed
   gpg capture.pcap.gpg
   ```

4. **Time-limited testing:**
   - Set boundaries (e.g., 9am-5pm only)
   - Automated tools should have kill switches
   - Don't leave proxies running unattended

---

### 📝 Documentation Standards

**What to log:**
- Timestamp of all tests
- Target systems and scope
- Tools and versions used
- Commands executed
- Findings and evidence
- Impact assessment

**Template for vulnerability report:**
```markdown
## Vulnerability: [Title]

**Severity:** Critical/High/Medium/Low
**CVSS Score:** X.X

### Description
[What is the vulnerability?]

### Steps to Reproduce
1. Set up MITM proxy
2. Intercept request to [endpoint]
3. Modify [parameter] to [value]
4. Observe [behavior]

### Impact
[What can an attacker do?]

### Affected Components
- [Component 1]
- [Component 2]

### Evidence
- Screenshot: [attached]
- PCAP file: [attached]
- Request/Response: [code block]

### Remediation
[How to fix it]

### References
- [CWE link]
- [OWASP link]
```

---

## Troubleshooting

### Common Issues and Solutions

#### 🚨 "SSL Handshake Failed" / "Certificate Error"

**Cause:** MITM certificate not trusted by client.

**Solutions:**
1. Verify certificate is installed correctly
2. Check certificate is trusted (not just installed)
3. For command-line tools, use:
   ```bash
   # Point to CA cert
   curl --cacert ~/.mitmproxy/mitmproxy-ca-cert.pem https://example.com

   # Or disable verification (testing only!)
   curl -k https://example.com
   ```

---

#### 🚨 App Doesn't Work Through Proxy

**Possible causes:**

1. **Certificate pinning** → Use Frida/Objection to bypass
2. **No proxy support** → Use transparent mode:
   ```bash
   # mitmproxy transparent mode
   mitmproxy --mode transparent

   # Set up iptables redirect
   iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 80 -j REDIRECT --to-port 8080
   iptables -t nat -A PREROUTING -i wlan0 -p tcp --dport 443 -j REDIRECT --to-port 8080
   ```
3. **App checks for proxy** → Use VPN mode or reverse proxy

---

#### 🚨 Can't See HTTPS Traffic in Wireshark

**Solutions:**

1. **Set SSLKEYLOGFILE** environment variable
2. **Restart browser** after setting variable
3. **Check Wireshark TLS settings:**
   - Preferences → Protocols → TLS
   - (Pre-)Master-Secret log filename must be set
4. **Filter traffic:** `tls` or `http2`

---

#### 🚨 Mobile Device Can't Connect to Proxy

**Checklist:**
- [ ] Computer and phone on same network
- [ ] Firewall allows connections on proxy port:
   ```bash
   # Linux
   sudo ufw allow 8080

   # macOS
   # System Preferences → Security → Firewall → Options
   ```
- [ ] Proxy listening on all interfaces (0.0.0.0, not 127.0.0.1):
   ```bash
   # mitmproxy
   mitmweb --listen-host 0.0.0.0

   # Burp Suite
   # Proxy → Options → Bind to address: All interfaces
   ```
- [ ] Correct IP address (verify with `ifconfig` or `ip addr`)

---

#### 🚨 "No Internet" After Setting Proxy

**Causes:**
1. Proxy not running
2. Wrong IP/port
3. Proxy crashed

**Quick fix:**
```bash
# Remove proxy settings
# Settings → WiFi → Proxy → None

# Or clear environment variables
unset HTTP_PROXY HTTPS_PROXY
```

---

#### 🚨 High CPU Usage / Slow Performance

**Solutions:**
1. **Filter traffic** to only intercept what you need:
   ```bash
   # mitmproxy - only intercept specific domain
   mitmweb -f "~d api.target.com"
   ```

2. **Disable real-time decoding:**
   - Burp: Proxy → Options → Intercept → Turn off
   - Save to file, analyze later

3. **Use command-line tools** instead of GUI:
   ```bash
   # mitmdump is faster than mitmweb
   mitmdump -w traffic.dump
   ```

---

## FAQ

### Q: Can I use MITM tools on HTTPS traffic?

**A:** Yes! That's the primary purpose. MITM tools create a proxy certificate that your device trusts, allowing the tool to decrypt, inspect, and re-encrypt HTTPS traffic.

---

### Q: Is it legal to use MITM tools?

**A:** It depends:
- ✅ On your own devices/networks: Legal
- ✅ With written authorization: Legal
- ❌ On public WiFi to spy on others: **Illegal**
- ❌ Without permission: **Illegal**

**Always get authorization first.**

---

### Q: Which tool should I start with?

**A:** Depends on your goal:

- **Web app testing:** Start with **OWASP ZAP** (free, automated)
- **API/mobile testing:** Start with **mitmproxy** (simple, powerful)
- **Professional pentesting:** Learn **Burp Suite** (industry standard)
- **Network analysis:** Use **Wireshark** (protocol details)

---

### Q: How do I handle certificate pinning?

**A:** Several approaches:

1. **Dynamic instrumentation:** Frida + Objection (no root needed)
2. **Static patching:** Modify APK/IPA
3. **Root/Jailbreak:** Magisk modules or Xposed
4. **Ask developer:** Sometimes they'll give you a debug build without pinning

**For your own apps:** Consider debug builds with pinning disabled.

---

### Q: Can the application detect my MITM proxy?

**A:** Yes, applications can detect proxies through:

- Certificate chain inspection (custom CA in chain)
- Timing attacks (proxy adds latency)
- Proxy headers (`X-Forwarded-For`, `Via`)
- Known proxy IPs
- Certificate subject differences

**Mitigations:**
- Use transparent mode instead of explicit proxy
- Remove proxy headers
- Use same certificate properties as legitimate server

---

### Q: How do I intercept non-HTTP traffic?

**A:** Different approaches:

- **TCP/UDP traffic:** Use **Wireshark** or **tcpdump**
- **WebSockets:** Supported in **mitmproxy** and **Burp Suite**
- **gRPC:** Use **mitmproxy** with protobuf addon
- **Custom protocols:** Write **Wireshark dissector** or **mitmproxy addon**

---

### Q: Is MITM the same as packet sniffing?

**A:** Similar but different:

| Packet Sniffing | MITM |
|----------------|------|
| Passive (just listens) | Active (intercepts and modifies) |
| Can't decrypt HTTPS | Can decrypt HTTPS |
| Doesn't modify traffic | Can modify traffic |
| Uses promiscuous mode | Uses proxy mode |
| Example: Wireshark, tcpdump | Example: Burp, mitmproxy |

**MITM is more powerful but also more detectable.**

---

### Q: Can I use these tools on production systems?

**A:** 🚨 **Caution required:**

- ✅ Passive interception for debugging: Usually OK
- ⚠️ Active scanning: **Only with approval and maintenance windows**
- ❌ Traffic modification: **Never on production without explicit approval**

**Always:**
- Get approval from management
- Schedule during low-traffic periods
- Have rollback plan
- Monitor for issues
- Document everything

---

### Q: How do I automate MITM testing?

**A:** Use scripting capabilities:

**mitmproxy:**
```python
# auto-intercept.py
from mitmproxy import http

def request(flow: http.HTTPFlow):
    if "api.target.com" in flow.request.host:
        # Modify request
        flow.request.headers["X-Custom"] = "value"

def response(flow: http.HTTPFlow):
    if "password" in flow.response.text:
        print("WARNING: Password in response!")
```

```bash
mitmproxy -s auto-intercept.py
```

**Burp Suite:**
- Use Burp Extensions (Java/Python)
- REST API for automation
- Headless mode for CI/CD

**OWASP ZAP:**
- Full REST API
- Docker containers for CI/CD
- Automation framework

---

### Q: What's the difference between Burp Community and Pro?

**A:** Key differences:

| Feature | Community | Professional |
|---------|-----------|--------------|
| Intercepting Proxy | ✅ | ✅ |
| Repeater | ✅ | ✅ |
| Intruder | ⚠️ Limited | ✅ Full speed |
| Scanner | ❌ | ✅ |
| Extensions | ✅ | ✅ |
| Save/Restore | ❌ | ✅ |
| Support | Community | Official |
| Price | Free | $449/year |

**Recommendation:** Start with Community, upgrade if you need the scanner.

---

### Q: How do I test HTTP/2 and HTTP/3?

**A:**

**HTTP/2:**
- ✅ Supported by: Burp Suite, mitmproxy, Wireshark
- No special configuration needed

**HTTP/3 (QUIC):**
- ⚠️ Limited support (uses UDP, not TCP)
- **Wireshark:** Can decode QUIC with keylog
- **mitmproxy:** Experimental support
- **Alternative:** Use QUIC-specific tools like `qlog`

---

## Additional Resources

### 📚 Learning Resources

- **PortSwigger Web Security Academy:** https://portswigger.net/web-security (Free!)
- **OWASP Testing Guide:** https://owasp.org/www-project-web-security-testing-guide/
- **mitmproxy Documentation:** https://docs.mitmproxy.org/
- **Android App Security:** https://mobile-security.gitbook.io/mobile-security-testing-guide/

### 🛠️ Useful Tools

- **Frida:** https://frida.re/ (Dynamic instrumentation)
- **Objection:** https://github.com/sensepost/objection (Frida helper)
- **apktool:** https://ibotpeaches.github.io/Apktool/ (APK decompiler)
- **Postman:** https://www.postman.com/ (API testing)

### 🏆 Practice Platforms

- **HackTheBox:** https://www.hackthebox.com/
- **PortSwigger Labs:** https://portswigger.net/web-security/all-labs
- **OWASP WebGoat:** https://owasp.org/www-project-webgoat/
- **DVWA:** http://www.dvwa.co.uk/

---

## Contributing

Found an error or want to add a tool? Contributions are welcome!

---

## Final Reminder ⚠️

**MITM tools are powerful and can be dangerous in the wrong hands.**

- 🔐 Only test systems you own or have written permission to test
- 🛡️ Use isolated environments for learning
- 📝 Document all testing activities
- 🤝 Follow responsible disclosure for vulnerabilities
- ⚖️ Understand and comply with local laws

**When in doubt, get explicit written authorization.**

---

## License

This guide is for educational purposes only. Use responsibly.

**Last Updated:** November 2025
