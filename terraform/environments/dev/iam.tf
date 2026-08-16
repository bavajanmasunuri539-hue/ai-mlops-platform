module "iam" {
  source = "../../modules/iam"

  role_name             = "CustomerChurnEC2ECRPullRole"
  instance_profile_name = "CustomerChurnEC2ECRPullProfile"
}

output "iam_role_name" {
  value = module.iam.role_name
}

output "instance_profile_name" {
  value = module.iam.instance_profile_name
}
