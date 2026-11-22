# Push this project to GitHub — Windows PowerShell steps (fixed)

> 🔒 **Keep this repository Private.** Screenshots and the PDF show your AWS account ID, EC2 instance IDs, and public IPs. Private is the safer default.

## Why your earlier commands failed (S3 repo)

| What you typed | What happened | Fix |
|---|---|---|
| `"C:\...\create-s3-buckets-with-terraform.zip"` | PowerShell just printed the path — it does **not** unzip anything | Unzip first |
| `cd create-s3-buckets-with-terraform` | It looked in `C:\Users\Mudau` instead of Downloads | Use the full Downloads path below |
| `gh auth login` → "not recognized" | GitHub CLI (`gh`) is not installed | Install it (Step 2), then close and reopen PowerShell |

## Step 1 — Unzip the project

Right-click `cloud-security-with-aws-iam.zip` in Downloads → **Extract All** → Extract. You should have a folder named `cloud-security-with-aws-iam`.

## Step 2 — Install GitHub CLI (`gh`) — once only

```powershell
winget install --id GitHub.cli
```

Then **close PowerShell completely and open a new one**. Verify:

```powershell
gh --version
git --version
```

## Step 3 — Go to the extracted project folder

```powershell
cd "$env:USERPROFILE\Downloads\cloud-security-with-aws-iam"
dir
```

You should see `README.md`, `iam`, `docs`, `scripts`, and `.github`.

## Step 4 — Initialize Git and make the first commit

The downloadable ZIP intentionally excludes `.git`, so create the local Git repository first:

```powershell
git init
git branch -M main
git add -A
git status --short
git commit -m "Cloud Security with AWS IAM project"
```

If Git says your name or email is not configured, set them for this repo and retry the commit. Prefer your GitHub-provided `noreply` email to keep your personal email out of commit history:

```powershell
git config user.name "Your Name"
git config user.email "your-github-noreply-email"
git commit -m "Cloud Security with AWS IAM project"
```

## Step 5 — Log in and create a Private repo + push

```powershell
gh auth login
```

Choose `GitHub.com` → `HTTPS` → `Login with a web browser` → complete browser authorization. Then:

```powershell
gh repo create cloud-security-with-aws-iam --private --source=. --remote=origin --push
```

## Step 6 — Check it worked

```powershell
gh repo view --web
```

Your browser opens the new repo. Also check the **Actions** tab — *Validate IAM policy* should be green.

## No `gh`? Use plain Git instead

After completing Step 4:

1. Go to github.com → **New repository** → name `cloud-security-with-aws-iam` → **Private** → do **not** tick "Add a README" → Create.
2. In PowerShell (in the project folder):

```powershell
git remote add origin https://github.com/your-username/cloud-security-with-aws-iam.git
git push -u origin main
```

Authenticate through Git Credential Manager or GitHub's prompt. Never paste a Personal Access Token into chat or commit it.
