# Test cases — how the policy was verified

Two methods were used in the project: **live login tests** (log in as the
intern user) and the **IAM Policy Simulator** (safer, non-disruptive).
Reproduce either one in your own AWS account.

## Setup recap

| Resource | Value |
|---|---|
| EC2 instances | 2× `t3.micro` in `eu-north-1` |
| Tags | `Env=development` (dev) / `Env=production` (prod) |
| Policy | `NextWorkDevEnvironmentPolicy` (see `NextWorkDevEnvironmentPolicy.json`) |
| Group | `nextwork-dev-group` (policy attached here) |
| User | intern user in that group (e.g. `nextwork-dev-*`) |
| Account alias | `nextwork-alias-lutendo` → `https://nextwork-alias-lutendo.signin.aws.amazon.com/console` |

## Live tests (as the intern user)

| # | Action attempted | Target | Expected | Observed |
|---|---|---|---|---|
| 1 | Sign in via alias URL | Console | Works; most panels hidden | ✅ Only EC2 (dev scope) visible |
| 2 | `StopInstances` | Production instance | **Denied** (tag ≠ development) | ✅ `AccessDenied` error |
| 3 | `StopInstances` | Development instance | **Allowed** | ✅ State → Stopping → Stopped |
| 4 | Create/Delete tags | Any instance | **Denied** (explicit Deny) | ✅ Blocked by statement 3 |

## Policy Simulator tests (no login / no real changes needed)

IAM → Policy Simulator → select the group/user → EC2 actions:

| Action | Expected | Observed |
|---|---|---|
| `ec2:StopInstances` | Allowed (for development-tagged scope) | ✅ `allowed — 1 matching statement` |
| `ec2:DeleteTags` | Denied | ✅ `denied — 1 matching statement` |

> Tip from the project: if the simulator says *denied* for an action you
> expected to pass, check the **resource tag context** first — the
> `Env=development` condition only matches instances that actually carry
> that tag. Tag the instance, then re-run the simulation.

## Local (no AWS needed)

```bash
python3 scripts/verify-policy.py
# OK: ... all policy checks passed
```

This validates the JSON structure and the three statements in CI
(`.github/workflows/validate-policy.yml`) on every push.
