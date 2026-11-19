# TECHNICAL THESIS REPORT — ASIR DEGREE PROJECT
## Deployment, Security Hardening and Cloud Infrastructure Automation on OCI

---

## 1. INTRODUCTION AND OBJECTIVES

### 1.1. Project Justification

This project exhaustively documents the architecture, hardening, service deployment and automation of a Linux server hosted on Oracle Cloud Infrastructure (OCI) under an ultra-optimized resource instance (VM.Standard.E2.1.Micro with 1GB RAM). The purpose is to demonstrate the technical ability to design, administer and secure a real production environment hosting an optimized web infrastructure, private network services via VPN and a continuous deployment pipeline adapted to heterogeneous devices.

### 1.2. Main Objectives

- Provision a cloud virtual machine (OCI) adapted to severe hardware constraints (1GB RAM).
- Implement advanced kernel-level adjustments, SWAP memory and TCP BBR congestion control.
- Apply a perimeter security and system hardening strategy (Hardening, UFW, Fail2Ban, Ed25519 keys and suppression of unnecessary services such as rpcbind).
- Configure a multi-site web server (Nginx) with WPO optimization (Gzip compression and static caching), automated HTTPS via Certbot and advanced SEO directives.
- Implement a private virtual network (WireGuard) with multi-peer isolation for secure traffic.
- Develop a hybrid CI/CD pipeline based on Python 3 to automate integration and deployment from mobile devices (iPadOS) and laptops (macOS).
- Manage project version control via Git and GitHub with credential sanitization.

---

## 2. PHASE 1: OS PROVISIONING AND OPTIMIZATION (OCI INFRASTRUCTURE)

- **Cloud Instance:** Provisioning of Ubuntu Server virtual machine on OCI with static public IP assignment and VCN (Virtual Cloud Network) addressing.
- **Swap Memory:** Creation and activation of a 2GB swapfile to mitigate critical intervention of the OOM Killer process due to physical RAM limitations.
- **TCP BBR Congestion Control:** Activation of Google's congestion control algorithm in the Linux kernel to maximize network flow performance.
- **Log Control and Rotation (Journald):** Strict limitation of system log retention to 200MB in `/etc/systemd/journald.conf` to prevent local storage saturation.

---

## 3. PHASE 2: HARDENING AND PERIMETER SECURITY (DEFENSE IN DEPTH)

- **SSH Service Hardening:** Modification of `/etc/ssh/sshd_config` absolutely disabling password authentication (`PasswordAuthentication no`) and forcing exclusive use of asymmetric cryptography based on Ed25519/RSA key pairs.
- **Brute Force Attack Mitigation:** Deployment and configuration of the Fail2Ban daemon for heuristic monitoring of access logs and automatic firewall bans.
- **Hybrid Firewall:** Layered configuration combining Security Lists and NSGs in the Oracle web console (Cloud Layer) with default deny policies implemented via UFW (Operating System Layer).
- **Socket Auditing and Surface Reduction:** Validation of listening port states via `ss -tulnp` and deactivation of unnecessary remote services not required in production (such as rpcbind on TCP/UDP port 111).

---

## 4. PHASE 3: NETWORKING AND VPN TUNNEL (WIREGUARD)

- **Private Virtual Network Deployment:** Installation and configuration of WireGuard operating directly on the Linux kernel space, listening on UDP port 51820 (previously opened in the OCI firewall).
- **Logical Subnet Definition:** Establishment of encrypted private addressing under the CIDR block `10.66.66.0/24`.
- **Multi-Peer Environment:** Configuration of isolated client profiles in `/etc/wireguard/wg0.conf` via public key routing (Cryptokey Routing), allowing concurrent and secure access from multiple devices (such as Mac workstations and mobile devices) without collisions in routing tables.

---

## 5. PHASE 4: MULTI-SITE ARCHITECTURE, WEB PERFORMANCE AND SEO (NGINX)

- **Web Server and Reverse Proxy:** Installation of Nginx to manage HTTP/HTTPS request routing.
- **Server Blocks:** Creation of host-name-oriented server blocks for the main domain (robertmesa.es) and subdomains (www), integrating `try_files` rewrite rules to support SPA (Single Page Application) web applications.
- **Automated TLS/SSL Encryption:** Implementation of Certbot (Let's Encrypt) for digital certificate issuance and permanent redirect (301) of insecure traffic from port 80 to port 443.
- **Web Performance Optimization (WPO):** Activation of the dynamic Gzip compression module (`gzip on`, `gzip_types`) and establishment of browser cache policies (`Cache-Control`, `expires 1y`) for static resources (JS, CSS, images, SVG).
- **Advanced SEO Optimization:** Injection of structured metadata in JSON-LD format, configuration of strict directives in robots.txt and sitemap structuring to facilitate crawling and indexing by search engines such as Googlebot.

---

## 6. PHASE 5: HYBRID CI/CD PIPELINE AND DEPLOYMENT AUTOMATION

Development of an autonomous continuous integration flow based on Python 3 scripting executed on the server (`deploy_server.py`) to update production environments without desktop computer dependency:

- **Dynamic Detection:** Heuristic monitoring at the user layer of compressed packages in `.zip` format transferred via secure SFTP channels.
- **Sandbox and Cleanup:** Extraction of content in an isolated temporary directory with automatic purging of unwanted metadata generated by other operating systems (such as `__MACOSX` folders).
- **Native Compilation:** Synchronous execution of dependencies with Node.js v20 LTS and packaging of production assets via modern build tools (`npm run build`).
- **Atomic Deployment:** Synchronous hot replacement of the production directory (`/var/www/danza`) minimizing any downtime.
- **Garbage Collection:** Automated and robust cleanup of temporary artifacts via structured exception blocks (`try/finally`), ensuring storage stability.

---

## SOURCE DOCUMENT

This Markdown file was generated from the original PDF `Memoria_Técnica_TFG.pdf` (4 pages, 71 KB) of the ASIR Final Degree Project. The original document was written in Spanish and has been translated to English for portfolio publication.
