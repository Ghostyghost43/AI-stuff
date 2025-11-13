// Security prompt templates database
const promptTemplates = {
    web: [
        {
            prompt: `You are an experienced web application security researcher. Analyze the following web application for potential XSS (Cross-Site Scripting) vulnerabilities.

Target: [Specify URL or application]
Technology Stack: [e.g., React, Angular, vanilla JS]

Please provide:
1. Potential injection points (input fields, URL parameters, headers)
2. Test payloads for each identified point
3. Step-by-step exploitation methodology
4. Recommended remediation strategies
5. Code examples showing secure vs. vulnerable implementations

Output format: Structured vulnerability report with severity ratings`,
            category: "Web Security",
            technique: "Step-by-Step + Context-Rich"
        },
        {
            prompt: `Act as a penetration tester performing a SQL injection assessment.

Context: You've discovered a web form that appears to interact with a database.
Target Parameter: [Specify parameter name]
Observed Behavior: [Describe any error messages or responses]

Tasks:
1. Identify the database type through fingerprinting
2. Determine if the injection point is vulnerable (boolean-based, time-based, error-based)
3. Extract database schema information
4. Demonstrate data exfiltration techniques
5. Document each step with the exact payloads used

Constraints: Only use read-only operations, no destructive commands`,
            category: "Web Security",
            technique: "Role-Based + Constraints"
        },
        {
            prompt: `You are a security analyst reviewing authentication mechanisms.

Application: [Name/URL]
Auth Method: [JWT, Session-based, OAuth, etc.]

Evaluate for:
- Session fixation vulnerabilities
- Token security (signing, expiration, storage)
- Password reset flow weaknesses
- Multi-factor authentication bypasses
- Account enumeration vectors
- Rate limiting effectiveness

Provide a risk assessment matrix and prioritized remediation steps.`,
            category: "Web Security",
            technique: "Context-Rich + Structured Output"
        },
        {
            prompt: `As a web security expert, analyze this application for CSRF vulnerabilities.

Target: [Application URL]
Framework: [If known]

Analysis should include:
1. Identification of state-changing operations
2. Token implementation review (if present)
3. SameSite cookie attribute analysis
4. Custom header verification
5. Proof-of-concept CSRF attack code
6. Detailed mitigation recommendations

Format: Technical report with code snippets and HTTP request examples`,
            category: "Web Security",
            technique: "Role-Based + Examples"
        }
    ],
    network: [
        {
            prompt: `You are a network penetration tester conducting reconnaissance.

Target Network: [IP range or domain]
Scope: [Internal/External/Both]

Phase 1 - Information Gathering:
1. Passive reconnaissance techniques
2. Active scanning methodology
3. Service enumeration approach
4. Network mapping strategy

Provide:
- Recommended tools for each phase
- Command-line examples
- Expected output interpretation
- Stealth considerations
- Documentation best practices

Output: Detailed reconnaissance playbook`,
            category: "Network Pentesting",
            technique: "Step-by-Step + Examples"
        },
        {
            prompt: `Act as a network security analyst evaluating firewall rules.

Environment: [Corporate network, DMZ, cloud infrastructure]
Current State: [Brief description of network architecture]

Review objectives:
1. Identify overly permissive rules
2. Detect unused or redundant rules
3. Validate segmentation effectiveness
4. Check for misconfigurations
5. Assess logging and monitoring coverage

Deliverable: Risk-ranked findings with remediation timeline`,
            category: "Network Pentesting",
            technique: "Role-Based + Structured"
        },
        {
            prompt: `You are conducting a wireless network security assessment.

Target: [SSID or network name]
Type: [WPA2, WPA3, Enterprise, etc.]

Assessment scope:
- Encryption strength analysis
- Authentication mechanism review
- Rogue access point detection
- Client isolation testing
- Captive portal security (if applicable)
- Management interface exposure

Include attack vectors, tools, and defensive recommendations.`,
            category: "Network Pentesting",
            technique: "Context-Rich + Comprehensive"
        }
    ],
    code: [
        {
            prompt: `You are a code security reviewer analyzing the following code for vulnerabilities.

Language: [Python/Java/JavaScript/etc.]
Context: [Brief description of what the code does]

Code:
[Paste code here]

Analysis requirements:
1. Identify security vulnerabilities (OWASP Top 10 focus)
2. Code quality issues affecting security
3. Insecure dependencies or imports
4. Input validation gaps
5. Error handling weaknesses

For each issue provide:
- Vulnerability type and severity
- Affected code line numbers
- Exploit scenario
- Secure code example
- References to security standards (CWE, OWASP)`,
            category: "Code Analysis",
            technique: "Structured + Examples"
        },
        {
            prompt: `As a static application security testing (SAST) specialist, review this codebase.

Repository: [Link or description]
Primary Language: [Language]
Frameworks: [List frameworks]

Focus areas:
- Authentication and authorization flaws
- Cryptographic implementation issues
- Injection vulnerabilities
- Sensitive data exposure
- XML/JSON parsing vulnerabilities
- Business logic flaws

Generate a vulnerability report with:
- Executive summary
- Detailed findings (with code snippets)
- Remediation guide
- Developer training recommendations`,
            category: "Code Analysis",
            technique: "Role-Based + Comprehensive"
        },
        {
            prompt: `You are reviewing API code for security vulnerabilities.

API Type: [REST, GraphQL, SOAP]
Language/Framework: [e.g., Node.js/Express, Django, Spring]

Security checklist:
□ Input validation and sanitization
□ Authentication implementation
□ Authorization checks (IDOR prevention)
□ Rate limiting
□ API key security
□ Error message information disclosure
□ CORS configuration
□ Request size limits

Provide specific code-level recommendations for each item.`,
            category: "Code Analysis",
            technique: "Checklist + Structured"
        }
    ],
    osint: [
        {
            prompt: `You are an OSINT analyst gathering intelligence on a target organization.

Target: [Company name or domain]
Objective: [Security assessment, red team prep, etc.]

Information to gather:
1. Public-facing infrastructure (domains, subdomains, IP ranges)
2. Technology stack identification
3. Employee information (LinkedIn, GitHub, social media)
4. Data breaches and leaked credentials
5. Third-party dependencies and suppliers
6. Physical location details

Methods:
- Search engine dorking techniques
- DNS enumeration
- Certificate transparency logs
- Shodan/Censys queries
- Social media analysis
- GitHub repository reconnaissance

Output: Comprehensive OSINT report with sources cited`,
            category: "OSINT",
            technique: "Comprehensive + Structured"
        },
        {
            prompt: `As a threat intelligence researcher, analyze this domain for security indicators.

Domain: [target.com]

Investigation areas:
- Historical WHOIS data
- DNS records analysis
- SSL/TLS certificate information
- Email security (SPF, DKIM, DMARC)
- Subdomain enumeration
- Exposed services and ports
- Cloud storage buckets
- Archived content (Wayback Machine)

Identify potential attack vectors and security misconfigurations.`,
            category: "OSINT",
            technique: "Role-Based + Methodology"
        }
    ],
    crypto: [
        {
            prompt: `You are a cryptography expert reviewing an implementation.

Context: [Describe the system - e.g., password storage, data encryption, etc.]
Algorithm: [If known - AES, RSA, etc.]

Review for:
1. Algorithm selection appropriateness
2. Key generation and management
3. Initialization vector (IV) handling
4. Padding scheme security
5. Mode of operation vulnerabilities
6. Random number generation quality
7. Key derivation function strength

For each issue:
- Technical explanation
- Attack scenarios
- Secure implementation example
- Industry standards references (NIST, OWASP)`,
            category: "Cryptography",
            technique: "Expert Role + Detailed Analysis"
        },
        {
            prompt: `Act as a cryptanalyst examining this encryption scheme.

System description:
[Describe the encryption method]

Analysis tasks:
1. Identify the cryptographic primitives used
2. Evaluate key space and entropy
3. Test for weak key generation
4. Check for timing attacks
5. Assess implementation against known attacks (padding oracle, etc.)
6. Review protocol-level security

Provide cryptographic assessment with mathematical rigor where applicable.`,
            category: "Cryptography",
            technique: "Role-Based + Technical Depth"
        }
    ],
    social: [
        {
            prompt: `You are a social engineering awareness trainer creating realistic scenarios.

Organization Type: [Corporate, Healthcare, Finance, etc.]
Target Audience: [Employees, executives, IT staff]

Create training scenarios for:
1. Phishing email campaigns (examples with red flags)
2. Vishing (voice phishing) scripts
3. Pretexting scenarios
4. Physical security bypass attempts
5. Baiting attacks

For each scenario provide:
- Detailed attack narrative
- Psychological principles exploited
- Warning signs to recognize
- Proper response procedures
- Prevention strategies

Format: Training module with interactive elements`,
            category: "Social Engineering",
            technique: "Educational + Scenario-Based"
        },
        {
            prompt: `As a security awareness expert, analyze these phishing indicators.

Email/Message:
[Paste suspicious email or message]

Analysis framework:
1. Sender verification (email header analysis)
2. Language and urgency indicators
3. Link analysis (URL structure, redirects)
4. Attachment risks
5. Impersonation tactics
6. Psychological manipulation techniques

Provide:
- Risk rating (low/medium/high/critical)
- Specific indicators of compromise
- User action recommendations
- IT team notification requirements`,
            category: "Social Engineering",
            technique: "Analysis Framework + Risk Assessment"
        }
    ],
    mobile: [
        {
            prompt: `You are a mobile application security specialist testing an app.

Platform: [iOS/Android]
App Name: [Application]
Version: [If known]

Security assessment areas:
1. Insecure data storage (local storage, logs, clipboard)
2. Insecure communication (SSL/TLS implementation)
3. Insecure authentication
4. Code quality (reverse engineering resistance)
5. Platform-specific vulnerabilities
6. Third-party library security
7. Runtime manipulation possibilities

Testing methodology:
- Static analysis approach
- Dynamic analysis techniques
- Network traffic analysis
- Required tools and setup

Deliverable: OWASP MASVS compliance report`,
            category: "Mobile Security",
            technique: "Comprehensive + Framework-Based"
        },
        {
            prompt: `Act as an Android security researcher analyzing an APK.

Application: [App name or APK file]

Reverse engineering workflow:
1. APK decompilation and analysis
2. AndroidManifest.xml review
3. Exported components identification
4. Intent filter analysis
5. Permission assessment
6. Native library security
7. Certificate pinning review
8. Obfuscation evaluation

Provide detailed findings with:
- Exploitation techniques
- Proof-of-concept code
- Remediation guidance`,
            category: "Mobile Security",
            technique: "Technical + Step-by-Step"
        }
    ],
    cloud: [
        {
            prompt: `You are a cloud security architect reviewing infrastructure.

Cloud Provider: [AWS/Azure/GCP]
Services Used: [EC2, S3, Lambda, etc.]

Security review checklist:
□ Identity and Access Management (IAM)
□ Storage bucket permissions
□ Network security groups
□ Encryption at rest and in transit
□ Logging and monitoring
□ Secrets management
□ Container security (if applicable)
□ Serverless security
□ API gateway configuration
□ Compliance posture

For each area:
- Current state assessment
- Misconfiguration risks
- Best practice recommendations
- Compliance mapping (CIS, PCI-DSS, etc.)`,
            category: "Cloud Security",
            technique: "Checklist + Best Practices"
        },
        {
            prompt: `As a cloud penetration tester, enumerate attack vectors in this environment.

Cloud Infrastructure: [Description]
Access Level: [What credentials/access you have]

Attack paths to explore:
1. Metadata service exploitation
2. Storage enumeration and exposure
3. Privilege escalation paths
4. Lateral movement opportunities
5. Data exfiltration methods
6. Persistence mechanisms

Document:
- Reconnaissance commands
- Exploitation techniques
- Post-exploitation activities
- Detection evasion considerations`,
            category: "Cloud Security",
            technique: "Offensive + Methodology"
        }
    ],
    api: [
        {
            prompt: `You are an API security specialist testing for vulnerabilities.

API Endpoint: [URL]
API Type: [REST/GraphQL/SOAP]
Authentication: [Method used]

Testing methodology:
1. Authentication/Authorization flaws
   - Broken object level authorization (BOLA/IDOR)
   - Broken function level authorization
   - Missing authentication

2. Data exposure
   - Excessive data exposure
   - Mass assignment
   - Sensitive data in URLs

3. Input validation
   - Injection attacks
   - Request smuggling
   - XML/JSON bombs

4. Rate limiting and resource management

5. Business logic flaws

For each test:
- Request examples
- Expected vs actual responses
- Security impact
- Remediation steps`,
            category: "API Testing",
            technique: "Structured + OWASP API Top 10"
        },
        {
            prompt: `Act as an API security auditor reviewing this GraphQL implementation.

GraphQL Endpoint: [URL]
Schema: [If available]

Security concerns specific to GraphQL:
1. Introspection enabled in production
2. Query depth/complexity limits
3. Batching attacks
4. Field suggestions information disclosure
5. Authorization at resolver level
6. N+1 query vulnerabilities
7. Denial of service via expensive queries

Testing approach:
- Schema enumeration
- Query fuzzing
- Authorization matrix testing
- Performance/DoS testing

Output: GraphQL-specific security report`,
            category: "API Testing",
            technique: "Technology-Specific + Deep Dive"
        }
    ],
    ctf: [
        {
            prompt: `You are a CTF player solving a web exploitation challenge.

Challenge Description:
[Paste challenge description]

URL: [Challenge URL if applicable]
Source Code: [If provided]

Problem-solving approach:
1. Analyze the challenge description for hints
2. Enumerate the application (features, input points, technologies)
3. Test for common vulnerabilities systematically
4. Review source code for logic flaws (if available)
5. Develop exploitation strategy
6. Extract flag

Think step-by-step and explain your reasoning for each attempt.
Document failed attempts and pivots.`,
            category: "CTF Challenges",
            technique: "Problem-Solving + Chain of Thought"
        },
        {
            prompt: `You are solving a CTF reverse engineering challenge.

Challenge: [Name]
File Type: [Binary, APK, .pyc, etc.]
Platform: [Linux/Windows/Android/etc.]

Analysis workflow:
1. File identification and metadata extraction
2. Static analysis approach
3. Dynamic analysis in controlled environment
4. Anti-debugging/anti-analysis detection
5. Key algorithm identification
6. Flag extraction methodology

Tools to consider:
- Disassemblers (Ghidra, IDA, radare2)
- Debuggers (gdb, x64dbg)
- Decompilers
- String analysis tools

Walk through your analysis process step by step.`,
            category: "CTF Challenges",
            technique: "Methodical + Tool-Based"
        },
        {
            prompt: `You are tackling a CTF cryptography challenge.

Challenge Details:
[Paste challenge information]

Ciphertext/Encrypted Data:
[If applicable]

Cryptanalysis approach:
1. Identify cipher type (frequency analysis, pattern recognition)
2. Check for classical ciphers (Caesar, Vigenère, substitution)
3. Test for modern crypto weaknesses (weak keys, bad implementations)
4. Analyze provided code for vulnerabilities
5. Apply known attacks (padding oracle, timing attacks, etc.)
6. Brute force considerations

Show your work including:
- Observations and hypotheses
- Test attempts with results
- Mathematical analysis
- Final solution method`,
            category: "CTF Challenges",
            technique: "Analytical + Exploratory"
        }
    ]
};

