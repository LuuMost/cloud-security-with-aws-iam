#!/usr/bin/env python3
"""Validate the NextWorkDevEnvironmentPolicy JSON without needing AWS access.

Checks:
  1. File is valid JSON with Version + Statement.
  2. Statement 1: Allow ec2:* only when tag Env=development.
  3. Statement 2: Allow ec2:Describe* (read-only visibility).
  4. Statement 3: Explicit Deny on ec2:DeleteTags + ec2:CreateTags.
  5. No statement uses Action "*" (least-privilege sanity check).

Usage:  python3 scripts/verify-policy.py [path/to/policy.json]
Exit code 0 = all checks passed, 1 = a check failed.
"""
import json
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "iam" / "NextWorkDevEnvironmentPolicy.json"


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    try:
        policy = json.loads(path.read_text())
    except Exception as exc:  # noqa: BLE001 - report any parse error clearly
        print(f"FAIL: {path} is not valid JSON: {exc}")
        return 1

    errors = []
    if policy.get("Version") != "2012-10-17":
        errors.append("Version must be '2012-10-17'")
    stmts = policy.get("Statement", [])
    if len(stmts) != 3:
        errors.append(f"Expected 3 statements, found {len(stmts)}")

    def has_action(stmt, action):
        actions = stmt.get("Action", [])
        return action in (actions if isinstance(actions, list) else [actions])

    if stmts:
        s1 = stmts[0]
        if s1.get("Effect") != "Allow" or not has_action(s1, "ec2:*"):
            errors.append("Statement 1 must Allow ec2:*")
        cond = s1.get("Condition", {}).get("StringEquals", {})
        if cond.get("ec2:ResourceTag/Env") != "development":
            errors.append("Statement 1 must require tag Env=development")
    if len(stmts) > 1:
        s2 = stmts[1]
        if s2.get("Effect") != "Allow" or not has_action(s2, "ec2:Describe*"):
            errors.append("Statement 2 must Allow ec2:Describe*")
    if len(stmts) > 2:
        s3 = stmts[2]
        if s3.get("Effect") != "Deny":
            errors.append("Statement 3 must be an explicit Deny")
        for action in ("ec2:DeleteTags", "ec2:CreateTags"):
            if not has_action(s3, action):
                errors.append(f"Statement 3 must Deny {action}")

    for i, stmt in enumerate(stmts, 1):
        if stmt.get("Action") == "*":
            errors.append(f"Statement {i} uses Action '*' — too broad")

    if errors:
        print(f"FAIL: {path}")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {path} — all policy checks passed (3 statements, tag-scoped Allow, explicit Deny).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
