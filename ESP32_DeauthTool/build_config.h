/*
 * ESP32 Pentesting Tool - Build Configuration
 *
 * Enable/disable features to customize your build
 * This allows you to fit more features by disabling unused ones
 *
 * Memory Budget:
 * - ESP32 has ~520KB RAM total
 * - ~200KB used by core system
 * - ~300KB available for features
 *
 * Each feature's approximate memory usage is listed
 */

#ifndef BUILD_CONFIG_H
#define BUILD_CONFIG_H

// ============================================
// CORE FEATURES (Always enabled, required)
// ============================================
// These cannot be disabled
#define FEATURE_WEB_SERVER      true  // Web control interface
#define FEATURE_ACCESS_POINT    true  // AP mode for control
#define FEATURE_NETWORK_SCAN    true  // WiFi network scanning

// ============================================
// ATTACK FEATURES (Enable what you need)
// ============================================

// Basic Attacks (~15KB)
#define FEATURE_DEAUTH          true  // DeAuth attack (5KB)
#define FEATURE_CAPTIVE_PORTAL  true  // Captive portal (8KB)
#define FEATURE_AUTO_CONNECT    true  // Auto-connect to networks (2KB)

// Advanced WiFi Attacks (~25KB total)
#define FEATURE_EVIL_TWIN       false // Evil Twin AP (5KB) - COMING SOON
#define FEATURE_BEACON_FLOOD    false // Beacon flooding (2KB) - COMING SOON
#define FEATURE_PROBE_SNIFF     false // Probe request sniffing (3KB) - COMING SOON
#define FEATURE_KARMA_ATTACK    false // Karma attack (4KB) - COMING SOON
#define FEATURE_WPS_ATTACK      false // WPS PIN attack (8KB) - COMING SOON
#define FEATURE_HANDSHAKE_CAP   false // Handshake capture (10KB) - COMING SOON

// Network Attacks (~30KB total)
#define FEATURE_MITM            true  // MITM framework (8KB)
#define FEATURE_ARP_POISON      true  // ARP poisoning (4KB)
#define FEATURE_DNS_POISON      true  // DNS poisoning (3KB)
#define FEATURE_TRAFFIC_SNIFF   true  // Traffic sniffing (5KB)
#define FEATURE_DHCP_STARVE     false // DHCP starvation (3KB) - COMING SOON
#define FEATURE_SSL_STRIP       false // SSL stripping (6KB) - COMING SOON
#define FEATURE_HTTP_SNIFF      false // HTTP credential extraction (5KB) - COMING SOON

// Reconnaissance (~20KB total)
#define FEATURE_NETWORK_RECON   true  // Network reconnaissance (5KB)
#define FEATURE_DEVICE_SCAN     true  // Device discovery (4KB)
#define FEATURE_PORT_SCAN       false // Port scanning (8KB) - COMING SOON
#define FEATURE_BANNER_GRAB     false // Banner grabbing (4KB) - COMING SOON

// ============================================
// DATA & STORAGE FEATURES
// ============================================

// Storage (~15KB total)
#define FEATURE_CRED_STORAGE    true  // Save credentials to flash (2KB)
#define FEATURE_DEVICE_LOG      true  // Log discovered devices (3KB)
#define FEATURE_TRAFFIC_LOG     true  // Log captured traffic (4KB)
#define FEATURE_SD_CARD         false // SD card export (8KB) - REQUIRES SD MODULE
#define FEATURE_CLOUD_UPLOAD    false // Cloud data upload (12KB) - COMING SOON

// Advanced Logging (~10KB total)
#define FEATURE_PCAP_EXPORT     false // PCAP file export (6KB) - COMING SOON
#define FEATURE_GPS_LOGGING     false // GPS tagging (6KB) - REQUIRES GPS MODULE
#define FEATURE_STATISTICS      false // Statistics dashboard (4KB) - COMING SOON

// ============================================
// AUTOMATION FEATURES
// ============================================

// Automation (~15KB total)
#define FEATURE_AUTO_PILOT      false // Fully automated mode (3KB) - COMING SOON
#define FEATURE_ATTACK_PROFILES false // Save/load profiles (2KB) - COMING SOON
#define FEATURE_SCHEDULED       false // Scheduled attacks (4KB) - COMING SOON
#define FEATURE_SMART_TARGET    false // AI targeting (6KB) - COMING SOON

// Evasion (~8KB total)
#define FEATURE_MAC_SPOOF       false // Random MAC spoofing (1KB) - COMING SOON
#define FEATURE_AUTO_EVASION    false // Detection evasion (5KB) - COMING SOON
#define FEATURE_STEALTH_MODE    false // Stealth operations (3KB) - COMING SOON

// ============================================
// HARDWARE INTERFACE FEATURES
// ============================================

