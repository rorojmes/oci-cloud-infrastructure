# Subdomains and Deployed Websites

## ✅ Active Sites

### 1. robertmesa.es (Main)
- **URL:** https://robertmesa.es
- **Document Root:** `/var/www/danza`
- **Nginx Config:** `02_CODE_AND_CONFIG/nginx/danza.conf`
- **Certificate:** Let's Encrypt (automatic renewal)
- **Status:** ✅ Production

### 2. cv.robertmesa.es (Professional CV)
- **URL:** https://cv.robertmesa.es
- **Document Root:** `/var/www/html`
- **Nginx Config:** `02_CODE_AND_CONFIG/nginx/cv.conf`
- **Certificate:** Let's Encrypt (automatic renewal)
- **Content:** Interactive CV with embedded PDFs (PDF.js)
- **Status:** ✅ Production

### 3. IP Access (Legacy)
- **URL:** http://130.162.60.196
- **Behavior:** Returns 404 (Access not allowed by IP)
- **Status:** ✅ Disabled for security

---

## 📋 DNS Configuration

| Subdomain | Type | Value | TTL |
|------------|------|-------|-----|
| `@` (robertmesa.es) | A | 130.162.60.196 | 3600 |
| `www` | A | 130.162.60.196 | 3600 |
| `cv` | A | 130.162.60.196 | 3600 |

**DNS Provider:** dns-parking.com

---

## 🔒 SSL/TLS Certificates

All certificates are managed by **Certbot** (Let's Encrypt) with automatic renewal every 90 days.

```bash
# View installed certificates
sudo certbot certificates

# Renew all certificates
sudo certbot renew --dry-run

# Force renewal of a specific domain
sudo certbot renew --cert-name cv.robertmesa.es --force-renewal
```

### Current Certificates

| Domain | Expiration | Status |
|---------|------------|--------|
| robertmesa.es, www.robertmesa.es | 2027-02-06 | ✅ Valid |
| cv.robertmesa.es | 2027-02-14 | ✅ Valid |

---

## 🚀 CV Subdomain Deployment

### Automatic Script (Certbot)

```bash
#!/usr/bin/env bash
# setup-cv-subdomain.sh

DOMAIN="robertmesa.es"
SUBDOMAIN="cv"
EMAIL="tu_email@ejemplo.com"

# Create document root
sudo mkdir -p /var/www/html
sudo chown -R www-data:www-data /var/www/html
sudo chmod 755 /var/www/html

# Obtain certificate
sudo certbot certonly --webroot -w /var/www/html \
  -d ${SUBDOMAIN}.${DOMAIN} \
  --email ${EMAIL} \
  --agree-tos --non-interactive

# Create Nginx config (see cv.conf)
sudo nano /etc/nginx/sites-available/cv.conf

# Enable site
sudo ln -s /etc/nginx/sites-available/cv.conf /etc/nginx/sites-enabled/

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

---

## 📂 Website Structure

```
/var/www/
├── html/                    # cv.robertmesa.es
│   ├── index.html
│   ├── assets/
│   └── pdf/
└── danza/                   # robertmesa.es
    ├── index.html
    ├── assets/
    └── pdf/
```

---

## 🔧 Useful Commands

```bash
# Check Nginx syntax
sudo nginx -t

# View Nginx logs
sudo tail -f /var/log/nginx/error.log

# Check SSL expiration
sudo certbot certificates

# Force HTTPS redirect test
curl -I http://cv.robertmesa.es
```

---

## 🛡️ Security Headers

All sites include the following headers (see `security-headers.conf`):

- `Strict-Transport-Security`: HSTS enabled (1 year, includeSubDomains)
- `X-Content-Type-Options`: nosniff
- `X-Frame-Options`: SAMEORIGIN
- `Referrer-Policy`: strict-origin-when-cross-origin

---

## 📊 Architecture Diagram

```
                    ┌─────────────────┐
                    │   OCI NSG       │
                    │  (Firewall)     │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Oracle Cloud   │
                    │  Instance       │
                    │  130.162.60.196 │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────┐ ┌───────▼──────┐ ┌────▼─────┐
     │   Nginx     │ │   Nginx      │ │ WireGuard│
     │ :443 (SSL)  │ │   :443 (SSL) │ │ :51820   │
     │ robertmesa  │ │ cv.robert... │ │  VPN     │
     │     .es     │ │     .es      │ │          │
     └─────────────┘ └──────────────┘ └──────────┘
```

---

## 📝 Implementation Notes

1. **IPv6:** Enabled but not used for DNS records.
2. **Cache:** Static assets cached for 1 year (`Cache-Control: public, no-transform, immutable`).
3. **Gzip:** Enabled for text, CSS, JS, SVG, JSON.
4. **SPA Fallback:** `try_files $uri $uri/ /index.html` for client-side routing.
5. **IP Access:** Returns 404 to prevent direct IP access.

---

## 🔗 Related Documentation

- [TFG_README.md](TFG_README.md) - Complete project summary
- [runbook.md](runbook.md) - Step-by-step setup guide
