# AWS CLI (`aws`) Cheat Sheet

This cheat sheet provides a comprehensive reference for the most commonly used AWS CLI (`aws`) commands, organized by service categories.

---

## 1. Configuration & Authentication

Configure your CLI credentials, named profiles, and region defaults.

| Command | Description |
| :--- | :--- |
| `aws configure` | Interactive setup to configure Access Key, Secret Key, Default Region, and Output format. |
| `aws configure set <name> <value>` | Set a specific configuration parameter (e.g. `aws configure set region us-east-1`). |
| `aws configure list` | View active configuration settings and where they are sourced from. |
| `aws configure --profile <profile-name>` | Configure a named profile with separate credentials. |
| `aws sts get-caller-identity` | Verify active credentials (returns Account ID, Arn, and User ID). |
| `aws identity login` | SSO login interactive prompt (when configured via AWS IAM Identity Center). |

---

## 2. Elastic Compute Cloud (`aws ec2`)

Manage Virtual Servers (Instances), Security Groups, and AMI Key Pairs.

```bash
# Launch a Linux VM (Amazon Linux 2023)
aws ec2 run-instances \
  --image-id ami-04b70fa74e45c3917 \
  --count 1 \
  --instance-type t3.micro \
  --key-name my-keypair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0

# List instances (in table format displaying ID, Type, State, and Public IP)
aws ec2 describe-instances --query "Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType,State:State.Name,PublicIP:PublicIpAddress}" --output table

# Start, Stop, and Terminate (delete) an EC2 Instance
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0

# Create a Key Pair and save the private key locally
aws ec2 create-key-pair --key-name my-keypair --query 'KeyMaterial' --output text > my-keypair.pem
chmod 400 my-keypair.pem
```

---

## 3. Simple Storage Service (`aws s3` & `aws s3api`)

Manage S3 Buckets and objects.

```bash
# Create an S3 Bucket (must be globally unique)
aws s3 mb s3://my-unique-bucket-name --region us-east-1

# Upload a local file to a bucket
aws s3 cp /path/to/local/file.txt s3://my-unique-bucket-name/uploads/

# List objects inside a bucket
aws s3 ls s3://my-unique-bucket-name --recursive

# Download an object from a bucket
aws s3 cp s3://my-unique-bucket-name/uploads/file.txt /path/to/downloaded/

# Sync a local directory with a bucket (uploads modified/new files)
aws s3 sync /my/local/folder s3://my-unique-bucket-name/backup/

# Delete an object
aws s3 rm s3://my-unique-bucket-name/uploads/file.txt

# Delete a bucket (must be empty first or use --force)
aws s3 rb s3://my-unique-bucket-name --force
```

---

## 4. Virtual Private Cloud (VPC) Networking

Manage networks, subnets, and security rules.

```bash
# Create a VPC
aws ec2 create-vpc --cidr-block 10.0.0.0/16 --query 'Vpc.VpcId' --output text

# Create a Subnet in an existing VPC
aws ec2 create-subnet --vpc-id vpc-0123456789abcdef0 --cidr-block 10.0.1.0/24 --query 'Subnet.SubnetId' --output text

# Create a Security Group
aws ec2 create-security-group \
  --group-name web-security-group \
  --description "Web Security Group allowing HTTP/SSH" \
  --vpc-id vpc-0123456789abcdef0

# Authorize inbound SSH (port 22) rule on a security group
aws ec2 authorize-security-group-ingress \
  --group-id sg-0123456789abcdef0 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

---

## 5. Identity & Access Management (`aws iam`)

Manage users, roles, policies, and permissions.

```bash
# Create an IAM User
aws iam create-user --user-name deployer-user

# Attach AdministratorAccess managed policy to user (dangerous, use caution!)
aws iam attach-user-policy --user-name deployer-user --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# Create an IAM Role for EC2 using a trust policy JSON
aws iam create-role --role-name my-ec2-role --assume-role-policy-document file://trust-policy.json

# Create and download Access Keys for an IAM user (sensitive!)
aws iam create-access-key --user-name deployer-user
```

---

## 6. Containers & Serverless (`aws ecr`, `aws ecs` & `aws lambda`)

Manage container registries, clusters, and lambda functions.

### Elastic Container Registry (`aws ecr`)

```bash
# Create an ECR repository
aws ecr create-repository --repository-name my-devops-app --region us-east-1

# Authenticate Docker CLI to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

### Lambda Serverless (`aws lambda`)

```bash
# Create a Lambda function (zipping the code first)
zip function.zip index.js
aws lambda create-function \
  --function-name my-lambda-function \
  --runtime nodejs18.x \
  --zip-file fileb://function.zip \
  --handler index.handler \
  --role arn:aws:iam::123456789012:role/my-lambda-execution-role

# Invoke a Lambda function manually
aws lambda invoke --function-name my-lambda-function response.json
```

---

## 7. Relational Database Service (`aws rds`)

Manage databases.

```bash
# Provision a PostgreSQL DB Instance (t3.micro tier)
aws rds create-db-instance \
  --db-instance-identifier my-postgres-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --allocated-storage 20 \
  --master-username rdsadmin \
  --master-user-password "SecurePassword123!"

# List RDS DB instances
aws rds describe-db-instances --query "DBInstances[*].{ID:DBInstanceIdentifier,Class:DBInstanceClass,Engine:Engine,Status:DBInstanceStatus}" --output table
```

---

## 8. CloudWatch Monitoring (`aws logs`)

Tail and inspect system logs.

```bash
# List CloudWatch Log Groups
aws logs describe-log-groups --query "logGroups[*].logGroupName" --output table

# Tail logs in real-time from a log group
aws logs tail /aws/lambda/my-lambda-function --follow
```
