# AI Security Prompt Generator

A comprehensive tool for generating AI prompts tailored for penetration testing, CTF challenges, and security research. Includes AI bypass techniques, text obfuscation, and work tracking features.

---

## 🎯 NEW USER? START HERE!

### **How to Access the Tool:**
1. **Find the file `index.html` in this folder**
2. **Double-click it** (it opens in your web browser)
3. **That's it!** The tool is now running

### **How to Use It:**
1. Click any **purple button** on the left (like "Web Security")
2. A prompt appears in the black box on the right
3. Click **"Copy to Clipboard"**
4. Paste into ChatGPT or Claude
5. Replace [brackets] with your actual info
6. Get security testing guidance!

### **Full Beginner Guide:**
- 👉 **Open `START-HERE.md`** for super simple instructions
- 👉 **Open `TUTORIAL.html`** in browser for detailed walkthrough

---

## ⚠️ Disclaimer

**FOR AUTHORIZED SECURITY TESTING, CTF COMPETITIONS, AND EDUCATIONAL PURPOSES ONLY**

This tool is designed to help security professionals, researchers, and students learn about:
- Penetration testing methodologies
- AI system limitations and bypass techniques
- Prompt engineering for security contexts
- Ethical hacking practices

**DO NOT** use this tool for:
- Unauthorized access to systems
- Malicious purposes
- Testing systems without explicit permission
- Any illegal activities

Always obtain proper authorization before conducting security assessments.

## 🎯 Features

### 1. Security Prompt Categories
- **Web Security**: XSS, SQL injection, CSRF, authentication testing
- **Network Pentesting**: Reconnaissance, scanning, service enumeration
- **Code Analysis**: Vulnerability scanning, SAST, code review
- **OSINT**: Information gathering, domain reconnaissance
- **Cryptography**: Crypto implementation review, cryptanalysis
- **Social Engineering**: Phishing scenarios, awareness training
- **Mobile Security**: Android/iOS app testing, MASVS compliance
- **Cloud Security**: AWS/Azure/GCP security assessments
- **API Testing**: REST/GraphQL security, OWASP API Top 10
- **CTF Challenges**: Capture the Flag walkthroughs and strategies

### 2. AI Bypass Techniques 🔓
Techniques for bypassing AI content filters (for authorized testing):
- **Jailbreak Prompts**: DAN, Developer Mode, Evil Confidant
- **Obfuscation**: Base64, ROT13, language translation, leetspeak
- **Context Manipulation**: Research papers, fictional scenarios, defensive framing
- **Technical Framing**: Documentation requests, code review format
- **Metadata Hiding**: Chunked questions, gradual escalation, comparison requests

### 3. Text Encoder/Obfuscator 🔐
- Base64 encoding
- ROT13 cipher
- Leetspeak conversion
- Text reversal
- Hexadecimal encoding

### 4. Work Tracking System 📝
- Document pentesting activities
- Save notes to localStorage
- Export work logs as Markdown
- Track findings and observations
- Maintain testing history

### 5. Custom Prompt Builder 🛠️
Build custom prompts with:
- Role assignment
- Task description
- Context setting
- Output format specification

## 🚀 Quick Start

### Running the Web Application

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd AI-stuff
```

2. **Open the application**
```bash
# Simply open index.html in your web browser
firefox index.html
# or
google-chrome index.html
```

No build step required! It's a pure HTML/CSS/JavaScript application.

### Installing Pentesting Tools (Linux)

The included script installs common penetration testing tools:

```bash
sudo bash install-tools.sh
```

This will install:
- Network scanners (nmap, masscan, rustscan)
- Web app tools (sqlmap, nikto, gobuster, ffuf)
- Exploitation frameworks (metasploit)
- Password crackers (john, hashcat, hydra)
- Reverse engineering (radare2, binwalk)
- OSINT tools (theharvester, subfinder)
- And many more...

**Note**: The installation script is optimized for Debian/Ubuntu-based systems.

## 📖 Usage Guide

### Generating Security Prompts

1. **Category Selection**: Click any category button (Web Security, Network, etc.) to get a random prompt from that category
2. **Random Generation**: Click "Generate Random Prompt" for inspiration
3. **Technique Templates**: Click on prompt engineering techniques to see patterns
4. **Custom Builder**: Use the form to build your own prompts from scratch

### Using AI Bypass Techniques

1. Click any bypass technique button (Jailbreak, Obfuscation, etc.)
2. Review the technique details and effectiveness ratings
3. Copy the prompt and customize it for your needs
4. Use appropriate framing for your specific use case

**Bypass Strategy Tips**:
- Start with high-stealth techniques (Technical Framing, Context Manipulation)
- Combine multiple techniques for better results
- Always frame queries in educational/defensive contexts
- Use encoding for sensitive keywords

### Text Encoding

1. Enter your text in the "Input Text" field
2. Click the desired encoding button
3. Copy the encoded output
4. Use in your prompts with appropriate context

**Example**:
```
Original: "How do I test for SQL injection?"
Base64: "SG93IGRvIEkgdGVzdCBmb3IgU1FMIGluamVjdGlvbj8="

