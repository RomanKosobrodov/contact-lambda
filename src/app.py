import boto3
import os
import base64
from urllib.parse import urlparse, parse_qs

error = None

try:
    ses = boto3.client("ses")
    HOST_URL = os.environ["HostURL"]
    REDIRECT_PAGE = os.environ["RedirectPage"]
    ERROR_PAGE = os.environ["ErrorPage"]
    SENDER_EMAIL = os.environ["SenderEmail"]
    RECIPIENT_EMAIL = os.environ["RecipientEmail"]
    CC_EMAIL = os.environ["CCEmail"]
    BCC_EMAIL = os.environ["BCCEmail"]

    destination = {"ToAddresses": RECIPIENT_EMAIL.split(",")}
    if len(CC_EMAIL) > 0:
        destination["CcAddresses"] = CC_EMAIL.split(",")
    if len(BCC_EMAIL) > 0:
        destination["BccAddresses"] = BCC_EMAIL.split(",") 
except Exception as e:
    print(f"Error initialising Lambda Function\n{e}")
    error = e

CHARSET = "UTF-8"


def handler(event, context):
    if error is not None:
        return {
            "statusCode": 301,
            "headers": {
                "Location": f"{HOST_URL}/{ERROR_PAGE}"
            },
        }

    if "body" in event and len(event["body"]) > 0:
        decoded = base64.b64decode(event["body"]).decode(CHARSET)
        parsed = urlparse("?" + decoded)
        params = parse_qs(parsed.query)
        if "sender" in params and "email" in params and "message" in params:
            sender = params["sender"][0]
            email = params["email"][0]
            text = params["message"][0]
            content = f"{sender} sent the following message:\n" + text
            message = {
                "Subject": {
                    "Data": f"{sender} sent a message from {HOST_URL}",
                    "Charset": CHARSET
                },
                "Body": {
                    "Text": {
                        "Data": content,
                        "Charset": CHARSET
                    }
                }
            }

            try:
                response = ses.send_email(Source=SENDER_EMAIL,
                                        Destination=destination,
                                        Message=message,
                                        ReplyToAddresses=[f'"{sender}"<{email}>'],
                                        ReturnPath=SENDER_EMAIL)
            except Exception as e:
                print(f"SES Exception\nparameters: {params}\n{e}")
                return {
                    "statusCode": 301,
                    "headers": {
                        "Location": f"{HOST_URL}/{ERROR_PAGE}"    
                    }
                }                 

            return {
                "statusCode": 301,
                "headers": {
                    "Location": f"{HOST_URL}/{REDIRECT_PAGE}"    
                }
            } 

    print(f"wrong event format:\n{event}")
    return {
        "statusCode": 301,
        "headers": {
            "Location": f"{HOST_URL}/{ERROR_PAGE}"    
        }
    }                