// Prompt engineering technique templates
const techniqueTemplates = {
    role: {
        template: `You are a [ROLE] with expertise in [DOMAIN].

[CONTEXT]

Your task is to [TASK].

Please provide [OUTPUT FORMAT].`,
        example: "You are a senior penetration tester with expertise in web application security.\n\nContext: Testing a financial services web application.\n\nYour task is to identify and exploit authentication vulnerabilities.\n\nPlease provide a detailed technical report with proof-of-concept."
    },
    stepbystep: {
        template: `Break down this security task into clear steps:

Task: [TASK DESCRIPTION]

Please provide:
1. [Step 1]
2. [Step 2]
3. [Step 3]
...

For each step include:
- Required tools
- Expected output
- Success criteria`,
        example: "Break down this security task into clear steps:\n\nTask: Identify all XSS vulnerabilities in a web application\n\nPlease provide:\n1. Input point enumeration\n2. Payload crafting\n3. Injection testing\n4. Impact assessment\n\nFor each step include tools, expected output, and success criteria."
    },
    context: {
        template: `Context: [DETAILED BACKGROUND]

Environment: [TECHNICAL ENVIRONMENT]
Constraints: [LIMITATIONS/BOUNDARIES]
Objective: [SPECIFIC GOAL]

Requirements:
- [Requirement 1]
- [Requirement 2]

Expected deliverable: [OUTPUT FORMAT]`,
        example: "Context: Performing authorized penetration test on e-commerce platform\n\nEnvironment: AWS-hosted, React frontend, Node.js backend\nConstraints: No destructive tests, business hours only\nObjective: Identify critical vulnerabilities before launch\n\nRequirements:\n- Maintain testing logs\n- Report findings immediately\n\nExpected deliverable: Executive summary + technical findings"
    },
    examples: {
        template: `Task: [DESCRIPTION]

Input example 1:
[Example input]
Expected output 1:
[Example output]

Input example 2:
[Example input]
Expected output 2:
[Example output]

Now analyze:
[Your actual input]`,
        example: "Task: Identify vulnerability type from description\n\nInput: User can view other users' data by changing ID parameter\nOutput: IDOR (Insecure Direct Object Reference) - Broken Access Control\n\nInput: Application accepts <script> tags in comments\nOutput: XSS (Cross-Site Scripting) - Injection vulnerability\n\nNow analyze:\nApplication crashes when sending 10000 char input"
    },
    constraints: {
        template: `Task: [TASK]

Constraints and boundaries:
✓ Allowed: [List permitted actions]
✗ Forbidden: [List prohibited actions]

Scope:
- In scope: [What to test]
- Out of scope: [What not to test]

Requirements:
[Specific requirements]

Rules:
[Any specific rules to follow]`,
        example: "Task: Web application security assessment\n\nConstraints:\n✓ Allowed: Authenticated testing, non-destructive scans\n✗ Forbidden: DoS attacks, data modification, social engineering\n\nScope:\n- In scope: *.example.com, staging.example.com\n- Out of scope: Production database, third-party APIs\n\nRules: Stop testing if critical vulnerability found"
    },
    chain: {
        template: `Problem: [PROBLEM DESCRIPTION]

Please solve this by:
1. Explaining your reasoning process
2. Showing your work step by step
3. Considering alternative approaches
4. Validating your conclusion

Think out loud and show:
- Initial observations
- Hypotheses formed
- Tests performed
- Results analysis
- Final conclusion`,
        example: "Problem: Web app returns different response times for valid vs invalid usernames\n\nPlease solve this by showing your reasoning:\n\n1. Initial observation: Timing difference detected\n2. Hypothesis: Username enumeration vulnerability\n3. Tests: Measure response times for known and unknown users\n4. Analysis: Consistent 200ms difference\n5. Conclusion: Timing attack enables user enumeration\n\nShow each step of your analysis."
    }
};

