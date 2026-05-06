# RDS — PX-Nexus

## Resource Names

| Property | Value |
|:---------|:------|
| **Instance** | `px-nexus-db` |
| **Engine** | PostgreSQL 16 |
| **DB Name** | `px_nexus` |
| **Master User** | `postgres` |
| **Publicly Accessible** | Yes (requires IP in SG) |

## Specs (as of creation)

- db.t3.micro, 20 GB gp3
- Single-AZ (us-east-1b), no encryption, no Multi-AZ
- Backup retention: 7 days
- Deletion protection: disabled

## Discover Endpoint

```bash
aws rds describe-db-instances --db-instance-identifier px-nexus-db \
    --query 'DBInstances[0].Endpoint.{host:Address,port:Port}' --output text
```

## Discover Password

```bash
aws secretsmanager get-secret-value --secret-id px-nexus-stg-secret \
    --query SecretString --output text | jq -r .DB_PASSWORD
```

## Connect from Local Machine

Requires your IP whitelisted in the RDS security group (`px-nexus-rds-sg`).

```bash
RDS_HOST=$(aws rds describe-db-instances --db-instance-identifier px-nexus-db --query 'DBInstances[0].Endpoint.Address' --output text)

psql -h "$RDS_HOST" -p 5432 -U postgres -d px_nexus
```

## Connect via ECS Exec (no SG whitelisting needed)

```bash
TASK_ARN=$(aws ecs list-tasks --cluster px-nexus-cluster --service-name px-nexus-api-service --query 'taskArns[0]' --output text)
RDS_HOST=$(aws rds describe-db-instances --db-instance-identifier px-nexus-db --query 'DBInstances[0].Endpoint.Address' --output text)

aws ecs execute-command \
    --cluster px-nexus-cluster \
    --task "$TASK_ARN" \
    --container px-nexus-api \
    --interactive \
    --command "psql -h $RDS_HOST -p 5432 -U postgres -d px_nexus"
```

## Check RDS Status

```bash
aws rds describe-db-instances --db-instance-identifier px-nexus-db \
    --query 'DBInstances[0].{status:DBInstanceStatus,engine:EngineVersion,class:DBInstanceClass,storage:AllocatedStorage,az:AvailabilityZone}'
```

## Whitelist a New IP

```bash
RDS_SG=$(aws rds describe-db-instances --db-instance-identifier px-nexus-db --query 'DBInstances[0].VpcSecurityGroups[0].VpcSecurityGroupId' --output text)

aws ec2 authorize-security-group-ingress \
    --group-id "$RDS_SG" \
    --protocol tcp \
    --port 5432 \
    --cidr "YOUR_IP/32"
```

## Networking

- SG name: `px-nexus-rds-sg`
- Subnet group: `px-nexus-db-subnet-group-public` (public subnets)
- Inbound: port 5432 from ECS SG + whitelisted developer IPs
