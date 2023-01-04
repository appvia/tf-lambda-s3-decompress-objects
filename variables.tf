################################################################################
# Required Variables
################################################################################

variable "bucket_name" {
  description = "The name of the S3 bucket to grant access to"
  type        = string
}

variable "timeout" {
  type        = number
  description = "The amount of time the Lambda Function has to run in seconds."
  default     = 30
}