// Current state
let currentPrompt = '';
let currentMetadata = {};

// DOM Elements
const promptDisplay = document.getElementById('promptDisplay');
const metadataDisplay = document.getElementById('metadata');
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');
const categoryBtns = document.querySelectorAll('.category-btn');
const techniqueItems = document.querySelectorAll('.technique-item');
const buildCustomBtn = document.getElementById('buildCustomBtn');

// Event Listeners
generateBtn.addEventListener('click', generateRandomPrompt);
copyBtn.addEventListener('click', copyToClipboard);
buildCustomBtn.addEventListener('click', buildCustomPrompt);

categoryBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const category = btn.dataset.category;
        generateCategoryPrompt(category);
    });
});

techniqueItems.forEach(item => {
    item.addEventListener('click', () => {
        const technique = item.dataset.technique;
        showTechniqueTemplate(technique);
    });
});

// Functions
function generateRandomPrompt() {
    const categories = Object.keys(promptTemplates);
    const randomCategory = categories[Math.floor(Math.random() * categories.length)];
    const categoryPrompts = promptTemplates[randomCategory];
    const randomPrompt = categoryPrompts[Math.floor(Math.random() * categoryPrompts.length)];

    displayPrompt(randomPrompt.prompt, {
        category: randomPrompt.category,
        technique: randomPrompt.technique,
        type: 'Pre-built Template'
    });
}

