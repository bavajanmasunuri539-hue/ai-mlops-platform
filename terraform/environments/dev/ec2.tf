module "ec2" {
  source = "../../modules/ec2"

  ami_id                = var.ami_id
  instance_type         = var.instance_type
  key_name              = var.key_name
  subnet_id             = var.subnet_id
  security_group_id     = "sg-0f96eeb30d6646ae9"
  instance_profile_name = module.iam.instance_profile_name
  project_name          = var.project_name
  environment           = var.environment
}

output "ec2_instance_id" {
  value = module.ec2.instance_id
}

output "ec2_public_ip" {
  value = module.ec2.public_ip
}

output "ec2_private_ip" {
  value = module.ec2.private_ip
}
