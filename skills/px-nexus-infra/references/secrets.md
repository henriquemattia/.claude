# Secrets — PX-Nexus

## Secrets in Secrets Manager

| Name | Purpose |
|:-----|:--------|
| `px-nexus-stg-secret` | Main secret (injected into ECS container) |
| `px-nexus/db-credentials` | Database credentials |
| `px-nexus/cortex-credentials` | Cortex API credentials |
| `px-nexus/aws-credentials` | AWS credentials for the application |

```bash
aws secretsmanager list-secrets \
    --filters "Key=name,Values=px-nexus" \
    --query 'SecretList[*].{name:Name,description:Description,lastChanged:LastChangedDate}'
```

## Main Secret: `px-nexus-stg-secret`

This is the primary secret injected into the ECS task definition. All keys are available as environment variables in the running container.

### Env Var Categories

| Category | Variables |
|:---------|:---------|
| **Database** | `DATABASE_URL`, `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` |
| **Server** | `HOST`, `PORT`, `NODE_ENV` |
| **AWS** | `ACCESS_KEY_ID`, `SECRET_ACCESS_KEY` |
| **API** | `API_KEY` |
| **Cortex** | `CORTEX_API_URL`, `CORTEX_API_KEY`, `CORTEX_AGENT_ID` |
| **Salesforce** | `SALESFORCE_URL`, `SALESFORCE_CLIENT_ID`, `SALESFORCE_CLIENT_SECRET` |
| **Azure AD** | `AZURE_AD_TENANT_ID`, `AZURE_AD_CLIENT_ID`, `AZURE_AD_CLIENT_SECRET` |
| **Datadog** | `DD_API_KEY` |

### Read all keys (names only, no values)

```bash
aws secretsmanager get-secret-value --secret-id px-nexus-stg-secret \
    --query SecretString --output text | jq 'keys'
```

### Read the full secret

```bash
aws secretsmanager get-secret-value --secret-id px-nexus-stg-secret \
    --query SecretString --output text | jq .
```

### Read a specific key

```bash
aws secretsmanager get-secret-value --secret-id px-nexus-stg-secret \
    --query SecretString --output text | jq -r '.DATABASE_URL'
```

## Update a Secret

### Update a single key

```bash
CURRENT=$(aws secretsmanager get-secret-value --secret-id px-nexus-stg-secret --query SecretString --output text)
UPDATED=$(echo "$CURRENT" | jq '.MY_KEY = "new-value"')

aws secretsmanager update-secret \
    --secret-id px-nexus-stg-secret \
    --secret-string "$UPDATED"
```

### After updating, force new ECS deployment to pick up changes

```bash
aws ecs update-service \
    --cluster px-nexus-cluster \
    --service px-nexus-api-service \
    --force-new-deployment
```

## Hardcoded Env Vars (in Task Definition, not Secrets Manager)

Datadog-related variables are set directly in the task definition, not via secrets:
`DD_SERVICE`, `DD_ENV`, `DD_VERSION`, `DD_SITE`, `DD_TRACE_ENABLED`, `DD_PROFILING_ENABLED`, `DD_RUNTIME_METRICS_ENABLED`, `DD_LOGS_INJECTION`, `ECS_FARGATE`