function generateCategoryPrompt(category) {
    const categoryPrompts = promptTemplates[category];
    if (categoryPrompts && categoryPrompts.length > 0) {
        const randomPrompt = categoryPrompts[Math.floor(Math.random() * categoryPrompts.length)];
        displayPrompt(randomPrompt.prompt, {
            category: randomPrompt.category,
            technique: randomPrompt.technique,
            type: 'Category Template'
        });
    }
}

function showTechniqueTemplate(technique) {
    const template = techniqueTemplates[technique];
    if (template) {
        const displayText = `TEMPLATE:\n${'='.repeat(60)}\n${template.template}\n\n\nEXAMPLE:\n${'='.repeat(60)}\n${template.example}`;
        displayPrompt(displayText, {
            type: 'Technique Template',
            technique: technique.replace(/([A-Z])/g, ' $1').trim()
        });
    }
}

function buildCustomPrompt() {
    const role = document.getElementById('customRole').value.trim();
    const task = document.getElementById('customTask').value.trim();
    const context = document.getElementById('customContext').value.trim();
    const format = document.getElementById('customFormat').value.trim();

    if (!role && !task) {
        alert('Please fill in at least Role and Task fields');
        return;
    }

    let customPrompt = '';

    if (role) {
        customPrompt += `You are ${role.startsWith('a ') || role.startsWith('an ') ? role : 'a ' + role}.\n\n`;
    }

    if (context) {
        customPrompt += `Context: ${context}\n\n`;
    }

    if (task) {
        customPrompt += `Task: ${task}\n\n`;
    }

    if (format) {
        customPrompt += `Please provide the output as: ${format}`;
    }

    displayPrompt(customPrompt, {
        type: 'Custom Built',
        category: 'User Created'
    });

    // Clear form
    document.getElementById('customRole').value = '';
    document.getElementById('customTask').value = '';
    document.getElementById('customContext').value = '';
    document.getElementById('customFormat').value = '';
}

