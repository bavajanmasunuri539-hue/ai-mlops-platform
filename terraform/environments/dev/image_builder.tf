module "image_builder" {
  source = "../../modules/image_builder"

  project_name          = var.project_name
  environment           = var.environment
  instance_profile_name = module.iam.instance_profile_name
  subnet_id             = var.subnet_id
  security_group_id     = module.security_group.security_group_id
}

output "image_builder_pipeline_arn" {
  value = module.image_builder.pipeline_arn
}

output "image_builder_recipe_arn" {
  value = module.image_builder.recipe_arn
}

output "image_builder_component_arn" {
  value = module.image_builder.component_arn
}
