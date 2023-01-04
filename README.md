<!-- BEGIN_TF_DOCS -->
# tf-lambda-s3-decompress-objects

This module deploys a Lambda function which can be called via S3 Notifications, extracts zip files and uploads their contents back into S3.

When a file is uploaded to an S3 bucket, the Lambda function would receive an event similar to below:

```json
{
    "Records": [
      {
        "eventVersion": "2.1",
        "eventSource": "aws:s3",
        "awsRegion": "eu-west-2",
        "eventTime": "2022-12-22T00:00:00.000Z",
        "eventName": "ObjectCreated:Put",
        "userIdentity": {
          "principalId": "AWS:1234567890"
        },
        "requestParameters": {
          "sourceIPAddress": "192.0.2.0"
        },
        "responseElements": {
          "x-amz-request-id": "C3D13FE58DE4C810",
          "x-amz-id-2": "FMyUVURIY8/IgAtTv8xRjskZQpcIZ9KG4V5Wp6S7S/JRWeUWerMUE5JgHvANOjpD"
        },
        "s3": {
          "s3SchemaVersion": "1.0",
          "configurationId": "testConfigRule",
          "bucket": {
            "name": "my-test-bucket",
            "ownerIdentity": {
              "principalId": "A3NL1KOZZKExample"
            },
            "arn": "arn:aws:s3:::my-test-bucket"
          },
          "object": {
            "key": "input/mydir/myfiles.tar.gz",
            "size": 1024,
            "eTag": "d41d8cd98f00b204e9800998ecf8427e",
            "sequencer": "0055AED6DCD90281E5"
          }
        }
      }
    ]
}
```

The Lambda function will:
1. Download the `.tar.gz` file
2. Extract the contents
3. Loop through each `.log` file
4. Uploads the file(s) to S3 in an `output` directory

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_bucket_name"></a> [bucket\_name](#input\_bucket\_name) | The name of the S3 bucket to grant access to | `string` | n/a | yes |
| <a name="input_timeout"></a> [timeout](#input\_timeout) | The amount of time the Lambda Function has to run in seconds. | `number` | `30` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_arn"></a> [arn](#output\_arn) | ARN of the lambda function |
| <a name="output_function_name"></a> [function\_name](#output\_function\_name) | Lambda function name |
| <a name="output_invoke_arn"></a> [invoke\_arn](#output\_invoke\_arn) | Invoke ARN of the lambda function |
| <a name="output_qualified_arn"></a> [qualified\_arn](#output\_qualified\_arn) | ARN identifying your Lambda Function Version (if versioning is enabled via publish = true) |
| <a name="output_role_arn"></a> [role\_arn](#output\_role\_arn) | Lambda IAM role ARN |
| <a name="output_role_name"></a> [role\_name](#output\_role\_name) | Lambda IAM role name |
<!-- END_TF_DOCS -->