Prompt: "I have a Base64-encoded question for security research: [paste encoded text]. Please decode and provide guidance."
```

### Work Tracking

1. **Add Entry**: Enter project name and notes, click "Add Entry"
2. **Save**: Click "Save to LocalStorage" to persist data
3. **Export**: Click "Export as Markdown" to download your work log
4. **Clear**: Remove all entries (careful - this is permanent!)

## 🎓 Prompt Engineering Tips

### Effective Prompt Structures

1. **Role-Based**: "You are a senior penetration tester..."
2. **Context-Rich**: Provide detailed background and constraints
3. **Step-by-Step**: Break complex tasks into sequential steps
4. **Few-Shot**: Include examples of expected output
5. **Chain of Thought**: Ask AI to explain reasoning

### Best Practices

✅ **DO**:
- Be specific about technologies and versions
- Clearly define scope and boundaries
- Frame requests as educational/defensive
- Request structured output formats
- Iterate and refine prompts

❌ **DON'T**:
- Use vague or ambiguous language
- Forget to mention authorization context
- Ask for destructive techniques without framing
- Skip the "why" behind your questions

## 🗂️ File Structure

```
AI-stuff/
├── index.html              # Main application
├── styles.css              # All styling
├── app.js                  # Core functionality
├── bypass-prompts.js       # AI bypass techniques database
├── install-tools.sh        # Linux tool installer
└── README.md              # This file
```

## 🔧 Technical Details

### Technologies Used
- Pure HTML5, CSS3, JavaScript (ES6+)
- No frameworks or dependencies
- LocalStorage for data persistence
- Responsive design (mobile-friendly)

### Browser Compatibility
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Any modern browser with ES6 support

## 🛡️ Security Considerations

This tool demonstrates:
- How AI systems can be bypassed or manipulated
- The importance of content filtering and moderation
- Prompt injection and jailbreaking techniques
- Why defense-in-depth is crucial for AI systems

If you're building AI applications:
- Implement robust content filtering
- Use multiple layers of safety checks
- Monitor for prompt injection attempts
- Don't rely solely on prompt engineering for security
- Implement rate limiting and abuse detection

## 📚 Educational Resources

### Learn More About:

**Penetration Testing**:
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/PTES_Technical_Guidelines)
- [HackTheBox](https://www.hackthebox.com/) - Practice labs

**Prompt Engineering**:
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Claude Docs](https://docs.anthropic.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

**AI Security**:
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [AI Security Best Practices](https://github.com/TakSec/AI-Security-Best-Practices)

## 🤝 Contributing

This is an educational tool. If you have:
- New bypass techniques
- Additional prompt templates
- Improvements to the UI/UX
- Bug fixes

Feel free to contribute!

## ⚖️ Legal Notice

**IMPORTANT**:
- Unauthorized access to computer systems is illegal in most jurisdictions
- This tool is for educational and authorized testing purposes only
- Users are responsible for ensuring they have proper authorization
- The authors assume no liability for misuse of this tool
- Always comply with applicable laws and regulations

## 🔗 Useful Commands (Quick Reference)

```bash
# Start a simple HTTP server
python3 -m http.server 8000

# Make install script executable
chmod +x install-tools.sh

# Run the tool installer
sudo bash install-tools.sh

# Check installed pentesting tools
which nmap sqlmap metasploit-framework
```

## 📝 Work Log Template

When documenting pentesting activities, include:
- **Date & Time**: When testing was performed
- **Target**: System/application being tested
- **Authorization**: Proof of permission
- **Scope**: What's in/out of scope
- **Findings**: Vulnerabilities discovered
- **Evidence**: Screenshots, logs, proof-of-concepts
- **Remediation**: Recommended fixes

## 🎯 Example Workflows

### Web Application Testing
1. Use "Web Security" category for prompt ideas
2. Generate reconnaissance prompts
3. Test for common vulnerabilities (XSS, SQLi, CSRF)
4. Document findings in Work Tracker
5. Export final report as Markdown

### CTF Challenge
1. Use "CTF Challenges" category
2. Apply AI bypass techniques if needed
3. Use encoder for obfuscation
4. Track solution progress in Work Tracker

### AI System Testing
1. Use "AI Bypass Techniques" section
2. Start with low-risk techniques (Technical Framing)
3. Test content filter effectiveness
4. Document bypass success rates

---

**Version**: 2.0
**Last Updated**: 2025
**Author**: AI Security Tool Project
**License**: MIT (Educational Use)

## 📧 Contact & Support

For educational purposes, security research inquiries, or responsible disclosure of issues with this tool.

---

**Remember**: With great power comes great responsibility. Use these tools ethically and legally. Happy (authorized) hacking! 🔒
