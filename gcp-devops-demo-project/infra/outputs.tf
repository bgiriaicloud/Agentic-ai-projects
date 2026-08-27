output "cloud_run_url" {
  value       = google_cloud_run_v2_service.web_app.uri
  description = "The public URL of the deployed Cloud Run web application"
}

output "artifact_registry_endpoint" {
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}"
  description = "The Docker registry path to push images to"
}
