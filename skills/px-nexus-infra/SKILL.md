---
name: px-nexus-infra
description: |
  PX-Nexus AWS infrastructure reference. Use when connecting to remote environment, debugging ECS tasks, accessing RDS database, viewing logs, or managing deployments.
triggers:
  - nexus infra
  - ecs exec
  - nexus logs
  - nexus deploy
  - nexus db
  - connect remote
  - aws nexus
  - nexus container
  - nexus pipeline
  - nexus secrets
  - nexus alb
  - nexus rds
  - nexus ecs
  - shell container
  - remote database
  - cloudwatch nexus
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
category: cloud-infrastructure
metadata:
  version: 1.0.0
  environment: staging
  region: us-east-1
---

# PX-Nexus AWS Infrastructure

Static navigation guide for the PX-Nexus staging environment. Contains resource names and discovery commands — no hardcoded values.

## Resource Names

| Resource | Name |
|:---------|:-----|
| **ECS Cluster** | `px-nexus-cluster` |
| **ECS Service** | `px-nexus-api-service` |
| **Task Def Family** | `px-nexus-api` |
| **Container** | `px-nexus-api` (port 3001) |
| **RDS Instance** | `px-nexus-db` |
| **DB Name / User** | `px_nexus` / `postgres` |
| **ALB** | `px-nexus-alb` |
| **ECR Repo** | `px-nexus-api` |
| **Main Secret** | `px-nexus-stg-secret` |
| **CodeBuild** | `px-nexus-api-build` |
| **CodePipeline** | `px-nexus-pipeline` |

## Decision Tree

```
What do you need?
│
├── Shell into the container ──────────► ECS Exec (see below)
├── Connect to the database ───────────► references/rds.md
├── View application logs ─────────────► references/troubleshooting.md
├── View/update secrets ───────────────► references/secrets.md
├── Force a new deployment ────────────► references/cicd.md
├── Check network/ALB/SGs ─────────────► references/networking.md
├── View build logs ───────────────────► references/cicd.md
└── Understand architecture ───────────► references/architecture.md
```

## Quick Commands

### Shell into the running container

```bash
TASK_ARN=$(aws ecs list-tasks --cluster px-nexus-cluster --service-name px-nexus-api-service --query 'taskArns[0]' --output text)

aws ecs execute-command \
    --cluster px-nexus-cluster \
    --task "$TASK_ARN" \
    --container px-nexus-api \
    --interactive \
    --command "/bin/sh"
```

### View recent application logs

```bash
aws logs tail /ecs/px-nexus-api --since 30m --follow
```

### Force new deployment

```bash
aws ecs update-service \
    --cluster px-nexus-cluster \
    --service px-nexus-api-service \
    --force-new-deployment
```

### Check service status

```bash
aws ecs describe-services \
    --cluster px-nexus-cluster \
    --services px-nexus-api-service \
    --query 'services[0].{status:status,running:runningCount,desired:desiredCount}'
```

### Read a secret

```bash
aws secretsmanager get-secret-value \
    --secret-id px-nexus-stg-secret \
    --query SecretString --output text | jq .
```

### Discover RDS endpoint

```bash
aws rds describe-db-instances \
    --db-instance-identifier px-nexus-db \
    --query 'DBInstances[0].Endpoint.{host:Address,port:Port}'
```

## Credential Notes

- AWS credentials are temporary (SSO session tokens expire)
- If you get `ExpiredToken`, run: `aws sso login`
- Verify identity: `aws sts get-caller-identity`

## Reference Files

| File | Content |
|:-----|:--------|
| [architecture.md](references/architecture.md) | Architecture flow, resource topology |
| [ecs.md](references/ecs.md) | Cluster, service, task definition, ECS Exec |
| [rds.md](references/rds.md) | Database connectivity, discovery commands |
| [networking.md](references/networking.md) | VPC, subnets, security groups, ALB |
| [secrets.md](references/secrets.md) | Secrets Manager, env var categories |
| [cicd.md](references/cicd.md) | CodeBuild, CodePipeline, ECR |
| [troubleshooting.md](references/troubleshooting.md) | Logs, health checks, common errors |
