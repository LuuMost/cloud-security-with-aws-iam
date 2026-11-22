# NextWorkDevEnvironmentPolicy — explained

Source: `NextWorkDevEnvironmentPolicy.json` (reproduced exactly from the
project's Policy editor screenshot). Attached to the **nextwork-dev-group**
IAM user group, so every intern user in that group inherits it.

## The 4 building blocks of every statement

| Element | Meaning |
|---|---|
| **Effect** | `Allow` or `Deny` — whether the statement grants or blocks the action |
| **Action** | What the holder can/cannot do (e.g. `ec2:StopInstances`) |
| **Resource** | Which AWS resources the statement applies to (`*` = all) |
| **Condition** | Extra rules that must be true (here: the instance's `Env` tag) |

> **Explicit Deny always wins** over any Allow. That is why statement 3 can
> block tag changes even though statement 1 allows `ec2:*`.

## Statement by statement

### 1. Full EC2 control — development instances only
```json
{ "Effect": "Allow", "Action": "ec2:*", "Resource": "*",
  "Condition": { "StringEquals": { "ec2:ResourceTag/Env": "development" } } }
```
Interns can start/stop/terminate etc. **only** instances tagged
`Env = development`. Production instances (`Env = production`) are outside
this statement, so the same actions are implicitly denied there.

### 2. Read-only visibility everywhere
```json
{ "Effect": "Allow", "Action": "ec2:Describe*", "Resource": "*" }
```
Interns can *see* all EC2 instances (list/describe) — helpful for finding
the development instance — without being able to change production.

### 3. Never touch tags
```json
{ "Effect": "Deny", "Action": ["ec2:DeleteTags", "ec2:CreateTags"], "Resource": "*" }
```
Nobody in the group can create/delete tags. This protects the whole model:
if interns could retag a production instance as `development`, statement 1
would suddenly grant them full control over it.

## Why this design works

- **Tag-based scoping** = one policy, two environments. New development
  instances just get the `Env=development` tag; production stays safe.
- **Least privilege (as far as the project goes):** interns get EC2 access
  only, only where they need it, and cannot alter the tags that enforce it.
- **Testable without disruption:** the IAM Policy Simulator can verify
  `StopInstances` / `DeleteTags` outcomes before anyone logs in as the
  intern or stops a real instance (see `test-cases.md`).

## Known limitation (good interview talking point)

Statement 1 uses `ec2:*` — broad. A stricter production version would list
only the actions interns truly need (`ec2:StartInstances`,
`ec2:StopInstances`, `ec2:Describe*`, …) and scope `Resource` to specific
instance ARNs instead of `*`. The tag condition is what makes the broad
action safe *in this project*; in a real account, narrow both.
