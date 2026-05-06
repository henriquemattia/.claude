# Troubleshooting — PX-Nexus

## CloudWatch Log Groups

| Log Group | Source |
|:----------|:-------|
| `/ecs/px-nexus-api` | Application logs (NestJS) |
| `/aws/codebuild/px-nexus-api-build` | Build logs |
| `/ecs/px-nexus-api-dd-poc` | Datadog POC (legacy) |

## View Logs

### Application logs (recent)

```bash
aws logs tail /ecs/px-nexus-api --since 30m --follow
```

### Application logs (with filter)

```bash
aws logs tail /ecs/px-nexus-api --since 1h --filter-pattern "ERROR"
```

### Build logs

```bash
aws logs tail /aws/codebuild/px-nexus-api-build --since 1h
```

### Query logs with Insights

```bash
aws logs start-query \
    --log-group-name /ecs/px-nexus-api \
    --start-time $(date -v-1H +%s) \
    --end-time $(date +%s) \
    --query-string 'fields @timestamp, @message | filter @message like /error/i | sort @timestamp desc | limit 50'
```

## Health Check

- **Path:** GET `/health`
- **Target Group:** `px-nexus-api-tg`
- **Interval:** 300s, Timeout: 120s
- **Thresholds:** 2 healthy / 2 unhealthy
- **Success Codes:** 200-399

### Check target health

```bash
TG_ARN=$(aws elbv2 describe-target-groups --names px-nexus-api-tg --query 'TargetGroups[0].TargetGroupArn' --output text)

aws elbv2 describe-target-health --target-group-arn "$TG_ARN"
```

## Common Issues

### Task keeps restarting

```bash
aws ecs describe-services --cluster px-nexus-cluster --services px-nexus-api-service \
    --query 'services[0].events[:10].[createdAt,message]' --output table
```

Check stopped tasks for reason:
```bash
STOPPED=$(aws ecs list-tasks --cluster px-nexus-cluster --service-name px-nexus-api-service --desired-status STOPPED --query 'taskArns[0]' --output text)

aws ecs describe-tasks --cluster px-nexus-cluster --tasks "$STOPPED" \
    --query 'tasks[0].{reason:stoppedReason,code:stopCode,exitCode:containers[0].exitCode}'
```

### Can't connect to RDS from local

1. Check your public IP: `curl -s ifconfig.me`
2. Check if IP is in the RDS SG:
```bash
RDS_SG=$(aws rds describe-db-instances --db-instance-identifier px-nexus-db --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' --output text)

aws ec2 describe-security-group-rules --filters "Name=group-id,Values=$RDS_SG" \
    --query 'SecurityGroupRules[?!IsEgress].{from:FromPort,cidr:CidrIpv4}' --output table
```
3. Add your IP if missing (see [rds.md](rds.md))

### ECS Exec not working

```bash
TASK_ARN=$(aws ecs list-tasks --cluster px-nexus-cluster --service-name px-nexus-api-service --query 'taskArns[0]' --output text)

aws ecs describe-tasks --cluster px-nexus-cluster --tasks "$TASK_ARN" \
    --query 'tasks[0].containers[0].managedAgents[?name==`ExecuteCommandAgent`].lastStatus'
```

Expected: `RUNNING`. If not, force new deployment.

### Pipeline failed

```bash
aws codepipeline get-pipeline-state --name px-nexus-pipeline \
    --query 'stageStates[*].{stage:stageName,status:latestExecution.status}'
```

For build failures, check CodeBuild logs:
```bash
aws logs tail /aws/codebuild/px-nexus-api-build --since 1h
```

### Deployment stuck

```bash
aws ecs describe-services --cluster px-nexus-cluster --services px-nexus-api-service \
    --query 'services[0].deployments[*].{status:status,running:runningCount,desired:desiredCount,taskDef:taskDefinition}'
```

If stuck, force new deployment or rollback:
```bash
aws ecs update-service \
    --cluster px-nexus-cluster \
    --service px-nexus-api-service \
    --force-new-deployment
```

## Known Observations

- No HTTP→HTTPS redirect on ALB (port 80 forwards directly to target group)
- RDS storage is not encrypted
- No VPC endpoints configured (traffic to AWS services goes via internet)
- Health check interval is 300s (5 min) — failures take time to detect
- Circuit breaker is disabled on the ECS service
