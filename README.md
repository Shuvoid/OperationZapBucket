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
sam deploy --template-file template.yaml --stack-name StackName --guided

```

## Usage

After deployment, whenever a new JSON file is added to the S3 bucket, the Lambda function will be triggered to compress the file into a ZIP format.

## AWS Resources Created

1. S3 bucket for storing compressed files
2. Lambda function for handling file compression

## Cost Analysis

### Estimation

1. Lambda Function Costs:

**Assumptions:**
1. Original file size: 10 MB per file
2. Compression reduces the file size by 50% (5 MB after compression)
3. Number of files processed per hour: 1,000,000
4. Lambda execution time: 1 second per file
5. AWS Lambda Memory Size: 1024 MB
6. AWS Lambda Pricing: $0.00001667 per GB-second
7. S3 Standard Storage Cost: $0.023/GB-month

**Calculations:**
Original Data Transfer Cost (without zipping):
> 1,000,000 files/hour * 10 MB/file * 1 hour * 30 days * $0.023/GB-month = $6,900,000

Estimated Data Transfer Cost (with zipping, assuming 50% reduction):
> 1,000,000 files/hour * 5 MB/file * 1 hour * 30 days * $0.023/GB-month = $3,450,000

Estimated Lambda Execution Cost (hourly):
> 1,000,000 executions/hour * 1 hour * $0.00001667 (per GB-second) = $16.67

Estimated Lambda Execution Cost (monthly):
> Estimated Lambda Execution Cost (hourly) * 730 hours = $16.67 * 730 = $12,151.10

**Total Estimated Monthly Cost:**
> Estimated Lambda Execution Cost (monthly) + Estimated Data Transfer Cost (with zipping) = $12,151.10 + $3,450,000 = $3,462,151.10

The total estimated monthly cost, considering both Lambda execution and data transfer with the zipping solution, is approximately $3,462,151.10. This estimation provides insights into the potential monthly costs for this specific use case based on the assumptions provided above.

### Cost Optimization Recommendations

1. **Optimizing Image Storage Costs with On-Demand Resizing:**
   - Implement an on-demand file compression strategy before getting stored into s3 bucket. This approach reduces data transfer cost during file compression in lambda and eliminate both the file processing task in lambda and re-uploading into s3 bucket.

2. **Leveraging S3 Lifecycle Policies for Storage Efficiency:**
   - By automating the transition of older files to cost-effective storage classes such as Amazon S3 Glacier or Glacier Deep Archive, storage costs can be managed strategically. Enabling Intelligent Tiering in Amazon S3 will monitor data access patterns in S3 and then migrates it to the most cost-effective storage class over time without human intervention

3. **Evaluating Reserved Capacity for Lambda:**
   - Consider exploring the benefits of Reserved Capacity for AWS Lambda if our workload demonstrates predictability and consistency. Reserved Capacity presents an opportunity for cost savings as it offers a fixed commitment for a specified duration, serving as a proactive measure against on-demand pricing fluctuations.

4. **Exploring Lambda Savings Plans for Consistent Cost Efficiency:**
   - Investigate the adoption of AWS Lambda Savings Plans based on our observed usage patterns. Savings Plans present an opportunity for substantial cost savings in comparison to standard on-demand pricing. By committing to a consistent amount of usage (measured in $/hr) for a 1 or 3-year period, a predictable discount can be secured, making this approach particularly beneficial for workloads with consistent Lambda usage.

5. **Lambda Power Tuning:**
  - To optimize memory and concurrency settings for better performance and cost efficiency. As CPU-bound Lambda functions see the most benefit when memory increases, so this will be a good use for this file compression task. So, by choosing the memory allocated to Lambda functions is an optimization process that balances execution speed (duration) and cost.

## Is this a scalable system?

The solution described above using AWS Lambda to compress and archive files in S3 is scalable to some extent, but there are potential bottlenecks and considerations that might impact the system's scalability and performance.

### Scalability:

1. **Lambda Scalability:**
   - AWS Lambda scales automatically by triggering multiple instances of the function in response to a high number of events. Each invocation of the function processes one file. Lambda can handle a large number of concurrent executions, making it suitable for processing a high volume of files.

2. **S3 Scalability:**
   - S3 is designed to scale automatically as the number of objects increases, making it suitable for storing a large number of compressed files.

### Potential Bottlenecks:

1. **Lambda Execution Time:**
   - Lambda has a time limit for how long it can work on a file (about 15 minutes). If the files are big or there are loads of them, it might hit that limit. We need to be mindful of that.

2. **Concurrency Limits:**
   - AWS Lambda has concurrency limits per region. If the volume of incoming files is very high, it may hit these limits which looks like a traffic jam for Lambda. It's important to monitor and consider adjusting the concurrent execution limits if necessary. A default AWS Lambda limit concurrency of 1,000 was put in place by AWS but this is soft limit and there are ways to overcome this limitation.

3. **S3 Event Rate:**
   - How quickly files are added to S3 can impact performance. If there's a very high rate of new files coming in, we need to make sure that Lambda can keep up and not fall behind.

4. **Resource Limits:**
   - AWS Lambda has resource limits, including memory and storage and CPU is tied to memory. Ensure that the Lambda function has enough resources to handle the compression of large files. AWS Lambda memory limit has been kept to a max of 3GB. It starts at 128 MB and can be increased by 64 MB increments. This memory is mostly sufficient for event-driven functions. However, there are times when we need CPU-intensive or logical calculation-based workloads and may cause timeout errors due to not being able to complete the execution in time as the hard time limit is 15 minutes.

6. **Retry Mechanism:**
   - Implement a retry mechanism in case the Lambda function fails to compress and upload a file. This ensures that no files are lost in case of transient failures.


### Recommendations:

1. We can consider breaking down the problem by using batch processing to optimize Lambda execution times and cost.
2. We can implement monitoring and alarm for any error happened during the file compression so that we can have a track and can get notified immediately.
3. We need to monitor Lambda function metrics and then adjust concurrency limits accordingly if required.

Overall, the architecture might need adjustments based on the actual usage patterns and evolving requirements. Regular testing and monitoring are crucial for maintaining a scalable and reliable system.

Thank you! 