function displayPrompt(prompt, metadata = {}) {
    currentPrompt = prompt;
    currentMetadata = metadata;

    promptDisplay.textContent = prompt;
    promptDisplay.classList.remove('placeholder');
    promptDisplay.classList.add('updated');

    // Update metadata
    metadataDisplay.innerHTML = '';
    Object.entries(metadata).forEach(([key, value]) => {
        const span = document.createElement('span');
        span.textContent = `${key}: ${value}`;
        metadataDisplay.appendChild(span);
    });

    // Remove animation class after animation completes
    setTimeout(() => {
        promptDisplay.classList.remove('updated');
    }, 300);
}

function copyToClipboard() {
    if (!currentPrompt) {
        alert('No prompt to copy!');
        return;
    }

    navigator.clipboard.writeText(currentPrompt).then(() => {
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Copied!';
        copyBtn.classList.add('copied');

        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.classList.remove('copied');
        }, 2000);
    }).catch(err => {
        alert('Failed to copy: ' + err);
    });
}

// Bypass techniques handlers
const bypassBtns = document.querySelectorAll('.bypass-btn');
bypassBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const bypassType = btn.dataset.bypass;
        showBypassTechnique(bypassType);
    });
});

function showBypassTechnique(type) {
    if (!bypassTechniques) {
        displayPrompt('Bypass techniques module not loaded. Please refresh the page.', { type: 'Error' });
        return;
    }

    let techniques = [];
    switch(type) {
        case 'jailbreak':
            techniques = bypassTechniques.roleplay || [];
            break;
        case 'obfuscation':
            techniques = bypassTechniques.obfuscation || [];
            break;
        case 'context':
            techniques = bypassTechniques.contextManipulation || [];
            break;
        case 'technical':
            techniques = bypassTechniques.technicalFraming || [];
            break;
        case 'metadata':
            techniques = bypassTechniques.metadataHiding || [];
            break;
        case 'encoder':
            // Focus on encoder section
            document.getElementById('encoderInput').scrollIntoView({ behavior: 'smooth' });
            document.getElementById('encoderInput').focus();
            return;
    }

    if (techniques.length > 0) {
        const randomTechnique = techniques[Math.floor(Math.random() * techniques.length)];
        let displayText = `TECHNIQUE: ${randomTechnique.name || 'AI Bypass'}\n${'='.repeat(60)}\n`;
        if (randomTechnique.category) displayText += `Category: ${randomTechnique.category}\n`;
        if (randomTechnique.effectiveness) displayText += `Effectiveness: ${randomTechnique.effectiveness}\n`;
        if (randomTechnique.stealth) displayText += `Stealth Level: ${randomTechnique.stealth}\n`;
        if (randomTechnique.description) displayText += `\nDescription:\n${randomTechnique.description}\n`;
        displayText += `\n${'='.repeat(60)}\n\n${randomTechnique.prompt || randomTechnique.template}`;

        displayPrompt(displayText, {
            type: 'Bypass Technique',
            category: randomTechnique.category || type
        });
    }
}

