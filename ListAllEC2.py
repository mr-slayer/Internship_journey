import json
from botocore.exceptions import ClientError
import boto3
def lambda_handler(event, context):

    l=""
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        # l.append(instance.id)/
        print(instance.state['Name'])
        l=l+instance.id+" " + instance.state['Name']+"<br>"
        # print (type(instance.id) , type(str(instance.state)))
    print(l)
 
 
 
    #  be verified with Amazon SES.
    SENDER = "aakashsagar640@gmail.com"

    RECIPIENT = "aakashsagar640@gmail.com"

    AWS_REGION = "ap-south-1"

    # The subject line for the email.
    SUBJECT = "Instance report"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = l
            
    # he HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>All Instances:</h1><b>
    """+BODY_TEXT+"""
    </b>
    </p>
    </body>
    </html>
            """          

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)

    # Try to send the email.
    try:
    #Provide the contents of the email.
        response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML,
                },
                'Text': {
                    'Charset': CHARSET,
                    'Data': BODY_TEXT,
                },
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,

        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
