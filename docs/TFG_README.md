# OCI Cloud Infrastructure & CI/CD Automated Pipeline

## Project Summary

This repository documents the architecture, hardening and automation of a Linux server hosted on Oracle Cloud Infrastructure (OCI) (VM.Standard.E2.1.Micro instance).

The main objective of this project is to demonstrate the ability to design and manage an ultra-optimized resource environment (1GB RAM) with perimeter security, hosting a multi-site web architecture and a private VPN, fully managed through a hybrid CI/CD pipeline from mobile devices (iPadOS) and laptops (macOS).

## Technology Stack

- **Cloud Provider:** Oracle Cloud Infrastructure (OCI)
- **Operating System:** Ubuntu 20.04.6 LTS Linux (kernel 5.15.0-1081-oracle)
- **Web Server & Proxy:** Nginx
- **Security:** UFW, Fail2Ban, Asymmetric Cryptography (Ed25519/RSA), SSL/TLS (Let's Encrypt)
- **Networking:** WireGuard VPN, TCP BBR, DNS Management
- **CI/CD & Scripting:** Python 3, Bash, AppleScript, SFTP
- **Frontend:** React, Vite, Tailwind CSS 4

---

## Phase 1: OS Provisioning and Optimization

Given hardware constraints (1GB RAM), kernel-level adjustments were implemented to ensure stability:

- **SWAP Memory (2GB):** Created a swapfile to mitigate OOM Killer intervention.
- **TCP BBR Congestion Control:** Enabled Google's algorithm in the kernel to maximize bandwidth performance.
- **Log Control (Journald):** Log retention limit set to 200MB to prevent local storage degradation (`/etc/systemd/journald.conf`).

---

## Phase 2: Hardening and Perimeter Security

Implementation of a Defense in Depth strategy:

- **Password Authentication Disabled:** SSH access restricted to public key authentication only.
- **Fail2Ban:** Active with aggressive rules (5 attempts, 48h ban).
- **UFW Firewall:** Strict rules (ports 22, 80, 443, 51820 only).
- **WireGuard VPN:** Private network 10.66.66.0/24 for secure remote access.

---

## Phase 3: Multi-Site Web Architecture

Deployment of two independent websites on the same server:

- **robertmesa.es:** Main website (React/Vite/Tailwind) - `/var/www/danza`
- **cv.robertmesa.es:** Professional CV with embedded PDFs - `/var/www/html`

Both sites use Let's Encrypt certificates with automatic renewal via Certbot.

---

## Phase 4: OCI Network Troubleshooting

Resolution of common Oracle Cloud NSG (Network Security Group) issues:

- **Problem:** "Connection Timeout" despite open ports in UFW.
- **Solution:** Add ingress/egress rules in OCI Console → Virtual Cloud Network → Security Lists.
- **Required Rules:** TCP 22, 80, 443 / UDP 51820 (from 0.0.0.0/0).

---

## Phase 5: Hybrid CI/CD Pipeline (iPadOS → Ubuntu)

Implementation of a deployment workflow from mobile devices:

```
[iPad: ZIP Download] ➔ [Documents: SFTP Upload] ➔ [Termius: SSH Execution] ➔ [Server: Python Script (Decompression + Node v20 Build + Deployment + Cleanup)]
```

- **Server Script:** `deploy_server.py` - Detects ZIP, builds with Node v20, deploys to production.
- **Local Watcher (Mac):** `auto_deploy.py` - Monitors directory, automatic SFTP upload on file change.

---

## Phase 6: Automated Deployment

Two deployment modes:

1. **From Mac:** `auto_deploy.py` runs in daemon mode (watchdog), monitors for ZIP files, automatically builds and uploads via SFTP.
2. **From iPad:** Manual upload via SFTP + SSH execution of `deploy_server.py` through Termius.

---

## Phase 7: Recovery, Ubuntu Pro and Secure Patching

### Tailscale + Tailscale SSH
- Independent rescue route (does not depend on sshd).
- Banner: `SSH-2.0-Tailscale` (vs `OpenSSH_8.2p1 Ubuntu`).
- Tested from Mac and iPhone (mobile data).

### Backups
- Full backup: 628 MB (tar.gz with SHA256).
- Emergency SSH key (Ed25519) stored offline.
- Package freeze: `apt-mark hold linux-image-oracle`.

### Ubuntu Pro
- Enables `esm-infra` and `esm-apps` until 2030.
- 235 security updates available.

### Hardening Applied
- WireGuard config: `chmod 600`.
- Nginx security headers (HSTS, X-Content-Type-Options, etc.).
- Fail2Ban: 48h ban, Tailscale IP whitelisted.
- Journald: 192MB limit.

### Pending Tasks

| Task | Priority | Status |
|------|----------|--------|
| Disable X11Forwarding | Medium | ⏳ Pending |
| Change PermitRootLogin to no | High | ⏳ Pending |
| Add AllowUsers directive | High | ⏳ Pending |
| Kernel update with Tailscale active | Critical | ⏳ Pending |

---

## Security Notes

- **`shell=True`** in Python scripts: Required for npm, but increases risk. Validate inputs.
- **No automatic backups:** Manual process. Schedule with cron.
- **Tailscale SSH:** Independent rescue route. Keep active before modifying SSH/firewall.

---

## Verification Commands

```bash
# Check Tailscale status
sudo tailscale status

# Verify SSH banners
ssh -v roro-vpn-ts 2>&1 | grep SSH

# Check pending updates
pro security-status

# Check Fail2Ban status
sudo fail2ban-client status
```

---

## Repository Structure

```
oci-cloud-infrastructure/
├── README.md
├── 01_MEMO/
│   ├── Technical_Thesis_Report.pdf
│   └── Phase_7_Hardening_and_Recovery.md
├── 02_CODE_AND_CONFIG/
│   ├── nginx/
│   ├── python/
│   ├── ssh/
│   └── wireguard/
├── 03_EVIDENCE_AND_SCREENSHOTS/
└── docs/
```

---

## Author

**Robert Mesa**  
Full Stack Developer · ASIR

---

## License

MIT License - See LICENSE file for details.
