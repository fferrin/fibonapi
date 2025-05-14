
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name    = "${local.project} - ${local.config.env} - VPC"
    Project = local.project
    Env     = local.config.env
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name    = "${local.project} - ${local.config.env} - VPC <-> Internet Gateway"
    Project = local.project
    Env     = local.config.env
  }
}

resource "aws_route_table" "main" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name    = "${local.project} - ${local.config.env} - Public Subnet Route Table."
    Project = local.project
    Env     = local.config.env
  }
}

resource "aws_security_group" "allow_http" {
  name        = "sg_allow_http"
  description = "Allow HTTP/HTTPS"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
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
    Name    = "${local.project} - ${local.config.env} - SG to allow HTTP and HTTPS"
    Project = local.project
    Env     = local.config.env
  }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.0.0/24"
  availability_zone = local.config.availability_zone

  tags = merge(
    local.tags,
    { Name = "${local.config.env} - Public Subnet" }
  )
}

resource "aws_route_table_association" "subnet_to_rt" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.main.id
}
