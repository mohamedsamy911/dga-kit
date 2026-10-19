# Running the weekly freshness check from GitHub

design.dga.gov.sa answers only from Saudi Arabia. GitHub's runners are not in Saudi Arabia, so
they time out on TCP 443 (`diagnostics/2026-08-31-freshness-timeout.md`). The fix is a small
**forward proxy in Saudi Arabia** that the GitHub runner sends this one request through:

```
GitHub runner ──CONNECT design.dga.gov.sa:443──▶ proxy in KSA ──▶ design.dga.gov.sa
              (TLS stays end-to-end: the proxy sees the hostname, never the content)
```

**Running since 2026-10-18.** The proxy is an Oracle Linux 9 VM in Saudi Arabia running Squid.
Its firewall admits TCP 3128 only from GitHub Actions' IP ranges. The first hosted run that
reached DGA was [run 39164824587](https://github.com/mohamedsamy911/dga-kit/actions/runs/39164824587):
exit `0`, no change.

Until the `DGA_HTTPS_PROXY` secret exists, `.github/workflows/dga-freshness.yml` does not try
the check. Each run shows a warning that freshness was **not checked**. It does not fail.

## 1 · A machine in Saudi Arabia with a public IP

A small Linux VM is enough (1 vCPU, ~0.5 GB RAM; the proxy moves ~5 KB a quiet week). You can
use a VM in a Saudi cloud region, such as Oracle Cloud's Saudi regions (what runs today) or
Google Cloud Dammam. An office server with a static IP also works.

**Test reachability before you pay for it.** DGA's network may block some hosting providers.
From the machine itself:

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://design.dga.gov.sa   # want: 200
```

## 2 · Squid, locked to one destination

Oracle Linux 9 (on Ubuntu: `apt-get install -y squid apache2-utils`, helper path
`/usr/lib/squid/basic_ncsa_auth`):

```bash
sudo dnf install -y squid httpd-tools
sudo htpasswd -c /etc/squid/passwords kit          # choose a long random password
sudo chown root:squid /etc/squid/passwords && sudo chmod 640 /etc/squid/passwords
```

Replace `/etc/squid/squid.conf` with:

```
http_port 3128
auth_param basic program /usr/lib64/squid/basic_ncsa_auth /etc/squid/passwords
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
sudo systemctl enable --now squid
```

The proxy refuses every other destination, and it cannot cache inside a TLS tunnel.

## 3 · Admit only GitHub Actions

GitHub publishes the Actions runners' addresses at `api.github.com/meta`, key `actions`: about
5,500 IPv4 ranges, which change often. That is too many for a cloud security list (Oracle allows
about 200 rules per list). So open TCP 3128 to `0.0.0.0/0` in the cloud console, and let the
instance's firewall do the filtering with a set refreshed daily.

`/usr/local/bin/github-allowlist.sh` (firewalld, Oracle Linux 9):

```bash
#!/bin/sh
set -eu
curl -fsS https://api.github.com/meta | python3 -c 'import json,sys; print("\n".join(c for c in json.load(sys.stdin)["actions"] if ":" not in c))' > /tmp/gh.txt
[ "$(wc -l < /tmp/gh.txt)" -gt 1000 ] || exit 1          # never load a truncated list
{ echo '<?xml version="1.0" encoding="utf-8"?>'; echo '<ipset type="hash:net"><option name="maxelem" value="65536"/>'
  sed 's|.*|<entry>&</entry>|' /tmp/gh.txt; echo '</ipset>'; } > /etc/firewalld/ipsets/github.xml
firewall-cmd --reload
```

```bash
sudo chmod +x /usr/local/bin/github-allowlist.sh && sudo /usr/local/bin/github-allowlist.sh
sudo firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source ipset="github" port port="3128" protocol="tcp" accept'
sudo firewall-cmd --reload
echo '15 3 * * * root /usr/local/bin/github-allowlist.sh' | sudo tee /etc/cron.d/github-allowlist
```

Create the set before the rule that names it. **Never** also run `--add-port=3128/tcp`: it opens
the port to everyone and makes the rule above pointless. Check with
`sudo firewall-cmd --list-ports` (no `3128/tcp`) and `sudo firewall-cmd --list-rich-rules`.

**The allowlist is not authentication.** These are shared Azure addresses that every GitHub
user's workflows run from. The allowlist stops random internet scans; the password and the
one-host rule are still the protection.

**The proxy password crosses the internet in plain text.** Basic auth to an `http://` proxy is
not encrypted. Only the tunnel to DGA is. Python's `urllib`, which `sources.py` uses, cannot
speak TLS to a proxy, so this cannot be fixed by configuration. A stolen password still only
reaches `design.dga.gov.sa:443`, a public site, and only from GitHub's ranges. So:
- use a random password that guards nothing else;
- rotate it if you suspect a leak.

## 4 · Test

From the VM itself (firewalld does not filter local traffic). Quote the URL, since a password
may contain shell characters such as `(`:

```bash
curl -x 'http://kit:PASSWORD@127.0.0.1:3128' -sS -o /dev/null -w '%{http_code}\n' https://design.dga.gov.sa   # 200
curl -x 'http://kit:PASSWORD@127.0.0.1:3128' -sS -o /dev/null -w '%{http_code}\n' https://example.com          # 403
```

A test from your own machine is now dropped by the allowlist. That is expected.

## 5 · Give GitHub the proxy

Add it as a **repository** secret (Settings → Secrets and variables → Actions → *Repository
secrets*). An *environment* secret, such as one on `github-pages`, is invisible to this workflow,
and the run reports *not checked*.

```bash
gh secret set DGA_HTTPS_PROXY --repo mohamedsamy911/dga-kit     # paste http://kit:PASSWORD@PROXY_IP:3128
gh workflow run dga-freshness.yml --repo mohamedsamy911/dga-kit
```

A password with `(` or `)` needs no encoding. Encode `@ : / # %` (`@` → `%40`).

The secret reaches two steps: the probe, which only tests that it is set, and *Run the
sentinel*. GitHub masks it in logs, and it is not given to workflows from forks. Python's
`urllib` reads it from `HTTPS_PROXY`, so `sources.py` is unchanged.

## What the results mean

| Exit | Meaning |
|---|---|
| `0` | Checked through the proxy, no change against the baseline |
| `1` | Checked, DGA changed: the rolling review issue opens |
| `2` | **Not known**: proxy down, wrong password (`407`), blocked by the allowlist (timeout), or DGA unreachable. The job fails, and no issue is opened |

A proxy outage is never reported as "clean". Tested on 2026-10-18 through a local authenticated
CONNECT proxy:
- the right password exited `0`;
- a wrong password exited `2` (`Tunnel connection failed: 407`);
- a dead proxy exited `2`.

Neither failure printed the password.
