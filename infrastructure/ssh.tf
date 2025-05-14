
resource "aws_security_group" "allow_ssh" {
  name        = "sg_allow_ssh"
  description = "Allow SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${local.project} - ${local.config.env} - SG to allow SSH"
    Project = local.project
    Env     = local.config.env
  }
}

resource "aws_key_pair" "main" {
  key_name   = "${local.config.env} - fibonapi"
  public_key = file("~/.ssh/fibonapi/${local.config.env}.pub")

  tags = {
    Name    = "${local.project} - ${local.config.env} - SSH Key Pair"
    Project = local.project
    Env     = local.config.env
  }
}
