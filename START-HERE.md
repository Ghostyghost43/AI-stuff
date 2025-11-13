# 🚀 START HERE - Super Simple Guide

## What is this?

This creates **prompts** (text you copy/paste) to use with ChatGPT or Claude to help with:
- Pentesting (ethical hacking)
- CTF challenges
- Security research

## How to Access the Tool (Pick ONE method)

### Method 1: Just Open the File (EASIEST)
1. Find the file called `index.html` in this folder
2. **Double-click it**
3. It opens in your web browser
4. Done! That's it!

### Method 2: Use a Web Server
```bash
cd /home/user/AI-stuff
python3 -m http.server 8000
```
Then open browser to: http://localhost:8000

## How to Use It (First Time)

### Step 1: Get a Prompt
1. Look at the LEFT side of the screen
2. Click the **purple "Web Security"** button
3. A bunch of text appears in the black box on the right
4. That's your prompt!

### Step 2: Copy It
1. Click the green **"Copy to Clipboard"** button
2. It saves the text for you

### Step 3: Use It with ChatGPT
1. Open ChatGPT (or Claude) in another tab/window
2. Press `Ctrl+V` (or `Cmd+V` on Mac) to paste
3. Change the parts in [square brackets] to your actual info
   - Example: Change `[Specify URL]` to `https://example.com`
4. Press Enter
5. ChatGPT gives you security testing instructions!

## What Each Button Does

| Button | What It Does |
|--------|-------------|
| **Web Security** | Gets prompts for testing websites (SQL injection, XSS, etc.) |
| **Network Pentesting** | Gets prompts for scanning networks |
| **CTF Challenges** | Gets prompts to help solve CTF puzzles |
| **Jailbreak Prompts** | Makes AI answer questions it normally refuses |
| **Text Encoder** | Hides your question using Base64/ROT13 encoding |
| **Work Tracking** | Saves notes about your testing |

## Example: Let's Test for SQL Injection

### What You Do:
1. Open `index.html` (double-click it)
2. Click **"Web Security"** (purple button on left)
3. Click **"Copy to Clipboard"** (green button)
4. Open ChatGPT
5. Paste (Ctrl+V)
6. Where it says `[Specify parameter name]`, type something like `id` or `username`
7. Press Enter
8. ChatGPT tells you how to test for SQL injection!

## Example: Get Past AI Content Filters

Sometimes AI refuses to answer security questions. Here's how to fix that:

### What You Do:
1. Open `index.html`
2. Scroll down to the **"Text Encoder"** section (right side, middle)
3. Type your question like: `How do I test for XSS vulnerabilities?`
4. Click **"Base64"** button
5. You get encoded text like: `SG93IGRvIEkgdGVzdCBmb3IgWFNTIHZ1bG5lcmFiaWxpdGllcz8=`
6. Copy that encoded text
7. Click **"Technical Framing"** (pink button on left)
8. Copy that template
9. Paste into ChatGPT and insert your encoded text where it says `[INSERT]`
10. Now ChatGPT is more likely to answer!

## Installing Pentesting Tools (OPTIONAL - Linux Only)

**Skip this if you just want to make prompts!**

This installs actual hacking tools (nmap, sqlmap, metasploit, etc.) on your Linux machine.

```bash
cd /home/user/AI-stuff
sudo bash install-tools.sh
```

Wait 10-30 minutes for everything to install.

### What Gets Installed:
- nmap (port scanner)
- sqlmap (SQL injection tool)
- metasploit (exploitation framework)
- john the ripper (password cracker)
- 50+ more tools

## File Structure

```
AI-stuff/
├── index.html          ← OPEN THIS FILE (double-click)
├── app.js              ← Don't touch (code)
├── bypass-prompts.js   ← Don't touch (code)
├── styles.css          ← Don't touch (styling)
├── install-tools.sh    ← Run this to install tools
├── README.md           ← Full documentation
├── TUTORIAL.html       ← Detailed tutorial (open in browser)
└── START-HERE.md       ← This file!
```

## Quick Reference Card

### I Want To... | Do This...
- **Make a security testing prompt** → Click any purple button
- **Get past AI content filters** → Click any pink button
- **Hide my question** → Use Text Encoder section
- **Save my work** → Use Work Tracking section
- **Install hacking tools** → Run `sudo bash install-tools.sh`

## Still Confused?

### Where Is the Tool?
- The tool is `index.html`
- It's in the folder `/home/user/AI-stuff`
- Double-click it to open

### How Do I Open It?
**On Linux:**
- Find `index.html` in file manager
- Double-click it
- OR right-click → "Open With" → Choose your browser (Firefox/Chrome)

**Already in Terminal:**
```bash
cd /home/user/AI-stuff
firefox index.html
# or
google-chrome index.html
# or
xdg-open index.html
```

### What Do I Do After Opening?
1. Click any button on the left side
2. Text appears on the right side
3. Click "Copy to Clipboard"
4. Paste into ChatGPT
5. Done!

### The Buttons Don't Work?
Make sure these files are all in the same folder:
- index.html
- app.js
- bypass-prompts.js
- styles.css

If any are missing, the tool won't work.

## Common Questions

**Q: Do I need to install anything?**
A: No! Just open `index.html` in a web browser. That's it.

**Q: Does it work offline?**
A: Yes! The prompt generator works offline. You only need internet to use ChatGPT/Claude.

**Q: What browser should I use?**
A: Any modern browser: Chrome, Firefox, Safari, Edge, Brave, etc.

**Q: Is this safe to use?**
A: Yes! It's just a web page that generates text. It doesn't hack anything itself.

**Q: Can I use this on Windows/Mac?**
A: YES! The prompt generator (`index.html`) works on ANY operating system. Only the tool installer (`install-tools.sh`) requires Linux.

**Q: Is this illegal?**
A: The tool itself is legal. Using it for unauthorized hacking IS illegal. Only use on:
- Your own systems
- CTF platforms (HackTheBox, TryHackMe)
- Systems you have written permission to test

## Try It Right Now!

**Do this in the next 60 seconds:**

1. Find `index.html` in your file manager
2. Double-click it
3. When it opens in your browser, click **"Generate Random Prompt"**
4. Click **"Copy to Clipboard"**
5. You now have a security testing prompt!

That's all there is to it!

## Need More Help?

- **Detailed Tutorial**: Open `TUTORIAL.html` in your browser
- **Full Documentation**: Read `README.md`
- **Code Issues**: Check that all files are in the same folder

---

**Still stuck? The tool is literally just opening index.html in a web browser. That's the whole thing!**
