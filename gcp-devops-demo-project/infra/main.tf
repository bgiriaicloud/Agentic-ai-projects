terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Artifact Registry Repository to store container images
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.repository_id
  description   = "Docker registry for GCP DevOps Demo application"
  format        = "DOCKER"

  docker_config {
    immutable_tags = false
  }
}

# 2. Cloud Run Service running the container
resource "google_cloud_run_v2_service" "web_app" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/${var.image_name}:${var.image_tag}"

      ports {
        container_port = 8080 // Standard Node.js port for Cloud Run
      }

      resources {
        limits = {
          cpu    = "1.0"
          memory = "512Mi"
        }
      }

      env {
        name  = "NODE_ENV"
        value = "production"
      }
      env {
        name  = "CUSTOM_WELCOME_MESSAGE"
        value = var.custom_welcome_message
      }
    }
  }

  traffic {
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

  depends_on = [google_artifact_registry_repository.repo]
}

# 3. IAM Policy to allow public (unauthenticated) traffic to Cloud Run
resource "google_cloud_run_v2_service_iam_member" "noauth" {
  location = google_cloud_run_v2_service.web_app.location
  name     = google_cloud_run_v2_service.web_app.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