// Display & Controls (~15KB total)
#define FEATURE_OLED_DISPLAY    false // OLED display support (8KB) - REQUIRES OLED
#define FEATURE_BUTTON_CONTROL  false // Physical buttons (2KB) - REQUIRES BUTTONS
#define FEATURE_LED_STATUS      false // LED indicators (1KB) - REQUIRES LEDs
#define FEATURE_BUZZER          false // Audio alerts (1KB) - REQUIRES BUZZER
#define FEATURE_SERIAL_CLI      false // Serial command interface (3KB) - COMING SOON

// Power Management (~5KB total)
#define FEATURE_LOW_POWER       false // Low power mode (2KB) - COMING SOON
#define FEATURE_BATTERY_MON     false // Battery monitoring (2KB) - REQUIRES ADC

// ============================================
// SECURITY & DETECTION FEATURES
// ============================================

// Security Testing (~12KB total)
#define FEATURE_IDS_DETECT      false // IDS/IPS detection (5KB) - COMING SOON
#define FEATURE_ROGUE_AP_DETECT false // Rogue AP detection (4KB) - COMING SOON
#define FEATURE_ENCRYPTION_ANAL false // Encryption analysis (3KB) - COMING SOON

// ============================================
// API & INTEGRATION FEATURES
// ============================================

// External Integration (~10KB total)
#define FEATURE_REST_API        true  // Full REST API (included in web server)
#define FEATURE_WEBSOCKET       false // WebSocket real-time updates (5KB) - COMING SOON
#define FEATURE_MQTT            false // MQTT integration (8KB) - COMING SOON

// ============================================
// PRESET BUILD CONFIGURATIONS
// ============================================

// Uncomment ONE of these to use a preset build
// (Comment out to use custom configuration above)

// #define BUILD_PRESET_MINIMAL       // Only basic features (~100KB)
// #define BUILD_PRESET_BALANCED      // Good mix of features (~200KB)
// #define BUILD_PRESET_ADVANCED      // All software features (~300KB)
// #define BUILD_PRESET_STEALTH       // Stealth & evasion focused
// #define BUILD_PRESET_RECON         // Reconnaissance focused
// #define BUILD_PRESET_STANDALONE    // For hardware with OLED/buttons

// ============================================
// PRESET CONFIGURATIONS
// ============================================

#ifdef BUILD_PRESET_MINIMAL
  #undef FEATURE_MITM
  #undef FEATURE_ARP_POISON
  #undef FEATURE_DNS_POISON
  #undef FEATURE_TRAFFIC_SNIFF
  #undef FEATURE_NETWORK_RECON

  #define FEATURE_MITM            false
  #define FEATURE_ARP_POISON      false
  #define FEATURE_DNS_POISON      false
  #define FEATURE_TRAFFIC_SNIFF   false
  #define FEATURE_NETWORK_RECON   false
#endif

#ifdef BUILD_PRESET_BALANCED
  // Use defaults (nothing to change)
#endif

#ifdef BUILD_PRESET_ADVANCED
  #undef FEATURE_EVIL_TWIN
  #undef FEATURE_BEACON_FLOOD
  #undef FEATURE_PROBE_SNIFF
  #undef FEATURE_KARMA_ATTACK

  #define FEATURE_EVIL_TWIN       true
  #define FEATURE_BEACON_FLOOD    true
  #define FEATURE_PROBE_SNIFF     true
  #define FEATURE_KARMA_ATTACK    true
#endif

#ifdef BUILD_PRESET_STEALTH
  #undef FEATURE_MAC_SPOOF
  #undef FEATURE_AUTO_EVASION
  #undef FEATURE_STEALTH_MODE

  #define FEATURE_MAC_SPOOF       true
  #define FEATURE_AUTO_EVASION    true
  #define FEATURE_STEALTH_MODE    true
#endif

#ifdef BUILD_PRESET_RECON
  #undef FEATURE_PORT_SCAN
  #undef FEATURE_BANNER_GRAB
  #undef FEATURE_PROBE_SNIFF
  #undef FEATURE_NETWORK_RECON

  #define FEATURE_PORT_SCAN       true
  #define FEATURE_BANNER_GRAB     true
  #define FEATURE_PROBE_SNIFF     true
  #define FEATURE_NETWORK_RECON   true

  // Disable attacks to save memory
  #undef FEATURE_DEAUTH
  #undef FEATURE_MITM
  #define FEATURE_DEAUTH          false
  #define FEATURE_MITM            false
#endif

#ifdef BUILD_PRESET_STANDALONE
  #undef FEATURE_OLED_DISPLAY
  #undef FEATURE_BUTTON_CONTROL
  #undef FEATURE_LED_STATUS
  #undef FEATURE_BATTERY_MON

  #define FEATURE_OLED_DISPLAY    true
  #define FEATURE_BUTTON_CONTROL  true
  #define FEATURE_LED_STATUS      true
  #define FEATURE_BATTERY_MON     true
