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

## Application Setup

Docker is the supported way to run Loggy.

1. Build the Docker image
```bash
./build.sh
```

2. Create config file
``` bash
mkdir ~/.loggy
cp config.template.json ~/.loggy/config.json
```

3. Update config with DynamoDB table names
Open the DynamoDB service in the AWS console and find the tables created for Loggy by the AWS SAM template.
Update the Loggy config file accordingly.

4. Add bash function to your bash profile for convenience
```bash
function loggy {
  docker run --rm -it -v "${HOME}/.loggy:/etc/loggy" -v "${HOME}/.aws:/root/.aws" loggy:latest "${@:1}"
}
```