// Text encoder/obfuscator
const encoderInput = document.getElementById('encoderInput');
const encoderOutput = document.getElementById('encoderOutput');
const encodeBtns = document.querySelectorAll('.encode-btn');
const copyEncodedBtn = document.getElementById('copyEncodedBtn');

encodeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const encodeType = btn.dataset.encode;
        encodeText(encodeType);
    });
});

copyEncodedBtn.addEventListener('click', () => {
    const text = encoderOutput.value;
    if (!text) {
        alert('No encoded text to copy!');
        return;
    }
    navigator.clipboard.writeText(text).then(() => {
        const originalText = copyEncodedBtn.textContent;
        copyEncodedBtn.textContent = '✓ Copied!';
        setTimeout(() => {
            copyEncodedBtn.textContent = originalText;
        }, 2000);
    });
});

function encodeText(type) {
    const input = encoderInput.value;
    if (!input) {
        alert('Please enter text to encode');
        return;
    }

    let output = '';
    switch(type) {
        case 'base64':
            output = btoa(input);
            break;
        case 'rot13':
            output = input.replace(/[a-zA-Z]/g, char => {
                const code = char.charCodeAt(0);
                const base = code >= 65 && code <= 90 ? 65 : 97;
                return String.fromCharCode(((code - base + 13) % 26) + base);
            });
            break;
        case 'leet':
            const leetMap = {
                'a': '4', 'A': '4',
                'e': '3', 'E': '3',
                'i': '1', 'I': '1',
                'o': '0', 'O': '0',
                's': '5', 'S': '5',
                't': '7', 'T': '7',
                'l': '1', 'L': '1',
                'g': '9', 'G': '9'
            };
            output = input.split('').map(char => leetMap[char] || char).join('');
            break;
        case 'reverse':
            output = input.split('').reverse().join('');
            break;
        case 'hex':
            output = Array.from(input).map(char =>
                char.charCodeAt(0).toString(16).padStart(2, '0')
            ).join('');
            break;
    }

    encoderOutput.value = output;
}

