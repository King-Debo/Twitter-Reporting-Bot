# Import the boto3 library
import boto3

# Define the AWS credentials
aws_access_key_id = "YOUR_AWS_ACCESS_KEY_ID"
aws_secret_access_key = "YOUR_AWS_SECRET_ACCESS_KEY"
aws_region_name = "YOUR_AWS_REGION_NAME"

# Create a boto3 client for SageMaker
sagemaker_client = boto3.client("sagemaker", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)

# Create a SageMaker model
model_name = "web_bot_model" # The name of the model
model_data_url = "s3://YOUR_BUCKET_NAME/model.h5" # The S3 URL of the model file
model_role = "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_ROLE_NAME" # The IAM role ARN for the model
model_container = {"Image": "763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-inference:2.4.1-cpu", # The container image for TensorFlow inference
                   "ModelDataUrl": model_data_url} # The model data URL
sagemaker_client.create_model(ModelName=model_name, PrimaryContainer=model_container, ExecutionRoleArn=model_role) # Create the model using the boto3 client

# Create a SageMaker endpoint configuration
endpoint_config_name = "web_bot_endpoint_config" # The name of the endpoint configuration
endpoint_config_production_variants = [{"VariantName": "AllTraffic", # The name of the production variant
                                        "ModelName": model_name, # The name of the model
                                        "InitialInstanceCount": 1, # The initial instance count
                                        "InstanceType": "ml.t2.medium"}] # The instance type
sagemaker_client.create_endpoint_config(EndpointConfigName=endpoint_config_name, ProductionVariants=endpoint_config_production_variants) # Create the endpoint configuration using the boto3 client

# Create a SageMaker endpoint
endpoint_name = "web_bot_endpoint" # The name of the endpoint
sagemaker_client.create_endpoint(EndpointName=endpoint_name, EndpointConfigName=endpoint_config_name) # Create the endpoint using the boto3 client

# Wait for the endpoint to be in service
sagemaker_client.get_waiter("endpoint_in_service").wait(EndpointName=endpoint_name) # Wait for the endpoint to be in service using the boto3 client

# Create a boto3 client for Lambda
lambda_client = boto3.client("lambda", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)

# Create a Lambda function
function_name = "web_bot_function" # The name of the function
function_role = "arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_ROLE_NAME" # The IAM role ARN for the function
function_code = {"ZipFile": open("lambda_function.zip", "rb").read()} # The zip file containing the function code and dependencies
function_handler = "lambda_function.lambda_handler" # The function handler
function_runtime = "python3.8" # The function runtime
function_timeout = 15 # The function timeout in seconds
function_memory_size = 128 # The function memory size in MB
lambda_client.create_function(FunctionName=function_name, Role=function_role, Code=function_code, Handler=function_handler, Runtime=function_runtime, Timeout=function_timeout, MemorySize=function_memory_size) # Create the function using the boto3 client

# Add permission to the Lambda function to invoke the SageMaker endpoint
lambda_client.add_permission(FunctionName=function_name, StatementId="sagemaker_invoke", Action="sagemaker:InvokeEndpoint", Principal="lambda.amazonaws.com", SourceArn=f"arn:aws:lambda:{aws_region_name}:{aws_account_id}:function:{function_name}") # Add permission using the boto3 client

# Create a boto3 client for SNS
sns_client = boto3.client("sns", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)

# Create a SNS topic
topic_name = "web_bot_topic" # The name of the topic
topic_response = sns_client.create_topic(Name=topic_name) # Create the topic using the boto3 client and get the response
topic_arn = topic_response["TopicArn"] # Extract the topic ARN from the response

# Subscribe to the SNS topic
subscription_protocol = "email" # The subscription protocol
subscription_endpoint = "YOUR_EMAIL_ADDRESS" # The subscription endpoint
sns_client.subscribe(TopicArn=topic_arn, Protocol=subscription_protocol, Endpoint=subscription_endpoint) # Subscribe to the topic using the boto3 client

# Test the Lambda function
test_event = {"text": "The COVID-19 vaccine causes infertility"} # The test event
test_response = lambda_client.invoke(FunctionName=function_name, Payload=json.dumps(test_event)) # Invoke the function using the boto3 client and get the response
test_result = json.load(test_response["Payload"]) # Extract the result from the response
print(test_result) # Print the result
