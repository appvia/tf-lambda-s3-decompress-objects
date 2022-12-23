provider "archive" {}

data "archive_file" "decompressor_object" {
  type        = "zip"
  source_file = "${path.module}/config/s3-decompressor.py"
  output_path = "${path.module}/config/s3-decompressor.zip"
}


module "lambda" {
  source  = "cloudposse/lambda-function/aws"
  version = "0.4.1"

  filename      = data.archive_file.decompressor_object.output_path
  handler       = "s3-decompressor.lambda_handler"
  runtime       = "python3.7"
  timeout       = 30
  function_name = "decompress-object"
}
