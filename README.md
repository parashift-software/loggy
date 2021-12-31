# Loggy

AWS LogGroup-Kinesis Subscription Manager (CLI Tool)

## Initial AWS Setup

Loggy uses DynamoDB tables in AWS to store shared configurations for your organization.

1. Navigate to the `aws_setup` directory
```bash
cd aws_setup
```

2. Create a SAM (Serverless Application Model) config
```bash
# Copy from template
cp samconfig.example.toml samconfig.toml

# Update samconfig.toml
# Update attributes: s3_bucket (bucket to store cloudformation stack config in), and region
```

3. Build the SAM app
```bash
sam build
```

4. Deploy the SAM app
```bash
sam deploy
```