#endif

// ============================================
// MEMORY LIMITS & SAFETY CHECKS
// ============================================

// Maximum number of items to store (to prevent memory overflow)
#define MAX_NETWORKS            50    // Max WiFi networks to store
#define MAX_DEVICES             30    // Max discovered devices
#define MAX_CREDENTIALS         50    // Max captured credentials
#define MAX_TRAFFIC_LOGS        100   // Max traffic captures
#define MAX_DNS_LOGS            50    // Max DNS queries

// Buffer sizes
#define WEB_RESPONSE_BUFFER     4096  // Web response buffer size
#define PACKET_BUFFER_SIZE      1500  // Packet capture buffer
#define STRING_BUFFER_SIZE      256   // General string buffer

// ============================================
// PERFORMANCE TUNING
// ============================================

// Web server settings
#define WEB_SERVER_TIMEOUT      5000  // HTTP timeout (ms)
#define WEB_UPDATE_INTERVAL     3000  // Status update interval (ms)

// Attack settings
#define DEAUTH_DEFAULT_PACKETS  20    // Packets per deauth burst
#define DEAUTH_DEFAULT_DELAY    100   // Delay between bursts (ms)
#define SCAN_TIMEOUT            5000  // Network scan timeout (ms)

// Network settings
#define CONNECT_TIMEOUT         10000 // WiFi connect timeout (ms)
#define RECON_INTERVAL          10000 // Reconnaissance interval (ms)

// ============================================
// DEBUG & DEVELOPMENT
// ============================================

#define DEBUG_ENABLED           true  // Enable serial debug output
#define DEBUG_VERBOSE           false // Verbose logging (uses more memory)
#define DEBUG_PACKET_DUMP       false // Dump raw packets (VERY verbose)

// ============================================
// FEATURE DEPENDENCY CHECKS
// ============================================

// Automatic dependency resolution
#if FEATURE_EVIL_TWIN
  #ifndef FEATURE_DEAUTH
    #define FEATURE_DEAUTH true  // Evil twin needs deauth
  #endif
#endif

#if FEATURE_MITM
  #ifndef FEATURE_ARP_POISON
    #define FEATURE_ARP_POISON true  // MITM needs ARP poison
  #endif
#endif

#if FEATURE_SD_CARD || FEATURE_PCAP_EXPORT
  #ifndef FEATURE_TRAFFIC_LOG
    #define FEATURE_TRAFFIC_LOG true  // Need logging for export
  #endif
#endif

// ============================================
// COMPILE-TIME MEMORY ESTIMATION
// ============================================

// This gives you a rough idea of memory usage at compile time
#define ESTIMATED_FLASH_USAGE ( \
  (FEATURE_DEAUTH          ? 5  : 0) + \
  (FEATURE_CAPTIVE_PORTAL  ? 8  : 0) + \
  (FEATURE_AUTO_CONNECT    ? 2  : 0) + \
  (FEATURE_EVIL_TWIN       ? 5  : 0) + \
  (FEATURE_BEACON_FLOOD    ? 2  : 0) + \
  (FEATURE_PROBE_SNIFF     ? 3  : 0) + \
  (FEATURE_KARMA_ATTACK    ? 4  : 0) + \
  (FEATURE_WPS_ATTACK      ? 8  : 0) + \
  (FEATURE_HANDSHAKE_CAP   ? 10 : 0) + \
  (FEATURE_MITM            ? 8  : 0) + \
  (FEATURE_ARP_POISON      ? 4  : 0) + \
  (FEATURE_DNS_POISON      ? 3  : 0) + \
  (FEATURE_TRAFFIC_SNIFF   ? 5  : 0) + \
  (FEATURE_NETWORK_RECON   ? 5  : 0) + \
  (FEATURE_PORT_SCAN       ? 8  : 0) + \
  (FEATURE_OLED_DISPLAY    ? 8  : 0) + \
  (FEATURE_SD_CARD         ? 8  : 0) + \
  100 /* base system */ \
)

// Warning if estimated usage is too high
#if ESTIMATED_FLASH_USAGE > 500
  #warning "Estimated flash usage is high! Consider disabling some features."
#endif

// ============================================
// HELPER MACROS
// ============================================

// Use these in your code to conditionally compile features
#define IF_FEATURE(feature) if (FEATURE_##feature)
#define WHEN_FEATURE(feature) #if FEATURE_##feature

// Example usage in main code:
// IF_FEATURE(DEAUTH) { performDeauth(); }
// This will only execute if FEATURE_DEAUTH is enabled

#endif // BUILD_CONFIG_H
