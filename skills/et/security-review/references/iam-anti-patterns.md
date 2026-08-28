# IAM Anti-Patterns

Common over-permissive patterns found in ASU PRs, with fixes.

## 1. Wildcard Actions

**Bad:**
```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

**Fix:** Scope to the actions actually needed:
```json
{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
  "Resource": [
    "arn:aws:s3:::my-bucket",
    "arn:aws:s3:::my-bucket/*"
  ]
}
```

## 2. AdministratorAccess on Service Roles

**Bad:**
```hcl
resource "aws_iam_role_policy_attachment" "jenkins_admin" {
  role       = aws_iam_role.jenkins.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
```

**When acceptable:** Only for Jenkins PoP roles that manage full-account infrastructure. Even then, flag for awareness.

**Fix for application roles:** Create a custom policy with only the permissions the service needs.

## 3. Wildcarded Vault Secret Paths

**Bad:**
```hcl
ops_vault_policies = [
  {
    path         = "secret/*"
    capabilities = ["read", "create", "update", "delete"]
  }
]
```

**Fix:** Enumerate specific paths:
```hcl
ops_vault_policies = [
  {
    path         = "secret/services/dco/jenkins/myteam/myapp/*"
    capabilities = ["read", "create", "update"]
  }
]
```

## 4. Overly Broad Trust Policies

**Bad:**
```json
{
  "Principal": {"AWS": "*"},
  "Action": "sts:AssumeRole"
}
```

**Fix:** Scope to specific role ARNs:
```json
{
  "Principal": {"AWS": "arn:aws:iam::524415254265:role/EKS-ServiceAccount-jenkins-myteam"},
  "Action": "sts:AssumeRole"
}
```

## 5. Missing Conditions

**Bad:** A policy that grants cross-account access with no conditions.

**Fix:** Add conditions to restrict:
```json
{
  "Condition": {
    "StringEquals": {
      "aws:PrincipalOrgID": "o-xxxxxxxxxx"
    }
  }
}
```

## 6. CreateLogGroup with Resource *

**Bad:**
```json
{
  "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
  "Resource": "*"
}
```

**Fix:** Split — `CreateLogGroup` can use `*`, but stream/event writes scope to the log group ARN:
```json
[
  {
    "Action": "logs:CreateLogGroup",
    "Resource": "*"
  },
  {
    "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
    "Resource": "arn:aws:logs:us-west-2:123456789:log-group:/aws/lambda/my-function:*"
  }
]
```

## 7. "We'll Scope Down Later"

Any comment or PR description that says permissions will be tightened in a future PR is a red flag. Temporary permissions become permanent. Require scoping now or a linked follow-up ticket with a deadline.
