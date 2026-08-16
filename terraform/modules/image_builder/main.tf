variable "project_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "instance_profile_name" {
  type = string
}

variable "subnet_id" {
  type = string
}

variable "security_group_id" {
  type = string
}

resource "aws_iam_role" "image_builder" {
  name = "${var.project_name}-image-builder-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect = "Allow"

      Principal = {
        Service = "ec2.amazonaws.com"
      }

      Action = "sts:AssumeRole"
    }]
  })

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_iam_role_policy_attachment" "image_builder" {
  role       = aws_iam_role.image_builder.name
  policy_arn = "arn:aws:iam::aws:policy/EC2InstanceProfileForImageBuilder"
}

resource "aws_iam_instance_profile" "image_builder" {
  name = "${var.project_name}-image-builder-profile"
  role = aws_iam_role.image_builder.name
}

resource "aws_imagebuilder_image_recipe" "this" {
  name         = "${var.project_name}-recipe"
  version      = "1.0.0"
  parent_image = "ami-07e5ce642bbc48c0d"

  component {
    component_arn = aws_imagebuilder_component.docker.arn
  }

  block_device_mapping {
    device_name = "/dev/sda1"

    ebs {
      volume_size           = 20
      volume_type           = "gp3"
      delete_on_termination = true
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_imagebuilder_infrastructure_configuration" "this" {
  name                  = "${var.project_name}-infra"
  instance_profile_name = aws_iam_instance_profile.image_builder.name

  # Use a low-vCPU instance to stay within the current EC2 vCPU quota.
  instance_types = ["t3.micro"]

  subnet_id                     = var.subnet_id
  security_group_ids            = [var.security_group_id]
  terminate_instance_on_failure = true

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_imagebuilder_distribution_configuration" "this" {
  name = "${var.project_name}-distribution"

  distribution {
    region = "ap-south-1"

    ami_distribution_configuration {
      name = "${var.project_name}-{{ imagebuilder:buildDate }}"
    }
  }

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

resource "aws_imagebuilder_image_pipeline" "this" {
  name                             = "${var.project_name}-pipeline"
  image_recipe_arn                 = aws_imagebuilder_image_recipe.this.arn
  infrastructure_configuration_arn = aws_imagebuilder_infrastructure_configuration.this.arn
  distribution_configuration_arn   = aws_imagebuilder_distribution_configuration.this.arn

  schedule {
    schedule_expression                = "cron(0 0 ? * SUN *)"
    pipeline_execution_start_condition = "EXPRESSION_MATCH_AND_DEPENDENCY_UPDATES_AVAILABLE"
  }

  status = "ENABLED"

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}

output "pipeline_arn" {
  value = aws_imagebuilder_image_pipeline.this.arn
}

output "recipe_arn" {
  value = aws_imagebuilder_image_recipe.this.arn
}

output "component_arn" {
  value = aws_imagebuilder_component.docker.arn
}
