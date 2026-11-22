# Cloud Security with AWS IAM

> **NextWork project** — *Cloud Security with AWS IAM*
> **Author:** Richard Lutendo Mudau

Use **AWS IAM** (Identity and Access Management) to control who can do what
in an AWS account: tag two EC2 instances by environment, write a JSON policy
that gives an intern full control over *development only*, attach it to a
user group, set an account alias, and prove — by logging in as the intern
and with the Policy Simulator — that production is protected.

![AWS IAM](https://img.shields.io/badge/AWS-IAM-FF9900?logo=amazonaws)
![EC2](https://img.shields.io/badge/Amazon-EC2-FF9900?logo=amazonec2)
![License](https://img.shields.io/badge/License-MIT-green)

## What this project does

1. Launches **two EC2 instances** and tags them `Env=development` /
   `Env=production` (tags = labels for grouping, cost allocation, and
   tag-based policies)
2. Creates a **JSON IAM policy** (`NextWorkDevEnvironmentPolicy`):
   allow all EC2 actions on development-tagged instances, allow
   read-only `Describe*` everywhere, explicitly deny tag changes
3. Sets an **account alias** (`nextwork-alias-lutendo`) so the console
   sign-in URL uses a nickname instead of the long account ID
4. Creates an **IAM user group** (`nextwork-dev-group`), attaches the
   policy to the group, and adds an **intern IAM user** to it
5. **Tests** the policy live (stop production → denied; stop development
   → allowed) and in the **IAM Policy Simulator**

**Tools & concepts:** IAM users, policies, user groups, account aliases,
Policy Simulator, JSON policies (`Effect` / `Action` / `Resource` /
`Condition`), EC2 tagging.

## Repository layout

```
cloud-security-with-aws-iam/
├── README.md                  ← you are here
├── PUSH-TO-GITHUB.md          ← Windows-first steps to publish to GitHub
├── LICENSE
├── .gitignore
├── iam/
│   ├── NextWorkDevEnvironmentPolicy.json  ← the exact policy from the project
│   ├── policy-explained.md                ← Effect/Action/Resource/Condition
│   └── test-cases.md                      ← live + simulator test results
├── scripts/
│   └── verify-policy.py       ← local/CI validator (no AWS access needed)
├── docs/
│   ├── cloud-security-with-aws-iam.pdf    ← original NextWork write-up
│   ├── TROUBLESHOOTING.md
│   └── screenshots/01–07      ← screenshots extracted from the write-up
└── .github/workflows/
    └── validate-policy.yml    ← CI: validates the policy JSON on push/PR
```

## The policy at a glance

```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": "ec2:*", "Resource": "*",
      "Condition": { "StringEquals": { "ec2:ResourceTag/Env": "development" } } },
    { "Effect": "Allow", "Action": "ec2:Describe*", "Resource": "*" },
    { "Effect": "Deny",  "Action": ["ec2:DeleteTags", "ec2:CreateTags"], "Resource": "*" }
  ]
}
```

Full breakdown: [`iam/policy-explained.md`](iam/policy-explained.md) ·
Test evidence: [`iam/test-cases.md`](iam/test-cases.md)

## Reproduce it in your own AWS account (Console steps)

1. **EC2:** Launch 2 instances (e.g. `t3.micro`, `eu-north-1`). Add tags:
   `Name=<your-dev-name>`, `Env=development` on one;
   `Name=<your-prod-name>`, `Env=production` on the other.
2. **Policy:** IAM → Policies → Create policy → JSON → paste
   `iam/NextWorkDevEnvironmentPolicy.json` → name it
   `NextWorkDevEnvironmentPolicy`.
3. **Alias:** IAM → Account settings → *Account alias* → set your alias
   (e.g. `nextwork-alias-<yourname>`). Sign-in URL becomes
   `https://<alias>.signin.aws.amazon.com/console`.
4. **Group:** IAM → User groups → Create group `nextwork-dev-group` →
   attach `NextWorkDevEnvironmentPolicy`.
5. **User:** IAM → Users → Create user (intern) → add to the group →
   set console access → share sign-in details (email instructions or
   download the CSV — **this is the only time the password is shown**).
6. **Test live:** sign in as the intern → try stopping production
   (expect *AccessDenied*) and development (expect *Stopped*).
7. **Test safely:** IAM → Policy Simulator → your group/user →
   `StopInstances` (allowed) vs `DeleteTags` (denied).

> ⚠️ This project was done in the AWS Console (no Terraform). The repo
> therefore contains the policy as JSON + docs + a validator, not `.tf`
> files. If you later want it as code, the same policy maps directly to
> `aws_iam_policy` / `aws_iam_group_policy_attachment` in Terraform.

## Validate the policy locally (no AWS needed)

```bash
python3 scripts/verify-policy.py
# OK: ... all policy checks passed
```

## Screenshots

| Screenshot | File |
|---|---|
| JSON policy in the Policy editor | [`docs/screenshots/01-json-policy.png`](docs/screenshots/01-json-policy.png) |
| EC2 Name/Env tags | [`docs/screenshots/02-ec2-tags.png`](docs/screenshots/02-ec2-tags.png) |
| Account alias dialog | [`docs/screenshots/03-account-alias.png`](docs/screenshots/03-account-alias.png) |
| IAM user created (sign-in details) | [`docs/screenshots/04-iam-user-created.png`](docs/screenshots/04-iam-user-created.png) |
| Stop production → denied | [`docs/screenshots/05-stop-production-denied.png`](docs/screenshots/05-stop-production-denied.png) |
| Stop development → allowed | [`docs/screenshots/06-stop-development-allowed.png`](docs/screenshots/06-stop-development-allowed.png) |
| Policy Simulator results | [`docs/screenshots/07-policy-simulator.png`](docs/screenshots/07-policy-simulator.png) |

> 🔒 **Security note:** screenshots 03/05/06 and the PDF contain your AWS
> account ID, instance IDs, and public IPs. **Publish this repo as PRIVATE**
> (or accept that those IDs become public). Never publish passwords,
> access keys, or sign-in CSVs — none are included here.

## Project reflection (from the original write-up)

> This project took approximately 1.5 hours including demo time. The most
> challenging part was understanding the IAM policy since it was written in
> JSON and contained multiple statements. It was most rewarding to see
> permission successfully denied when my intern tried to delete my
> production instance — my IAM access management worked.

Full write-up: [`docs/cloud-security-with-aws-iam.pdf`](docs/cloud-security-with-aws-iam.pdf)

## Troubleshooting

See [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

## License

MIT — see [`LICENSE`](LICENSE).
