# Architecture

## Network Flow

```
Internet
  │
  ▼
ALB (px-nexus-alb)
  │  SG: px-nexus-alb-sg ← allows 80/443 from internet
  │  SSL: *.motoristapx.com.br
  │
  ├── :80  → forward to target group (no HTTPS redirect)
  └── :443 → forward to target group (TLS 1.3)
        │
        ▼
  Target Group (px-nexus-api-tg)
        │  Health: GET /health
        │  Protocol: HTTP:3001
        │
        ▼
  ECS Fargate (px-nexus-api-service)
        │  SG: px-nexus-ecs-sg ← allows 3001 from ALB SG only
        │  Public subnets, public IP enabled
        │
        ▼
  RDS PostgreSQL (px-nexus-db)
     SG: px-nexus-rds-sg ← allows 5432 from ECS SG + whitelisted IPs
     Publicly accessible (requires IP in SG)
```

## CI/CD Flow

```
GitHub (px-center/px-nexus)
  │
  ▼
CodePipeline (px-nexus-pipeline)
  │
  ▼
CodeBuild (px-nexus-api-build)
  │  buildspec.yml
  │
  ├── Build Docker image
  ├── Push to ECR (px-nexus-api:latest)
  └── Register new task definition
        │
        ▼
  ECS Service rolling update
     maxPercent: 200, minHealthyPercent: 100
```

## VPC Layout

```
VPC: px-center-labs-vpc (10.5.0.0/16)
│
├── Public Subnets (used by ALB, ECS, RDS)
│   ├── px-center-labs-public-1  │ us-east-1a │ 10.5.100.0/24
│   └── px-center-labs-public-2  │ us-east-1b │ 10.5.101.0/24
│
└── Private Subnets (available but unused currently)
    ├── px-center-labs-private-1 │ us-east-1a │ 10.5.1.0/24
    └── px-center-labs-private-2 │ us-east-1b │ 10.5.2.0/24
```

## Discover Resource IDs

All resource IDs should be fetched dynamically:

```bash
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=px-center-labs-vpc" --query 'Vpcs[0].VpcId'
aws ec2 describe-subnets --filters "Name=tag:Name,Values=px-center-labs-*" --query 'Subnets[*].{name:Tags[?Key==`Name`].Value|[0],id:SubnetId,az:AvailabilityZone,cidr:CidrBlock}'
aws ec2 describe-security-groups --filters "Name=tag:Project,Values=px-nexus" --query 'SecurityGroups[*].{name:GroupName,id:GroupId}'
aws elbv2 describe-load-balancers --names px-nexus-alb --query 'LoadBalancers[0].{arn:LoadBalancerArn,dns:DNSName}'
aws ecs describe-clusters --clusters px-nexus-cluster --query 'clusters[0].clusterArn'
aws rds describe-db-instances --db-instance-identifier px-nexus-db --query 'DBInstances[0].{arn:DBInstanceArn,endpoint:Endpoint}'
aws ecr describe-repositories --repository-names px-nexus-api --query 'repositories[0].repositoryUri'
```

## IAM Roles (by name)

| Role Name | Used By |
|:----------|:--------|
| `px-nexus-ecs-task-execution-role` | ECS (pull images, get secrets, write logs) |
| `px-nexus-ecs-task-role` | Application code (S3, etc.) |
| `px-nexus-codebuild-role` | Build process |
| `px-nexus-codepipeline-role` | Pipeline orchestration |

## S3 Buckets

| Bucket Name | Purpose |
|:------------|:--------|
| `px-nexus-stg-terraform-state` | Terraform state |
| `px-nexus-uploads-labs` | Application uploads |
| `px-nexus-codebuild-source-*` | CodeBuild source artifacts |
