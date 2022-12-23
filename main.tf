provider "archive" {}

data "aws_caller_identity" "current" {}

data "archive_file" "decompressor_object" {
  type        = "zip"
  source_file = "${path.module}/config/s3-decompressor.py"
  output_path = "${path.module}/config/s3-decompressor.zip"
}

module "lambda" {
  source  = "cloudposse/lambda-function/aws"
  version = "0.4.1"

  custom_iam_policy_arns = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/lambda-s3-decompressor-access-${var.bucket_name}"]
  filename               = data.archive_file.decompressor_object.output_path
  function_name          = "decompress-object"
  handler                = "s3-decompressor.lambda_handler"
  runtime                = "python3.7"
  timeout                = 30

  depends_on = [
    aws_iam_policy.s3-access
  ]
}

resource "aws_iam_policy" "s3-access" {
  name        = "lambda-s3-decompressor-access-${var.bucket_name}"
  path        = "/"
  description = "Allow the Lambda S3 decompressor to get and upload files for the '${var.bucket_name}' bucket"
  policy      = data.aws_iam_policy_document.s3-access.json
}

data "aws_iam_policy_document" "s3-access" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
      "s3:PutObject"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:s3:::${var.bucket_name}",
      "arn:aws:s3:::${var.bucket_name}/*"
    ]
  }
}
