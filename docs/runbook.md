# OCI Linux Server Setup & Hardening Runbook

This repository contains the step-by-step deployment guide to configure, harden and optimize an Oracle Cloud Infrastructure (OCI) instance (VM.Standard.E2.1.Micro - 1GB RAM). The goal is to establish a solid and secure foundation for hosting lightweight web services (Nginx) and a WireGuard private network, overcoming Free Tier hardware limitations.

---

## Phase 1: System Preparation and Optimization

The initial instance has limited resources (1GB RAM). Memory and network management will be optimized before installing any services.

### 1.1 Base System Update

Ensure repositories and software are up to date:

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 SWAP Memory Configuration (2GB)

**Goal:** Prevent the system from killing processes due to lack of RAM (OOM Killer) by creating a paging file on disk.

**Execution:**

```bash
# 1. Create a 2GB file
sudo fallocate -l 2G /swapfile

# 2. Assign strict permissions (only root can read/write)
sudo chmod 600 /swapfile

# 3. Format the file as a swap partition
sudo mkswap /swapfile

# 4. Activate swap on the system
sudo swapon /swapfile

# 5. Make the change persistent by adding to fstab
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# 6. Verify it's active
sudo free -h
```

### 1.3 Network Acceleration (TCP BBR)

**Goal:** Enable Google's BBR algorithm in the Linux kernel to maximize bandwidth and reduce latency for VPN and web server.

**Execution:**

```bash
# 1. Add parameters to sysctl file
echo "net.core.default_qdisc=fq" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.tcp_congestion_control=bbr" | sudo tee -a /etc/sysctl.conf

# 2. Apply changes without reboot
sudo sysctl -p

# 3. Verify BBR is active
sysctl net.ipv4.tcp_congestion_control
# Expected: net.ipv4.tcp_congestion_control = bbr
```

### 1.4 Log Control (Journald)

**Goal:** Limit systemd journal log retention to 200MB to prevent storage degradation.

**Execution:**

```bash
# 1. Edit journald.conf
sudo nano /etc/systemd/journald.conf

# 2. Uncomment/modify these lines:
SystemMaxUse=200M
SystemKeepFree=1G

# 3. Restart journald
sudo systemctl restart systemd-journald
```

---

## Phase 2: SSH Hardening and Fail2Ban

### 2.1 Disable Password Authentication

**Goal:** Allow only public key authentication.

**Execution:**

```bash
# 1. Edit SSH config
sudo nano /etc/ssh/sshd_config

# 2. Modify these values:
PasswordAuthentication no
PermitEmptyPasswords no
ChallengeResponseAuthentication no

# 3. Validate config before restarting
sudo sshd -t

# 4. Restart SSH
sudo systemctl restart sshd
```

### 2.2 Fail2Ban Installation and Configuration

**Goal:** Protect SSH from brute force attacks.

**Execution:**

```bash
# 1. Install Fail2Ban
sudo apt install fail2ban -y

# 2. Create local jail config
sudo nano /etc/fail2ban/jail.local

# 3. Add this content:
[DEFAULT]
bantime = 48h
findtime = 10m
maxretry = 5
ignoreip = 127.0.0.1/8

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
bantime = 48h

# 4. Restart Fail2Ban
sudo systemctl restart fail2ban

# 5. Check status
sudo fail2ban-client status sshd
```

### 2.3 UFW Firewall Configuration

**Goal:** Allow only necessary ports (22, 80, 443, 51820).

**Execution:**

```bash
# 1. Install UFW
sudo apt install ufw -y

# 2. Set default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. Allow required ports
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 51820/udp # WireGuard

# 4. Enable UFW
sudo ufw enable

# 5. Check status
sudo ufw status verbose
```

---

## Phase 3: Nginx and WireGuard

### 3.1 Nginx Installation and Multi-Site Setup

**Goal:** Host multiple websites on the same server.

**Execution:**

```bash
# 1. Install Nginx
sudo apt install nginx -y

# 2. Create document roots
sudo mkdir -p /var/www/danza
sudo mkdir -p /var/www/html

# 3. Set permissions
sudo chown -R www-data:www-data /var/www
sudo chmod -R 755 /var/www

# 4. Create server blocks (see nginx/danza.conf and nginx/cv.conf)
sudo nano /etc/nginx/sites-available/danza
sudo nano /etc/nginx/sites-available/cv

# 5. Enable sites
sudo ln -s /etc/nginx/sites-available/danza /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/cv /etc/nginx/sites-enabled/

# 6. Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### 3.2 WireGuard VPN Setup

**Goal:** Create a private network for secure remote access.

**Execution:**

```bash
# 1. Install WireGuard
sudo apt install wireguard -y

# 2. Generate keys
cd /etc/wireguard
wg genkey | tee privatekey | wg pubkey > publickey

# 3. Create wg0.conf (see wireguard/wg0.conf)
sudo nano /etc/wireguard/wg0.conf

# 4. Set strict permissions
sudo chmod 600 /etc/wireguard/wg0.conf

# 5. Enable WireGuard
sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

# 6. Check status
sudo wg show
```

---

## Phase 4: Troubleshooting

### Connection Timeout

**Problem:** Ports open in UFW but still unreachable.

**Cause:** OCI Network Security Groups (NSG) block traffic at the VCN level.

**Solution:**

1. Go to OCI Console → Virtual Cloud Network → Security Lists.
2. Add ingress rules:
   - TCP 22, 80, 443 (from 0.0.0.0/0)
   - UDP 51820 (from 0.0.0.0/0)
3. Add egress rules (allow all traffic).

### WireGuard Handshake Issues

**Problem:** "Handshake did not complete after X seconds".

**Causes:**
- UDP 51820 blocked in OCI NSG.
- Wrong public key on client.
- NAT issues.

**Solution:**
1. Verify NSG rules (see above).
2. Regenerate keys and redistribute configs.
3. Check `AllowedIPs` on client config.

---

## Verification Commands

```bash
# Check system resources
free -h
df -h

# Check active services
systemctl status nginx fail2ban wg-quick@wg0

# Check open ports
sudo ss -tulpn

# Check SSL certificates
sudo certbot certificates
```

---

## Related Documentation

- [TFG_README.md](TFG_README.md) - Complete project summary
- [SUBDOMAINS.md](SUBDOMAINS.md) - DNS and SSL configuration
