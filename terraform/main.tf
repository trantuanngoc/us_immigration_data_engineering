terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
    redshift = {
      source  = "brainly/redshift"
      version = "1.0.2"
    }
  }
  required_version = ">= 1.2.0"
}

provider "aws" {
  region  = var.aws_region
  profile = "default"
}

# Create our S3 bucket (Datalake)
resource "aws_s3_bucket" "sde-data-lake" {
  bucket_prefix = var.bucket_prefix
  force_destroy = true
}

# Create zone 
resource "aws_s3_object" "landing-zone" {
  bucket = aws_s3_bucket.sde-data-lake.id
  key = "landing-zone/"
}
resource "aws_s3_object" "staging-zone" {
  bucket = aws_s3_bucket.sde-data-lake.id
  key = "staging-zone/"
}
resource "aws_s3_object" "processed-zone" {
  bucket = aws_s3_bucket.sde-data-lake.id
  key = "processed-zone/"
}

#Create key pair
resource "tls_private_key" "pk" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "kp" {
  key_name   = "myKey"       
  public_key = tls_private_key.pk.public_key_openssh

  provisioner "local-exec" { 
    command = "echo '${tls_private_key.pk.private_key_pem}' > ./myKey.pem"
  }
}

# IAM role for EC2 to connect to AWS Redshift, S3, & EMR
resource "aws_iam_role" "sde_ec2_iam_role" {
  name = "sde_ec2_iam_role"
  assume_role_policy = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })

  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3FullAccess", "arn:aws:iam::aws:policy/AmazonElasticMapReduceFullAccess", "arn:aws:iam::aws:policy/AmazonRedshiftAllCommandsFullAccess"]
}

resource "aws_iam_instance_profile" "sde_ec2_iam_role_instance_profile" {
  name = "sde_ec2_iam_role_instance_profile"
  role = aws_iam_role.sde_ec2_iam_role.name
}

# IAM role for Redshift to be able to read data from S3 via Spectrum
resource "aws_iam_role" "sde_redshift_iam_role" {
  name = "sde_redshift_iam_role"
  assume_role_policy = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "redshift.amazonaws.com"
        }
      },
    ]
  })
  managed_policy_arns = ["arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"]
}

# Create security group for access to EC2 from your Anywhere
resource "aws_security_group" "sde_security_group" {
  name        = "sde_security_group"
  description = "Security group to allow inbound SCP & outbound 8080 (Airflow) connections"
  ingress {
    description = "Inbound SCP"
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

  egress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sde_security_group"
  }
}

# Create iam role for emr
resource "aws_iam_role" "sde_emr_iam_role" {
  name               = "sde_emr_iam_role"
  assume_role_policy = jsonencode({
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "elasticmapreduce.amazonaws.com"
        }
      },
    ]
  })

  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"]
}

resource "aws_iam_role" "sde_emr_instance_profile_role" {
  name               = "sde_emr_instance_profile_role"
  assume_role_policy = <<EOF
    {
      "Statement": [
        {
          "Action": [
            "sts:AssumeRole"
          ],
          "Effect": "Allow",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          }
        }
      ]
    }
  EOF
  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceforEC2Role",
    "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  ]
}

resource "aws_iam_instance_profile" "sde_emr_iam_role_instance_profile" {
  name = "sde_emr_role_instance_profile"
  role = aws_iam_role.sde_emr_instance_profile_role.name
}

resource "aws_default_subnet" "default_ue1a" {
  availability_zone = "us-east-1a"
}

#Set up EMR
resource "aws_emr_cluster" "sde_emr_cluster" {
  name                   = "sde_emr_cluster"
  release_label          = "emr-6.2.0"
  applications           = ["Spark"]
  scale_down_behavior    = "TERMINATE_AT_TASK_COMPLETION"
  service_role           = aws_iam_role.sde_emr_iam_role.arn
  termination_protection = false
  auto_termination_policy {
    idle_timeout = var.auto_termination_timeoff
  }
  log_uri = "s3://aws-logs-245844301530-us-east-1"
  ec2_attributes {
    subnet_id        = aws_default_subnet.default_ue1a.id
    instance_profile = aws_iam_instance_profile.sde_emr_iam_role_instance_profile.arn
    key_name         = aws_key_pair.kp.key_name
  }

  master_instance_group {
    instance_type  = var.emr_instance_type
    instance_count = 1
    name           = "Master - 1"

    ebs_config {
      size                 = 32
      type                 = "gp2"
      volumes_per_instance = 2
    }
  }

  core_instance_group {
    instance_type  = var.emr_instance_type
    instance_count = 2
    name           = "Core - 2"

    ebs_config {
      size                 = "32"
      type                 = "gp2"
      volumes_per_instance = 2
    }
  }
}

resource "aws_security_group" "reds_security_group" {
  name        = "reds_security_group"
  ingress {
    from_port        = 5432
    to_port          = 5432
    security_groups  = [aws_security_group.sde_security_group.id]
    protocol         = "tcp"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "reds_security_group"
  }
}

# Set up Redshift
resource "aws_redshift_cluster" "sde_redshift_cluster" {
  cluster_identifier  = "sde-redshift-cluster"
  master_username     = var.redshift_user
  master_password     = var.redshift_password
  port                = 5439
  node_type           = var.redshift_node_type
  cluster_type        = "single-node"
  iam_roles           = [aws_iam_role.sde_redshift_iam_role.arn]
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.reds_security_group.id]
}

# Create Redshift schema
provider "redshift" {
  host     = aws_redshift_cluster.sde_redshift_cluster.dns_name
  username = var.redshift_user
  password = var.redshift_password
  database = "dev"
}

# Create EC2 with IAM role to allow EMR, Redshift, & S3 access and security group 
resource "tls_private_key" "custom_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name_prefix = var.key_name
  public_key      = tls_private_key.custom_key.public_key_openssh
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20220420"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] 
}





resource "aws_instance" "sde_ec2" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = var.ec2_instance_type

  key_name             = aws_key_pair.kp.key_name
  security_groups      = [aws_security_group.sde_security_group.name]
  iam_instance_profile = aws_iam_instance_profile.sde_ec2_iam_role_instance_profile.id
  tags = {
    Name = "sde_ec2"
  }

  user_data = <<EOF
#!/bin/bash
sudo apt-get -y update
sudo apt-get install pip3-python -y
sudo apt-get install python3.10-venv -y
cd /home/ubuntu
touch env
echo "
AIRFLOW_CONN_POSTGRES_DEFAULT=postgres://airflow:airflow@localhost:5439/airflow
AIRFLOW_CONN_AWS_DEFAULT=aws://?region_name=${var.aws_region}
AIRFLOW_VAR_EMR_ID=${aws_emr_cluster.sde_emr_cluster.id}
AIRFLOW_VAR_BUCKET=${aws_s3_bucket.sde-data-lake.id}
" > env

EOF
}

