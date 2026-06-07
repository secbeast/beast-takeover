🐉 Beast‑Takeover
Stay Hungry. Stay Beastly. Hunt Down Subdomain Takeovers!

🚀 Overview
Beast‑Takeover is an advanced subdomain takeover scanner built for bug bounty hunters. It analyzes DNS records, HTTP/HTTPS responses, and provider fingerprints to detect dangling CNAMEs and takeover signatures with clean, professional output.

✨ Features
🔎 DNS Intelligence — Collects A, AAAA, CNAME, MX records

🌐 HTTP/HTTPS Scanning — Checks both protocols for accuracy

⚡ Async Recon — Fast parallel scanning with asyncio

🧬 Deep Fingerprinting — Detects provider via headers and body signatures

🎯 Confidence Scoring — Weighted scoring system for takeover probability

📂 Evidence Collection — JSON report with DNS, headers, body snippet

🛡 False Positive Reduction — Filters noise for clean results

✅ Provider Validation — Cross‑checks DNS + body fingerprints

🏆 High‑Value Asset Prioritization — Prioritizes sensitive subdomains like admin, api, secure


📦 Installation
bash
git clone https://github.com/yourname/beast-takeover.git
cd beast-takeover
pip3 install -r requirements.txt

🛠 Usage

python3 beast-takeover.py -l urls.txt
<img width="1480" height="642" alt="image" src="https://github.com/user-attachments/assets/12fdad65-08d7-45e6-a35d-1ac6445ad570" />

