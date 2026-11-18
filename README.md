# OCI Cloud Infrastructure & CI/CD Automated Pipeline

Final work repository: infrastructure, hardening and automation of a Linux server on Oracle Cloud Infrastructure (OCI).

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](#license)

---

## Project Summary

Documents the architecture, hardening and automation of a Linux server hosted on OCI (VM.Standard.E2.1.Micro instance, 1 GB RAM), with multi-site web architecture (robertmesa.es + cv.robertmesa.es), private VPN (WireGuard) and hybrid CI/CD pipeline from iPadOS/macOS.

**Stack:** OCI · Ubuntu 20.04.6 LTS · Nginx · Fail2Ban · WireGuard · Let's Encrypt · Python 3 · Node.js v20 · React/Vite/Tailwind · Tailscale

---

## Repository Structure

```
oci-cloud-infrastructure/
├── README.md
├── .gitignore
├── 01_MEMO/
│   ├── Memoria_Técnica_TFG.pdf          # Technical thesis report
│   └── Phase_7_Hardening_and_Recovery.md  # Hardening, Ubuntu Pro, Tailscale
├── 02_CODE_AND_CONFIG/
│   ├── nginx/
│   │   ├── danza.conf                   # robertmesa.es vhost (with security headers)
│   │   ├── cv.conf                      # cv.robertmesa.es vhost (professional CV)
│   │   └── security-headers.conf        # HSTS, X-Content-Type-Options, etc.
│   ├── python/
│   │   ├── setup_server.sh              # Interactive instance replicator
│   │   ├── deploy_server.py             # Automatic deployment on server (from ZIP)
│   │   ├── auto_deploy.py               # Mac watcher (watchdog + SFTP + AppleScript)
│   │   ├── despliegue.py                # Incremental deployment (only new/modified files)
│   │   ├── explaining_auto_deploy.py.txt
│   │   └── explaining_autodeploy_on_ios.txt
│   ├── ssh/
│   │   ├── sshd_config    
│   │   └── EFFECTIVE_CONFIG_NOTE.md
│   └── wireguard/
│       └── wg0.conf                     # WireGuard server configuration
├── 03_EVIDENCE_AND_SCREENSHOTS/
│   ├── tailscale_admin_panel.png
│   ├── active_ports.png
│   ├── fail2ban_status.png
│   ├── ssh_remote_access.png
│   ├── nginx_service.png
│   ├── nginx_syntax.png
│   ├── htop_resource_monitoring.png
│   ├── fail2ban_bans.png
│   ├── fail2ban_rules.png
│   ├── wireguard_status.png
│   └── diagram.png
└── docs/
    ├── SUBDOMAINS.md
    ├── TFG_README.md
    └── runbook.md
```

---

## Main Features

### 🔐 Security
- **SSH Hardening:** Key-based authentication only, Fail2Ban active
- **Perimeter Firewall:** UFW with strict rules (22, 80, 443, 51820)
- **Private VPN:** WireGuard for secure remote access
- **Rescue Access:** Tailscale SSH (independent of sshd)
- **SSL/TLS:** Let's Encrypt certificates with automatic renewal

### 🚀 CI/CD
- **Hybrid Pipeline:** Development on iPadOS/macOS → Deployment on Ubuntu
- **Automatic Deployment:** Python scripts with SFTP + watchdog
- **Incremental Synchronization:** Only modified files are uploaded
- **Local Build:** npm run build before deployment

### 🌐 Multi-site Architecture
- **robertmesa.es:** Main website (React/Vite/Tailwind)
- **cv.robertmesa.es:** Professional CV with embedded PDFs
- **IP Access:** Disabled (404) for security

### ⚙️ Optimization
- **TCP BBR:** Google congestion algorithm for better bandwidth
- **SWAP 2GB:** Prevents OOM Killer on 1GB RAM instance
- **Log Control:** Journald limited to 200MB

---

## Quick Start

### Prerequisites
- Oracle Cloud account (Free Tier)
- Domain with DNS configured
- SSH keys (Ed25519 or RSA 4096+)

### Initial Setup
1. Clone the repository
2. Run `setup_server.sh` on the server
3. Configure DNS records
4. Deploy your websites

### Daily Deployment
- **From Mac:** Use `auto_deploy.py` (watchdog mode)
- **From iPad:** Upload ZIP via SFTP + execute `deploy_server.py`

---

## Documentation

- **[TFG_README.md](docs/TFG_README.md):** Complete project summary
- **[SUBDOMAINS.md](docs/SUBDOMAINS.md):** DNS and SSL configuration
- **[runbook.md](docs/runbook.md):** Step-by-step setup guide
- **[Phase_7_Hardening_and_Recovery.md](01_MEMO/Phase_7_Hardening_and_Recovery.md):** Security and recovery

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Author

**Robert Mesa**  
Full Stack Developer · ASIR

---

## Support

If you find this project useful, consider:
- ⭐ Starring this repository
- 📝 Sharing your experience
- 🔧 Contributing improvements
