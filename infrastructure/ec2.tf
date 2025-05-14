# IAM Execution Role
resource "aws_iam_role" "ec2_role" {
  name = "${local.config.env}-ec2-generic-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "cw_agent_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "${local.config.env}-ec2-instance-profile"
  role = aws_iam_role.ec2_role.name
}

# EC2 Instance
resource "aws_instance" "main" {
  ami                         = data.aws_ami.ubuntu_18_04.id
  instance_type               = "t3.micro"
  key_name                    = aws_key_pair.main.key_name
  vpc_security_group_ids      = [aws_security_group.allow_ssh.id, aws_security_group.allow_http.id]
  subnet_id                   = aws_subnet.public.id
  associate_public_ip_address = true
  user_data                   = file("userdata.tpl")

  iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

  # Enable IMDSv2
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
    instance_metadata_tags      = "enabled"
  }

  tags = merge(
    local.tags,
    { Name = "${local.config.env} - Backend" }
  )
}
