# Troubleshooting

## 1. Intern can see everything / nothing in the console

IAM users only see what their group's policies allow. If the intern sees
no EC2, check: (a) the user is actually in `nextwork-dev-group`,
(b) the policy is attached to the **group** (not just created), and
(c) statement 2 (`ec2:Describe*`) is present — without it, the console
cannot even list instances.

## 2. "AccessDenied" when stopping the development instance

Most likely the instance is **not tagged** `Env=development` (check the
tag key spelling — it must be exactly `Env`, and the condition is
`ec2:ResourceTag/Env`). Tag it, wait a few seconds, retry. The Policy
Simulator has the same requirement: set the resource tag context there too.

## 3. Simulator says "denied" for an action you expected to pass

The simulator evaluates the tag condition against the resource you select.
If you simulate against a production-tagged instance (or no tag context),
`ec2:*` will not match. Select/set the `Env=development` context and
re-run. See `iam/test-cases.md`.

## 4. Intern could retag production as development (privilege escalation)

That is exactly what statement 3 prevents (`Deny ec2:CreateTags` /
`ec2:DeleteTags` on `*`). Explicit Deny beats Allow. If you remove
statement 3, the tag-based model collapses — never remove it without a
replacement control.

## 5. "Account alias already exists"

Aliases must be unique per AWS account. Pick a different alias
(e.g. append your name/numbers) in IAM → Account settings.

## 6. Lost the IAM user's console password

Passwords are shown **once** at creation. If lost, IAM → Users → your
user → Security credentials → *Reset console password* (the user must
change it at next sign-in). Never share the original password in chat,
email, or Git.

## 7. Policy JSON won't save

Common causes: trailing commas, single quotes instead of double quotes,
or a missing comma between statements. Validate locally first:

```bash
python3 scripts/verify-policy.py
```
