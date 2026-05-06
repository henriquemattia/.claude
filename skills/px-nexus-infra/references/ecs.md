# ECS — PX-Nexus

## Resource Names

| Property | Value |
|:---------|:------|
| **Cluster** | `px-nexus-cluster` |
| **Service** | `px-nexus-api-service` |
| **Task Def Family** | `px-nexus-api` |
| **Container** | `px-nexus-api` |
| **Port** | 3001 |
| **Launch Type** | FARGATE |
| **ECS Exec** | Enabled |

## Specs (as of creation)

- 0.5 vCPU, 1 GB RAM, 20 GiB ephemeral storage
- Desired count: 1
- Rolling deployment (maxPercent: 200, minHealthyPercent: 100)
- Public subnets, public IP enabled

## Discovery Commands

```bash
aws ecs describe-clusters --clusters px-nexus-cluster \
    --query 'clusters[0].{name:clusterName,status:status,running:runningTasksCount}'

aws ecs describe-services --cluster px-nexus-cluster --services px-nexus-api-service \
    --query 'services[0].{status:status,running:runningCount,desired:desiredCount,taskDef:taskDefinition}'

aws ecs describe-task-definition --task-definition px-nexus-api \
    --query 'taskDefinition.{family:family,revision:revision,cpu:cpu,memory:memory}'
```

## ECS Exec — Shell into Container

```bash
TASK_ARN=$(aws ecs list-tasks --cluster px-nexus-cluster --service-name px-nexus-api-service --query 'taskArns[0]' --output text)

aws ecs execute-command \
    --cluster px-nexus-cluster \
    --task "$TASK_ARN" \
    --container px-nexus-api \
    --interactive \
    --command "/bin/sh"
```

### Run a single command inside the container

```bash
aws ecs execute-command \
    --cluster px-nexus-cluster \
    --task "$TASK_ARN" \
    --container px-nexus-api \
    --interactive \
    --command "node -e 'console.log(process.env.NODE_ENV)'"
```

### Verify ECS Exec agent is running

```bash
aws ecs describe-tasks --cluster px-nexus-cluster --tasks "$TASK_ARN" \
    --query 'tasks[0].containers[0].managedAgents'
```

## Force New Deployment

```bash
aws ecs update-service \
    --cluster px-nexus-cluster \
    --service px-nexus-api-service \
    --force-new-deployment
```

## View Service Events

```bash
aws ecs describe-services --cluster px-nexus-cluster --services px-nexus-api-service \
    --query 'services[0].events[:10].[createdAt,message]' --output table
```

## Get Running Task Details

```bash
TASK_ARN=$(aws ecs list-tasks --cluster px-nexus-cluster --service-name px-nexus-api-service --query 'taskArns[0]' --output text)

aws ecs describe-tasks --cluster px-nexus-cluster --tasks "$TASK_ARN" \
    --query 'tasks[0].{status:lastStatus,health:healthStatus,started:startedAt,ip:attachments[0].details[?name==`privateIPv4Address`].value|[0]}'
```

## Scale Service

```bash
aws ecs update-service \
    --cluster px-nexus-cluster \
    --service px-nexus-api-service \
    --desired-count 2
```

## Container Config

- Logging: awslogs → `/ecs/px-nexus-api` (stream prefix: `ecs`)
- Secrets injected from: `px-nexus-stg-secret` (see [secrets.md](secrets.md))
- Datadog env vars hardcoded in task definition (DD_SERVICE, DD_ENV, etc.)
