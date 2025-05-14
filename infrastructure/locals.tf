locals {
  project             = "FibonAPI"

  workspaces = {
    prod = {
      env               = terraform.workspace
      region            = "us-east-1"
      availability_zone = "us-east-1a"
      disk_db_size      = 1
    }
  }

  config = local.workspaces[terraform.workspace]

  tags = {
    Project = local.project
    Env     = local.config.env
  }
}
