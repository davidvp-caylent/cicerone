# Beer Tasting Agent - Deployment Guide

This guide explains how to deploy the Beer Tasting Agent to Amazon Bedrock AgentCore Runtime.

## Prerequisites

Before deploying, ensure you have:

- An AWS account with appropriate [AgentCore permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-permissions.html)
- Python 3.10+
- AWS CLI configured with credentials
- `bedrock-agentcore` package installed

## Environment Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Update the `.env` file with your AWS configuration:
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
BEDROCK_MODEL_ID=us.anthropic.claude-sonnet-4-5-20250929-v1:0
```

## Deployment Options

### Option A: Quick Deployment with Starter Toolkit (Recommended for Prototyping)

1. Install the starter toolkit:
```bash
pip install bedrock-agentcore-starter-toolkit
```

2. Configure your agent:
```bash
agentcore configure --entrypoint app.py
```

3. (Optional) Test locally:
```bash
agentcore launch --local
```

4. Deploy to AWS:
```bash
agentcore launch
```

5. Test your deployed agent:
```bash
agentcore invoke '{"prompt": "Hola, quiero hacer una cata de cerveza"}'
```

### Option B: Manual Deployment with boto3

For more control over the deployment process:

1. Package your code as a container image (see Docker section below)

2. Push to Amazon ECR:
```bash
# Create ECR repository
aws ecr create-repository --repository-name beer-tasting-agent --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker buildx build --platform linux/arm64 -t <account-id>.dkr.ecr.us-east-1.amazonaws.com/beer-tasting-agent:latest --push .
```

3. Create the agent runtime using boto3:
```python
import boto3

client = boto3.client('bedrock-agentcore-control', region_name='us-east-1')

response = client.create_agent_runtime(
    agentRuntimeName='beer-tasting-agent',
    agentRuntimeArtifact={
        'containerConfiguration': {
            'containerUri': '<account-id>.dkr.ecr.us-east-1.amazonaws.com/beer-tasting-agent:latest'
        }
    },
    networkConfiguration={"networkMode": "PUBLIC"},
    roleArn='arn:aws:iam::<account-id>:role/AgentRuntimeRole'
)

print(f"Agent Runtime ARN: {response['agentRuntimeArn']}")
```

## Local Testing

To test the agent locally before deployment:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the agent
python app.py

# In another terminal, test with curl:
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hola, quiero información sobre cervezas"}'
```

## Docker Deployment (Option B)

If you need to create a custom Docker image:

1. Create a `Dockerfile`:
```dockerfile
FROM --platform=linux/arm64 python:3.13-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "app.py"]
```

2. Build and test locally:
```bash
docker buildx build --platform linux/arm64 -t beer-tasting-agent:arm64 --load .

docker run --platform linux/arm64 -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID" \
  -e AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY" \
  -e AWS_REGION="$AWS_REGION" \
  beer-tasting-agent:arm64
```

## Invoking the Deployed Agent

Once deployed, you can invoke the agent using boto3:

```python
import boto3
import json

client = boto3.client('bedrock-agentcore', region_name='us-east-1')

payload = json.dumps({
    "prompt": "Hola, quiero hacer una cata de cerveza"
}).encode()

response = client.invoke_agent_runtime(
    agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:<account-id>:runtime/beer-tasting-agent-<suffix>',
    runtimeSessionId='unique-session-id-at-least-33-chars-long',
    payload=payload
)

response_body = response['response'].read()
result = json.loads(response_body)
print(result['response'])
```

## Payload Format

The agent expects the following payload format:

```json
{
  "prompt": "User message here",
  "session_id": "optional-session-id",
  "user_id": "optional-user-id"
}
```

Response format:

```json
{
  "response": "Agent response text",
  "session_id": "session-id",
  "status": "success",
  "metadata": {
    "beers_tasted_count": 0,
    "has_preference_profile": false,
    "message_count": 2
  }
}
```

## Monitoring and Observability

To enable observability for your agent:

1. Enable CloudWatch Transaction Search in the AWS Console
2. Add ADOT to requirements.txt (already included)
3. Run with auto-instrumentation:
```bash
opentelemetry-instrument python app.py
```

4. View metrics in CloudWatch Console under GenAI Observability

## Troubleshooting

### Common Issues

**Import Error: No module named 'bedrock_agentcore'**
- Solution: Install the package: `pip install bedrock-agentcore`

**AWS Credentials Not Found**
- Solution: Configure AWS CLI or set environment variables:
  ```bash
  export AWS_ACCESS_KEY_ID=your_key
  export AWS_SECRET_ACCESS_KEY=your_secret
  export AWS_REGION=us-east-1
  ```

**Agent Not Responding**
- Check CloudWatch logs for errors
- Verify IAM role permissions
- Ensure the agent runtime is in ACTIVE state

**Session State Not Persisting**
- Verify session_id is being passed correctly
- Check that session_manager is working (test locally first)

## Additional Resources

- [Amazon Bedrock AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/what-is-bedrock-agentcore.html)
- [Strands Agents Documentation](https://strandsagents.com/latest/)
- [AgentCore Deployment Guide](https://strandsagents.com/latest/documentation/docs/user-guide/deploy/deploy_to_bedrock_agentcore/)
