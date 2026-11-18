# Note: Effective SSH Configuration on Server

The `sshd_config` file in this folder is the reference copy of the base `/etc/ssh/sshd_config`.
The effective configuration is supplemented by `/etc/ssh/sshd_config.d/60-cloudimg-settings.conf`, which contains the actually applied values:

- `PasswordAuthentication no`
- `KbdInteractiveAuthentication no`
- `PermitEmptyPasswords no`
- `PermitRootLogin without-password`
- `X11Forwarding yes`
- `ChallengeResponseAuthentication no`
- `UsePAM yes`

Highlighted values:
- No `AllowUsers` (pending to add in hardening phase).
- `X11Forwarding yes` (pending to disable).
- `PermitRootLogin without-password` (pending to change to `no`).

The server's public key (Ed25519 host key) is:
`<HOST_KEY_FINGERPRINT>`

During Phase 7, `sshd_config` and port 22 were NOT modified.
The rescue route is Tailscale SSH (`ssh roro-vpn-ts`), which does not depend on `sshd`.
