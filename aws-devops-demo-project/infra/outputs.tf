output "app_runner_url" {
  value       = aws_apprunner_service.web_app.service_url
  description = "The public URL of the deployed App Runner web application"
}

output "ecr_repository_url" {
  value       = aws_ecr_repository.repo.repository_url
  description = "The ECR repository URL to push images to"
}
