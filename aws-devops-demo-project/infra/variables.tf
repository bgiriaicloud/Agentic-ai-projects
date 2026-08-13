variable "region" {
  type        = string
  description = "The target AWS region"
  default     = "us-east-1"
}

variable "repository_id" {
  type        = string
  description = "The ID of the ECR repository"
  default     = "aws-devops-demo-repo"
}

variable "service_name" {
  type        = string
  description = "The name of the App Runner service"
  default     = "aws-devops-demo-app"
}

variable "image_tag" {
  type        = string
  description = "The container tag to deploy"
  default     = "latest"
}

variable "custom_welcome_message" {
  type        = string
  description = "Custom message environment variable for App Runner"
  default     = "Hello from AWS App Runner (Deployed via Terraform & CI/CD)!"
}
