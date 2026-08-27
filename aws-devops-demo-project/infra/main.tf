terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region
}

# 1. Elastic Container Registry (ECR) Repository to store container images
resource "aws_ecr_repository" "repo" {
  name                 = var.repository_id
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

# 2. IAM Role for AWS App Runner to pull images from ECR
resource "aws_iam_role" "apprunner_ecr_access" {
  name = "apprunner-ecr-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "build.apprunner.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "apprunner_ecr_policy" {
  role       = aws_iam_role.apprunner_ecr_access.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSAppRunnerServicePolicyForECRAccess"
}

# 3. AWS App Runner Service running the container
resource "aws_apprunner_service" "web_app" {
  service_name = var.service_name

  source_configuration {
    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.repo.repository_url}:${var.image_tag}"
      image_repository_type = "ECR"

      image_configuration {
        port = "8080" // Standard Node.js port for App Runner container
        runtime_environment_variables = {
          NODE_ENV               = "production"
          CUSTOM_WELCOME_MESSAGE = var.custom_welcome_message
        }
      }
    }

    auto_deployments_enabled = false
  }

  instance_configuration {
    cpu    = "1 vCPU"
    memory = "2 GB"
  }

  depends_on = [
    aws_ecr_repository.repo,
    aws_iam_role_policy_attachment.apprunner_ecr_policy
  ]
}
