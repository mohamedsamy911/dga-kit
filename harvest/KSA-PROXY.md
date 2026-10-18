# Running the weekly freshness check from GitHub

design.dga.gov.sa answers only from Saudi Arabia. GitHub's runners are not in Saudi Arabia, so
they time out on TCP 443 (`diagnostics/2026-08-31-freshness-timeout.md`). The fix is a small
**forward proxy in Saudi Arabia** that the GitHub runner sends this one request through:

```
GitHub runner ──CONNECT design.dga.gov.sa:443──▶ proxy in KSA ──▶ design.dga.gov.sa
              (TLS stays end-to-end: the proxy sees the hostname, never the content)
```

Until the `DGA_HTTPS_PROXY` secret exists, `.github/workflows/dga-freshness.yml` does not try
the check. Each run shows a warning that freshness was **not checked**. It does not fail.

## 1 · A machine in Saudi Arabia with a public IP

A small Linux VM is enough (1 vCPU, ~0.5 GB RAM; the proxy moves ~5 KB a quiet week). You can
use a VM in a Saudi cloud region, such as Google Cloud Dammam or Oracle Cloud Jeddah. An office
server with a static IP also works.

**Test reachability before you pay for it.** DGA's network may block some hosting providers.
From the machine itself:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://design.dga.gov.sa   # want: 200
```

## 2 · Squid, locked to one destination

```bash
sudo apt-get install -y squid apache2-utils
sudo htpasswd -c /etc/squid/passwords kit          # choose a long random password
```

Replace `/etc/squid/squid.conf` with:

```
http_port 3128
auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwords
auth_param basic realm dga-kit
acl kit proxy_auth REQUIRED
acl dga dstdomain design.dga.gov.sa
acl tls port 443
acl CONNECT method CONNECT
http_access deny !kit
http_access allow CONNECT dga tls
http_access deny all
cache deny all
```

```bash
sudo systemctl restart squid
```

Open **TCP 3128 only** in the firewall or cloud security group. GitHub's runner addresses cover
too much of Azure to allowlist, so the password and the one-host rule are the protection. The
proxy refuses every other destination, and it cannot cache inside a TLS tunnel.

**The proxy password crosses the internet in plain text.** Basic auth to an `http://` proxy is
not encrypted. Only the tunnel to DGA is. Python's `urllib`, which `sources.py` uses, cannot
speak TLS to a proxy, so this cannot be fixed by configuration. A stolen password still only
reaches `design.dga.gov.sa:443`, a public site. So:
- use a random password that guards nothing else;
- rotate it if you suspect a leak.

If that bound is not acceptable, use a Tailscale exit node instead: the tunnel to it is
encrypted, at the cost of an OAuth client and a GitHub Action in the workflow.

## 3 · Test from outside

```bash
curl -x http://kit:PASSWORD@PROXY_IP:3128 -sS -o /dev/null -w '%{http_code}\n' https://design.dga.gov.sa   # 200
curl -x http://kit:PASSWORD@PROXY_IP:3128 -sS -o /dev/null -w '%{http_code}\n' https://example.com          # 403
```

## 4 · Give GitHub the proxy

```bash
gh secret set DGA_HTTPS_PROXY --repo mohamedsamy911/dga-kit --body 'http://kit:PASSWORD@PROXY_IP:3128'
gh workflow run dga-freshness.yml --repo mohamedsamy911/dga-kit
```

The secret reaches two steps: the probe, which only tests that it is set, and *Run the
sentinel*. GitHub masks it in logs, and it is not
given to workflows from forks. Python's `urllib` reads it from `HTTPS_PROXY`, so `sources.py` is
unchanged.

## What the results mean

| Exit | Meaning |
|---|---|
| `0` | Checked through the proxy, no change against the baseline |
| `1` | Checked, DGA changed: the rolling review issue opens |
| `2` | **Not known**: proxy down, wrong password (`407`), or DGA unreachable. The job fails, and no issue is opened |

A proxy outage is never reported as "clean". Tested on 2026-10-18 through a local authenticated
CONNECT proxy:
- the right password exited `0`;
- a wrong password exited `2` (`Tunnel connection failed: 407`);
- a dead proxy exited `2`.

Neither failure printed the password.
