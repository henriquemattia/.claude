# CI/CD — PX-Nexus

## Pipeline Overview

```
GitHub (px-center/px-nexus)
  → CodePipeline (px-nexus-pipeline)
    → CodeBuild (px-nexus-api-build)
      → ECR (px-nexus-api:latest)
        → ECS rolling deployment
```

## ECR Repository

| Property | Value |
|:---------|:------|
| **Name** | `px-nexus-api` |
| **Tag Mutability** | Mutable |
| **Scan on Push** | Enabled |

```bash
aws ecr describe-repositories --repository-names px-nexus-api \
    --query 'repositories[0].{uri:repositoryUri,arn:repositoryArn}'
```

### Login to ECR

```bash
aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin \
    $(aws ecr describe-repositories --repository-names px-nexus-api --query 'repositories[0].repositoryUri' --output text | cut -d/ -f1)
```

### List recent images

```bash
aws ecr describe-images --repository-name px-nexus-api \
    --query 'imageDetails | sort_by(@, &imagePushedAt) | [-5:].[imageTags[0],imagePushedAt]' \
    --output table
```

## CodeBuild

| Property | Value |
|:---------|:------|
| **Project** | `px-nexus-api-build` |
| **Source** | GitHub (`px-center/px-nexus`) |
| **Buildspec** | `buildspec.yml` |
| **Image** | `aws/codebuild/standard:7.0` |
| **Compute** | `BUILD_GENERAL1_LARGE` |
| **Privileged** | Yes (Docker builds) |

### View recent builds

```bash
aws codebuild list-builds-for-project --project-name px-nexus-api-build \
    --query 'ids[:5]' --output table
```

### Get last build status

```bash
BUILD_ID=$(aws codebuild list-builds-for-project --project-name px-nexus-api-build --query 'ids[0]' --output text)

aws codebuild batch-get-builds --ids "$BUILD_ID" \
    --query 'builds[0].{status:buildStatus,start:startTime,end:endTime}'
```

### View build logs

```bash
aws logs tail /aws/codebuild/px-nexus-api-build --since 1h
```

### Trigger a build manually

```bash
aws codebuild start-build --project-name px-nexus-api-build
```

## CodePipeline

| Property | Value |
|:---------|:------|
| **Name** | `px-nexus-pipeline` |
| **Version** | V2 |

### View pipeline state

```bash
aws codepipeline get-pipeline-state --name px-nexus-pipeline \
    --query 'stageStates[*].{stage:stageName,status:latestExecution.status}'
```

### View recent executions

```bash
aws codepipeline list-pipeline-executions --pipeline-name px-nexus-pipeline \
    --query 'pipelineExecutionSummaries[:5].{status:status,trigger:trigger.triggerType,time:startTime}' \
    --output table
```

### Trigger pipeline manually

```bash
aws codepipeline start-pipeline-execution --name px-nexus-pipeline
```

## IAM Roles (by name)

| Role | Used By |
|:-----|:--------|
| `px-nexus-ecs-task-execution-role` | ECS (pull images, get secrets, write logs) |
| `px-nexus-ecs-task-role` | Application code (S3, etc.) |
| `px-nexus-codebuild-role` | Build process |
| `px-nexus-codepipeline-role` | Pipeline orchestration |

## Full Deployment Flow

1. Push to GitHub triggers CodePipeline
2. CodePipeline starts CodeBuild
3. CodeBuild runs `buildspec.yml` → builds image → pushes to ECR → registers new task def
4. ECS rolling update: starts new task → health check passes → drains old task
5. Verify: `aws ecs describe-services --cluster px-nexus-cluster --services px-nexus-api-service`
