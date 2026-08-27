variable "project_id" {
  type        = string
  description = "The GCP Project ID where resources will be deployed"
}

variable "region" {
  type        = string
  description = "The target GCP region"
  default     = "us-central1"
}

variable "repository_id" {
  type        = string
  description = "The ID of the Artifact Registry repository"
  default     = "gcp-devops-demo-repo"
}

variable "service_name" {
  type        = string
  description = "The name of the Cloud Run service"
  default     = "gcp-devops-demo-app"
}

variable "image_name" {
  type        = string
  description = "The image name inside the repository"
  default     = "web-dashboard"
}

variable "image_tag" {
  type        = string
  description = "The container tag to deploy"
  default     = "latest"
}

variable "custom_welcome_message" {
  type        = string
  description = "Custom message environment variable for Cloud Run"
  default     = "Hello from Google Cloud Run (Deployed via Terraform & CI/CD)!"
}
