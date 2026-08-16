resource "aws_imagebuilder_component" "docker" {
  name     = "${var.project_name}-docker"
  platform = "Linux"
  version  = "1.0.2"

  data = <<-EOT
    name: Install Docker
    description: Install Docker for ML inference
    schemaVersion: 1.0

    phases:
      - name: build
        steps:
          - name: InstallDocker
            action: ExecuteBash
            inputs:
              commands:
                - apt-get update
                - apt-get install -y docker.io
                - systemctl enable docker
                - systemctl start docker
                - usermod -aG docker ubuntu
  EOT

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
