output "public_ip" {
  description = "Public IP of the application VM."
  value       = aws_instance.app.public_ip
}

output "application_url" {
  description = "HTTP URL for the deployed application."
  value       = "http://${aws_instance.app.public_ip}"
}

output "vpc_id" {
  description = "Custom VPC ID."
  value       = aws_vpc.app.id
}

output "public_subnet_id" {
  description = "Public subnet ID."
  value       = aws_subnet.public.id
}

output "private_key_path" {
  description = "Local path of the generated SSH private key."
  value       = local_sensitive_file.ssh_private_key.filename
}
