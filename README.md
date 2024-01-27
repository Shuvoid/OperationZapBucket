# OperationZapBucket

## Description

This AWS SAM project focuses on compressing JSON files into ZIP files using gzip file compression. It deploys a Lambda function to handle the compression process. The compressed files are stored in an S3 bucket, and the corresponding JSON files are deleted to optimize storage.

## Prerequisites

Before getting started, ensure the following prerequisites are met:

- AWS CLI is installed and configured
- AWS SAM CLI is installed
- Python 3.10 is installed

## Folder Structure

The project is organized with the following structure:

- `src/`: Contains the source code for the AWS Lambda function.
  - `lambda_function.py`: Main Lambda function code responsible for compressing JSON files into ZIP format.
  - `utilities.py`: Utility module with common functions used by the Lambda function.

- `.gitignore`: Specifies which files and directories should be ignored by Git.

- `LICENSE`: The license file, indicating the terms under which the project is distributed. This project is licensed under the MIT License.

- `README.md`: This documentation file providing information about this project.

- `template.yaml`: AWS SAM template file defining the infrastructure for this serverless application.

This structure is designed to keep the code organized and modular, separating the Lambda function code from utility functions and the SAM template for infrastructure definition.

## Deployment

1. Clone this repository.
2. Navigate to the project directory.

```bash
cd OperationZapBucket

# This will validate the SAM template configuration
sam validate --lint

# Run the following command to deploy the SAM application. Replace "BucketName" with your desired S3 bucket name.
sam deploy --template-file template.yaml --stack-name StackName --s3-bucket BucketName

```

## Usage

After deployment, whenever a new JSON file is added to the S3 bucket, the Lambda function will be triggered to compress the file into a ZIP format.

## AWS Resources Created

1. S3 bucket for storing compressed files
2. Lambda function for handling file compression

## Cost Analysis

### Estimation

1. Lambda Function Costs:

Execution Cost: Assuming an execution time of 1 second per file:

> 1,000,000 executions/hour * 1 hour * $0.00001667 (per GB-second) = $16.67

Data Transfer Costs: Assuming minimal data transfer within the same region (intra-region), so the cost is minimal.

2. S3 Storage Costs:
> 1,000,000 files/hour * 10 MB/file * 1 hour * 30 days * $0.023/GB-month = $690,000

**Total Monthly Cost:**
> Lambda Execution Cost + S3 Storage Cost = $16.67 + $690,000 = $690,016.67

## Suggestions for Cost Savings

1. Use S3 Lifecycle Policies: Implement S3 lifecycle policies to automatically transition older files to cheaper storage classes like Amazon S3 Glacier or Glacier Deep Archive if fast access is not required or even the files can be deleted permanently after a time period. It will save the storage cost a lot.
2. Reserved Capacity: Consider Reserved Capacity for Lambda if the workload is predictable and consistent. This can provide cost savings compared to on-demand pricing.