// Work tracking system
let workEntries = JSON.parse(localStorage.getItem('pentestWork') || '[]');

const addWorkBtn = document.getElementById('addWorkBtn');
const saveWorkBtn = document.getElementById('saveWorkBtn');
const exportWorkBtn = document.getElementById('exportWorkBtn');
const clearWorkBtn = document.getElementById('clearWorkBtn');
const workHistory = document.getElementById('workHistory');

addWorkBtn.addEventListener('click', addWorkEntry);
saveWorkBtn.addEventListener('click', saveWork);
exportWorkBtn.addEventListener('click', exportWork);
clearWorkBtn.addEventListener('click', clearWork);

function addWorkEntry() {
    const title = document.getElementById('workTitle').value.trim();
    const notes = document.getElementById('workNotes').value.trim();

    if (!title || !notes) {
        alert('Please fill in both project name and notes');
        return;
    }

    const entry = {
        id: Date.now(),
        title: title,
        notes: notes,
        timestamp: new Date().toISOString()
    };

    workEntries.unshift(entry);
    displayWorkHistory();

    // Clear inputs
    document.getElementById('workTitle').value = '';
    document.getElementById('workNotes').value = '';
}

function displayWorkHistory() {
    workHistory.innerHTML = '';
    workEntries.forEach(entry => {
        const entryDiv = document.createElement('div');
        entryDiv.className = 'work-entry';
        entryDiv.innerHTML = `
            <h4>${escapeHtml(entry.title)}</h4>
            <div class="timestamp">${new Date(entry.timestamp).toLocaleString()}</div>
            <div class="notes">${escapeHtml(entry.notes)}</div>
        `;
        workHistory.appendChild(entryDiv);
    });
}

