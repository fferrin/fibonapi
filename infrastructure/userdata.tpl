#!/bin/sh
set -ex
sudo apt-get update

# Install Docker and Docker Compose
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor --yes -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin docker-compose
sudo groupadd docker
sudo usermod -aG docker $USER

sudo apt-get install gnupg2 pass

# Mount EBS for the database in /mnt/db
sudo mkfs.ext4 /dev/nvme1n1
sudo mkdir /mnt/db
echo "/dev/nvme1n1 /mnt/db ext4 defaults 0 0" | sudo tee -a /etc/fstab
sudo mount -a

# Install CloudWatch agent
wget https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i -E amazon-cloudwatch-agent.deb
sudo rm amazon-cloudwatch-agent.deb
sudo tee /opt/aws/amazon-cloudwatch-agent/bin/config.json > /dev/null <<EOF
{
  "agent": {
    "metrics_collection_interval": 60,
    "run_as_user": "cwagent",
    "logfile": "/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log"
  },
  "metrics": {
    "aggregation_dimensions": [["InstanceId"]],
    "metrics_collected": {
      "disk": {
        "measurement": [
          {"name": "used_percent", "rename": "EBSDiskUsagePercentage"}
        ],
        "metrics_collection_interval": 60,
        "resources": [
          "/",
          "/dev/shm"
        ]
      }
    }
  }
}
EOF

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s
sudo systemctl enable amazon-cloudwatch-agent
