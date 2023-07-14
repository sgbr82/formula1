# try:
#     import unzip_requirements
# except ImportError:
#     pass

import os
import boto3
import pandas as pd
import requests

def uploadToS3(s3_bucket,key, data):
    """
    The function `uploadToS3` uploads data to an S3 bucket using the specified key.
    
    :param s3_bucket: The `s3_bucket` parameter is the name of the S3 bucket where you want to upload
    the data
    :param key: The "key" parameter in the "uploadToS3" function is the name or path of the object you
    want to upload to the S3 bucket. It is used as the unique identifier for the object within the
    bucket
    :param data: The `data` parameter in the `uploadToS3` function represents the content or data that
    you want to upload to an S3 bucket. It can be any type of data, such as a string, a file, or binary
    data
    :return: a dictionary with two key-value pairs. The 'statusCode' key has a value of 200, indicating
    a successful operation, and the 'body' key has a value of 'Data uploaded to S3 successfully', which
    is a message indicating the success of the upload.
    """
    s3 = boto3.client('s3')
    s3.put_object(
        Bucket=s3_bucket,
        Key=key,
        Body=data
    )
    return {
        'statusCode': 200,
        'body': 'Data uploaded to S3 successfully'
    }

def seasons(event, context):
    """
    The `seasons` function retrieves a list of seasons from an API, converts it to a DataFrame, uploads
    it to an S3 bucket, and returns the DataFrame as a JSON response.
    
    :param event: The `event` parameter is typically used to pass data to the Lambda function. It can
    contain information about the triggering event, such as the request payload or any other relevant
    data
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not being used
    :return: The code is returning a JSON response with a status code of 200 and a body containing the
    seasons data in JSON format.
    """
    response = requests.request("GET", os.environ['API_SEASONS'], headers={}, data={})
    seasons_list = pd.read_json(response.text).MRData.SeasonTable.get("Seasons")
    seasons_df = pd.DataFrame(seasons_list, columns=["season","url"])
    uploadToS3(os.environ['S3_BUCKET_NAME'],'/inbound/seasons.json',seasons_df.to_json(orient='records',lines=True))
    return {
        "statusCode": 200, 
        "body": seasons_df.to_json(orient='records',lines=True)
        }

def circuits(event, context):
    """
    The `circuits` function retrieves circuit data from an API, converts it to a DataFrame, uploads it
    to an S3 bucket, and returns the data as a JSON response.
    
    :param event: The `event` parameter is the input data passed to the function. It can contain
    information about the triggering event, such as the request details or any additional data needed
    for the function to execute
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information
    :return: a JSON response with a status code of 200 and a body containing the circuits data in JSON
    format.
    """
    response = requests.request("GET", os.environ['API_CIRCUITS'], headers={}, data={})
    circuits_list= pd.read_json(response.text).MRData.CircuitTable.get("Circuits")
    circuits_df = pd.DataFrame(circuits_list, columns=["circuitId","url","circuitName","Location"])
    uploadToS3(os.environ['S3_BUCKET_NAME'],'/inbound/circuits.json',circuits_df.to_json(orient='records',lines=True))
    return {
        "statusCode": 200, 
        "body": circuits_df.to_json(orient='records',lines=True)
        }
    
def drivers(event, context):
    """
    The `drivers` function retrieves a list of drivers from an API, converts it into a DataFrame,
    uploads it to an S3 bucket, and returns the DataFrame as a JSON response.
    
    :param event: The `event` parameter is typically used to pass data to the function. It can contain
    information about the triggering event, such as the request details or any data associated with the
    event
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not used
    :return: a dictionary with two key-value pairs. The "statusCode" key has a value of 200, indicating
    a successful response, and the "body" key has a value of the drivers_df DataFrame converted to JSON
    format using the 'records' orientation and 'lines' format.
    """
    response = requests.request("GET", os.environ['API_DRIVERS'], headers={}, data={})
    drivers_list= pd.read_json(response.text).MRData.DriverTable.get("Drivers")
    drivers_df = pd.DataFrame(drivers_list, columns=["driverId","url","givenName","familyName","dateOfBirth","nationality"])
    uploadToS3(os.environ['S3_BUCKET_NAME'],'/inbound/drivers.json',drivers_df.to_json(orient='records',lines=True))
    return {
        "statusCode": 200, 
        "body": drivers_df.to_json(orient='records',lines=True)
        }
    
def constructors(event, context):
    """
    The `constructors` function retrieves a list of constructors from an API, converts it into a
    DataFrame, uploads it to an S3 bucket, and returns the DataFrame as a JSON response.
    
    :param event: The `event` parameter is typically used to pass data to the function. It can contain
    information about the triggering event, such as the request details or any input data
    :param context: The `context` parameter is an object that provides information about the runtime
    environment of the function. It includes details such as the AWS request ID, function name, and
    other contextual information. In this code snippet, the `context` parameter is not being used
    :return: a dictionary with two key-value pairs. The "statusCode" key has a value of 200, indicating
    a successful response, and the "body" key has a value of the constructors_df DataFrame converted to
    JSON format using the 'records' orientation and 'lines' format.
    """
    response = requests.request("GET", os.environ['API_CONSTRUCTORS'], headers={}, data={})
    constructors_list= pd.read_json(response.text).MRData.ConstructorTable.get("Constructors")
    constructors_df = pd.DataFrame(constructors_list, columns=["constructorId","url","name","nationality"])
    uploadToS3(
                os.environ['S3_BUCKET_NAME'],
               '/inbound/constructors.json',
               constructors_df.to_json(orient='records',lines=True)
               )
    return {
        "statusCode": 200, 
        "body": constructors_df.to_json(orient='records',lines=True)
        }
    
    