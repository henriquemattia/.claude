# Networking — PX-Nexus

## VPC

| Property | Value |
|:---------|:------|
| **Name** | `px-center-labs-vpc` |
| **CIDR** | `10.5.0.0/16` |

```bash
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=px-center-labs-vpc" \
    --query 'Vpcs[0].{id:VpcId,cidr:CidrBlock,state:State}'
```

## Subnets

| Name | AZ | CIDR | Type |
|:-----|:---|:-----|:-----|
| `px-center-labs-public-1` | us-east-1a | `10.5.100.0/24` | Public |
| `px-center-labs-public-2` | us-east-1b | `10.5.101.0/24` | Public |
| `px-center-labs-private-1` | us-east-1a | `10.5.1.0/24` | Private |
| `px-center-labs-private-2` | us-east-1b | `10.5.2.0/24` | Private |

```bash
aws ec2 describe-subnets --filters "Name=tag:Name,Values=px-center-labs-*" \
    --query 'Subnets[*].{name:Tags[?Key==`Name`].Value|[0],id:SubnetId,az:AvailabilityZone,cidr:CidrBlock,public:MapPublicIpOnLaunch}' \
    --output table
```

## Security Groups

Three SGs, all tagged `Project=px-nexus`:

| Name | Purpose | Key Rules |
|:-----|:--------|:----------|
| `px-nexus-alb-sg` | ALB | Inbound: 80, 443 from `0.0.0.0/0` |
| `px-nexus-ecs-sg` | ECS tasks | Inbound: 3001 from ALB SG only |
| `px-nexus-rds-sg` | RDS | Inbound: 5432 from ECS SG + whitelisted IPs |

```bash
aws ec2 describe-security-groups \
    --filters "Name=tag:Project,Values=px-nexus" \
    --query 'SecurityGroups[*].{name:GroupName,id:GroupId,desc:Description}' --output table
```

### View rules for a specific SG

```bash
aws ec2 describe-security-group-rules \
    --filters "Name=group-id,Values=SG_ID" \
    --query 'SecurityGroupRules[*].{dir:IsEgress,proto:IpProtocol,from:FromPort,to:ToPort,cidr:CidrIpv4,srcSg:ReferencedGroupInfo.GroupId}' \
    --output table
```

## Application Load Balancer

| Property | Value |
|:---------|:------|
| **Name** | `px-nexus-alb` |
| **Scheme** | internet-facing |
| **SG** | `px-nexus-alb-sg` |

```bash
aws elbv2 describe-load-balancers --names px-nexus-alb \
    --query 'LoadBalancers[0].{dns:DNSName,state:State.Code,scheme:Scheme,arn:LoadBalancerArn}'
```

### Listeners

- `:80` — HTTP, forwards to target group (no HTTPS redirect)
- `:443` — HTTPS, TLS 1.3, cert `*.motoristapx.com.br`, forwards to target group

```bash
ALB_ARN=$(aws elbv2 describe-load-balancers --names px-nexus-alb --query 'LoadBalancers[0].LoadBalancerArn' --output text)

aws elbv2 describe-listeners --load-balancer-arn "$ALB_ARN" \
    --query 'Listeners[*].{port:Port,protocol:Protocol,actions:DefaultActions[0].Type}'
```

### Target Group

| Property | Value |
|:---------|:------|
| **Name** | `px-nexus-api-tg` |
| **Protocol** | HTTP:3001 |
| **Target Type** | ip |
| **Health Check** | GET `/health` |

```bash
aws elbv2 describe-target-groups --names px-nexus-api-tg \
    --query 'TargetGroups[0].{arn:TargetGroupArn,port:Port,healthPath:HealthCheckPath,interval:HealthCheckIntervalSeconds}'
```

### Check Target Health

```bash
TG_ARN=$(aws elbv2 describe-target-groups --names px-nexus-api-tg --query 'TargetGroups[0].TargetGroupArn' --output text)

aws elbv2 describe-target-health --target-group-arn "$TG_ARN"
```

## SSL Certificate

- Domain: `*.motoristapx.com.br`
- Managed by ACM

```bash
aws acm list-certificates --query 'CertificateSummaryList[?DomainName==`*.motoristapx.com.br`].{arn:CertificateArn,domain:DomainName,status:Status}'
```
