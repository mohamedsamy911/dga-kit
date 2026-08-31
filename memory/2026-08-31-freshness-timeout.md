# Debug report: hosted freshness checks cannot connect to DGA

- **Status: BLOCKED on hosted network reachability.** Reporting fixes are verified, but the
  source remains unreachable from the tested GitHub-hosted runners. The diagnostic branch is
  not a completed connectivity fix and has not been merged into `master`.
- **Symptom:** the [scheduled run](https://github.com/mohamedsamy911/dga-kit/actions/runs/33393214364)
  exited 2 after its first request timed out. Rerunning its failed job also failed.
- **Root cause established:** the runner cannot establish TCP port 443 to `design.dga.gov.sa`.
  DNS resolves to the same address locally and on both hosted runners. Python and curl both
  time out before TLS or an HTTP response. The precise network policy or routing cause is
  unknown; there is no evidence establishing geoblocking or a particular firewall rule.
- **Evidence:** the [Ubuntu diagnostic run](https://github.com/mohamedsamy911/dga-kit/actions/runs/33433754189)
  showed IPv4 TCP/TLS times of zero before connection timeout. The
  [macOS diagnostic run](https://github.com/mohamedsamy911/dga-kit/actions/runs/33434810114)
  showed the same failure and exhausted all three attempts. The identical Python GET succeeded
  locally with HTTP 200 and 4,417 bytes in 0.52 seconds during the macOS experiment.
- **Verified code changes:** `harvest/sources.py` retries only transient timeout/connection
  failures, at most three times with 5s/10s pauses. Exhaustion still exits 2. The workflow captures
  stderr, reports freshness as unknown when incomplete, and uploads only diagnostics on failure
  instead of presenting the committed report as current. No baseline or TLS behavior changed.
- **Regression tests:** `evals/test-automation.py` exercises actual Bash workflow scripts for
  exits 0/1/2 and missing results, downstream exit outputs, log capture, artifact conditions,
  retry recovery/exhaustion, and immediate HTTP/DNS/certificate failures. Its previous fetch
  mock leak is repaired; offline scenarios cannot write the repository's freshness report.
- **Break-tests:** disabling retries, removing stderr capture, mislabelling failed summaries,
  uploading reports unconditionally, and publishing the wrong exit output each caused their
  intended checks to fail. The marketplace fixture also rejects a wrong published branch while
  accepting feature/detached checkouts; it previously incorrectly inspected the current HEAD.
- **Validation:** all eleven `AGENTS.md` checks and Codex's plugin validator pass. Regenerated
  token files and `harvest/FRESHNESS.md` remain unchanged. The failed macOS run successfully
  uploaded its diagnostic artifact; its monitor step remained failed, as required.
- **Cleanup:** the temporary DNS/curl probe was removed and `ubuntu-latest` restored. Switching
  runners did not fix connectivity, so the experiment is not retained as a proposed solution.
- **Next decision:** obtain network-owner guidance or choose an approved execution environment
  that can reach DGA. A self-hosted runner needs an explicit security/deployment decision,
  especially for a public repository. Do not hide exit 2, accept a new baseline, disable TLS,
  or treat these failed checks as evidence that the DGA guidance is current.