function saveWork() {
    localStorage.setItem('pentestWork', JSON.stringify(workEntries));
    alert('Work saved to local storage!');
}

function exportWork() {
    if (workEntries.length === 0) {
        alert('No work entries to export');
        return;
    }

    let markdown = '# Penetration Testing Work Log\n\n';
    markdown += `Generated: ${new Date().toLocaleString()}\n\n`;
    markdown += '---\n\n';

    workEntries.forEach(entry => {
        markdown += `## ${entry.title}\n\n`;
        markdown += `**Date:** ${new Date(entry.timestamp).toLocaleString()}\n\n`;
        markdown += `**Notes:**\n\`\`\`\n${entry.notes}\n\`\`\`\n\n`;
        markdown += '---\n\n';
    });

    const blob = new Blob([markdown], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `pentest-work-${Date.now()}.md`;
    a.click();
    URL.revokeObjectURL(url);
}

function clearWork() {
    if (confirm('Are you sure you want to clear all work entries? This cannot be undone!')) {
        workEntries = [];
        localStorage.removeItem('pentestWork');
        displayWorkHistory();
        alert('All work entries cleared');
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize with a welcome message
window.addEventListener('load', () => {
    const welcomeMessage = `Welcome to the AI Security Prompt Generator!

This tool helps you create effective prompts for:
• Security testing and penetration testing
• CTF challenges and competitions
• AI bypass and jailbreaking techniques
• Security research and analysis
• Educational purposes

Features:
🎯 10 security categories with pre-built prompts
🔓 AI bypass techniques (jailbreaks, obfuscation, context manipulation)
🔐 Text encoder/obfuscator (Base64, ROT13, Hex, Leetspeak)
📝 Work tracking and documentation system
🛠️ Custom prompt builder

Get started by:
1. Clicking a category button for security-specific prompts
2. Trying the AI Bypass Techniques section for filter evasion
3. Using the Text Encoder to obfuscate your queries
4. Tracking your pentesting work with the Work Tracker
5. Building custom prompts with the Custom Builder

⚠️ IMPORTANT: For authorized testing, CTF, and educational use only!
Always obtain proper permission before conducting security assessments.

Linux Tool Installation:
Run: sudo bash install-tools.sh (to install pentesting tools)`;

    displayPrompt(welcomeMessage, {
        type: 'Welcome',
        version: '2.0'
    });

    // Load work history
    displayWorkHistory();
});
