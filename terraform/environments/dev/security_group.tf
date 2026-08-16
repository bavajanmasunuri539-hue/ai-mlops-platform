module "security_group" {
  source = "../../modules/security_group"

  name        = "customer-churn-inference-sg"
  description = "Security group for Customer Churn ML inference"
  vpc_id      = var.vpc_id
  ssh_cidr    = "27.6.132.181/32"
}

output "security_group_id" {
  value = module.security_group.security_group_id
}
