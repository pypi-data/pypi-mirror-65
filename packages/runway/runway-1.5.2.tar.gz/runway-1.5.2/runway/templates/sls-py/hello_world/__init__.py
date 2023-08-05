"""Serverless Hello World function."""
import json


def handler(event, context):  # pylint: disable=unused-argument
    """Return Serverless Hello World."""
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    # return {
    #     "message": "Go Serverless v1.0! Your function executed!",
    #     "event": event
    # }
