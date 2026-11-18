# Phase 7 — Access Recovery, Ubuntu Pro and Secure Patching

## 1. Context and Main Restriction

- Server: Oracle Cloud, `roro-vpn`, Ubuntu 20.04.6 LTS, kernel `5.15.0-1081-oracle`, uptime 249 days, 952 MB RAM, 45 GB disk.
- Ubuntu 20.04 standard support ended on 05/31/2025. `pro security-status` reported 216 pending updates from `esm-infra` + 19 from `esm-apps`, including kernel, OpenSSH, OpenSSL, sudo, glibc, systemd, nginx.
- Server is managed remotely; during this process no serial console or reboot was used.
- **Adopted restriction:** freeze SSH, firewall and reboot until verifying Tailscale as an independent access route. No changes to `sshd_config`, port 22, or UFW/iptables.

## 2. Safety Net: Tailscale + Tailscale SSH

### Installation
```bash
curl -fsSL https://tailscale.com/install.sh -o /tmp/tailscale-install.sh
sudo sh /tmp/tailscale-install.sh
sudo systemctl enable --now tailscaled
sudo tailscale up --accept-dns=false
```
- `--accept-dns=false`: Tailscale does NOT modify server DNS.
- IP in tailnet: `<TAILSCALE_IP>`. MagicDNS: `<TAILSCALE_HOSTNAME>`.

### Tailscale SSH Activation (independent door from sshd)
```bash
sudo tailscale up --ssh --accept-dns=false
```
- Connection handled by `tailscaled`, not `sshd`. Verified: SSH banner `SSH-2.0-Tailscale` (vs `OpenSSH_8.2p1 Ubuntu`).
- Tested from Mac and iPhone (with Wi-Fi off, via mobile data).
- SSH alias added to `~/.ssh/config`: `ssh roro-vpn-ts`.

### Tailscale Account Hardening
- MFA via Apple ID (2FA).
- Device approval enabled for new devices.
- Server key expiration disabled (expired 05/05/2027).
- Recommended ACL for emergencies: `"action": "accept", "users": ["autogroup:members"], "ports": ["*:*"]`.

## 3. Backups and Recovery Keys

### Full Backup
```bash
sudo tar -czvf /root/backup_full_$(date +%Y%m%d).tar.gz \
  /etc/nginx /etc/letsencrypt /etc/fail2ban /etc/wireguard \
  /etc/ssh /etc/ufw /var/www /home/ubuntu
```
- Size: 628 MB. SHA256: `<HASH>`.
- Stored locally and in cloud (Google Drive).

### Emergency SSH Key
```bash
ssh-keygen -t ed25519 -f /root/emergency_key -N ""
```
- Public key added to `/root/.ssh/authorized_keys`.
- Private key stored offline (USB + printed paper).

### Package Freeze
```bash
sudo apt-mark hold linux-image-oracle linux-headers-oracle
```
- Prevents accidental kernel updates that could break boot.

## 4. Ubuntu Pro and ESM

### Activation
```bash
sudo pro attach <TOKEN>
```
- Enables `esm-infra` and `esm-apps` until 2030.
- 235 security updates available.

### Selective Patching
```bash
sudo apt update
sudo apt upgrade --only-upgrade openssh-server openssl sudo
```
- Critical packages updated first.
- Kernel deferred until Tailscale verification.

## 5. Hardening Applied

### File Permissions
```bash
sudo chmod 600 /etc/wireguard/wg0.conf
sudo chmod 600 /etc/ssh/sshd_config
```

### Nginx Security Headers
- Added `security-headers.conf` with HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy.

### Fail2Ban Tuning
```ini
[DEFAULT]
bantime = 48h
findtime = 10m
maxretry = 5
ignoreip = 127.0.0.1/8 <TAILSCALE_IP>/32
```
- Bans for 48 hours.
- Tailscale IP whitelisted to avoid lockout.

### Journal Control
```bash
sudo journalctl --vacuum-size=192M
```
- Logs limited to 192 MB.

## 6. Pending Tasks Table

| Task | Priority | Status |
|------|----------|--------|
| Disable X11Forwarding | Medium | ⏳ Pending |
| Change PermitRootLogin to no | High | ⏳ Pending |
| Add AllowUsers directive | High | ⏳ Pending |
| Kernel update with Tailscale active | Critical | ⏳ Pending |
| Disable IPv6 if unused | Low | ⏳ Pending |

## 7. Security Notes

- **Never modify SSH/firewall without Tailscale active.**
- **Test recovery from external network (mobile data).**
- **Keep emergency key offline and updated.**
- **Review Fail2Ban logs weekly.**

## 8. Final Verification Commands

```bash
# Check Tailscale status
sudo tailscale status

# Verify SSH banners
ssh -v roro-vpn-ts 2>&1 | grep SSH

# Check pending updates
pro security-status

# Verify backups
sha256sum /root/backup_full_*.tar.gz

# Check Fail2Ban status
sudo fail2ban-client status
```

---

**Conclusion:** Tailscale provides an independent rescue route. Ubuntu Pro extends security support to 2030. Hardening applied without compromising access.
