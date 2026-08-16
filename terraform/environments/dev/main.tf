module "ecr" {
  source = "../../modules/ecr"

  repository_name = "customer-churn-api"
}

output "ecr_repository_url" {
  value = module.ecr.repository_url
}
