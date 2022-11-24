import boto3
import os


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
    error = e

CHARSET = "UTF-8"


def handler(event, context): 
    if error is None and "queryStringParameters" in event:

        params = event["queryStringParameters"]
        if "sender" in params and "email" in params and "message" in params:
            sender = params["sender"]
            email = params["email"]
            content = f"{sender} sent the following message:\n'
            message = {
                "Subject": {
                    "Data": f"{sender} sent a message from {HOST_URL}",
                    "Charset": CHARSET
                },
                "Body": {
                    "Text": {
                        "Data": content + params["message"],
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
                print(f"parameters: {params}\n{e}")
                return {
                    "status": 301,
                    "headers": {
                        "Location": f"{HOST_URL}/{ERROR_PAGE}"
                    }
                    }                 
            return {
                "status": 301,
                "headers": {
                    "Location": f"{HOST_URL}/{REDIRECT_PAGE}"
                }
                }   

    return {
        "status": 301,
        "headers": {
            "Location": f"{HOST_URL}/{ERROR_PAGE}"
        }
        }                
