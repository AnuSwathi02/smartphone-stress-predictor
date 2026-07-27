# Simple AWS + Docker + Terraform Deployment

This is the simplest version of your assignment:

1. Push this whole project to GitHub
2. Use Terraform to create one AWS EC2 virtual machine
3. Let the VM install Docker and Docker Compose automatically
4. Let the VM clone your GitHub repo and start the containers
5. Expose the app to the internet through Nginx on port `80`
6. Access the app through the VM's public IP

## Why this is a correct problem statement

Yes, your refined statement is correct:

"Design and implement an end-to-end DevOps pipeline that provisions a virtual machine on a cloud platform entirely through code, containerizes an existing application using Docker, automatically deploys it to the provisioned virtual machine, exposes it publicly, and stores the complete source code, infrastructure code, and deployment scripts in GitHub."

For your project, we are using:

- Cloud: AWS
- Infrastructure as Code: Terraform
- Containerization: Docker
- Reverse Proxy: Nginx
- Hosting target: EC2 virtual machine
- Source control: GitHub

## What to push to GitHub

Push the full project, including:

- `app.py`
- `Dockerfile`
- `requirements.txt`
- `mobile_addiction_data.csv`
- `stress_model.pkl`
- `templates/`
- `static/`
- `deploy/`
- `infra/terraform/`

## Prerequisites

Install locally:

- AWS CLI
- Terraform
- Git

Then configure AWS credentials:

```bash
aws configure
```

## Step 1: Create a GitHub repo and push the project

From the project folder:

```bash
git init
git add .
git commit -m "Initial patent app with Docker and Terraform deployment"
git branch -M main
git remote add origin https://github.com/your-username/your-repo.git
git push -u origin main
```

## Step 2: Prepare Terraform variables

Go into:

```bash
cd infra/terraform
```

Edit `terraform.tfvars` and set:

- your GitHub repository URL
- your AWS region
- optional EC2 key pair name

Example:

```hcl
aws_region    = "ap-south-1"
project_name  = "patent-app"
instance_type = "t3.micro"
app_repo_url  = "https://github.com/your-username/your-repo.git"
app_branch    = "main"
```

## Step 3: Deploy using Terraform

```bash
terraform init
terraform plan
terraform apply
```

After apply completes, Terraform will print:

- `public_ip`
- `application_url`

Open the `application_url` in your browser.

## How the deployment works

Terraform creates:

- one custom VPC
- one public subnet
- one internet gateway
- one route table and subnet association
- one EC2 instance
- one security group that opens ports `80` and `22`

When the VM starts, the startup script:

- installs Docker, Docker Compose, and Git
- clones your GitHub repo
- starts two containers with Docker Compose
- exposes Nginx on port `80`
- forwards Nginx traffic to the Flask app container on port `8000`

## Where Docker Lies In The Architecture

Docker runs inside the EC2 virtual machine.

The runtime layering is:

1. AWS provides the EC2 virtual machine
2. Docker Engine runs on that VM
3. Docker Compose manages the containers on that VM
4. Nginx runs as one Docker container
5. Flask runs as another Docker container

So Docker is the platform inside the VM that hosts both application containers.

## How The Internet Exposure Works

Users on the internet call:

`http://<ec2-public-ip>`

Traffic flow:

1. Internet traffic reaches the custom VPC through the internet gateway
2. The route table sends public traffic into the public subnet
3. The EC2 VM in that subnet receives the request
4. AWS security group allows inbound HTTP traffic on port `80`
5. The Nginx container listens on port `80`
6. Nginx reverse proxies the request to the Flask app container on port `8000`

This is why the app becomes publicly accessible without exposing Flask directly.

## Do We Need Nginx?

Strictly speaking, no. You could expose Flask directly with Docker port mapping.

But for your assignment, using Nginx is better because:

- it is a more realistic deployment pattern
- it cleanly handles public HTTP traffic
- it makes the architecture easier to explain in a viva/demo
- it keeps Flask behind a reverse proxy

## Important note about public GitHub repos

This setup is easiest if the GitHub repo is public.

If your repo is private, the VM cannot clone it with plain `git clone` unless you add authentication. For a minimal academic submission, a public repo is the simplest option.

## How to destroy everything later

```bash
terraform destroy
```
