import json
import boto3
import sys
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
def email(msg):
     
    #  be verified with Amazon SES.
    SENDER = "aakashsagar640@gmail.com"

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "aakashsagar640@gmail.com"

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "ap-south-1"

    # The subject line for the email.
    SUBJECT = "Instance report"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = msg
            
    # he HTML body of the email.
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>Amazon SES Test (SDK for Python)</h1>
    <p>This email was sent with"""+BODY_TEXT+"""
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
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
            )
        # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
def lambda_handler(event, context):
    # TODO implement
    low={}
    high={}
    client = boto3.client('cloudwatch')
    l=[]
    ec2 = boto3.resource('ec2')
    for instance in ec2.instances.all():
        if(instance.state['Name']=='running'):
            #print (instance.id)
            l.append(instance.id)
    # msg=""
   #print(l)
    for ins in l:
        
        response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': ins
                },
                # {
                # 'Name': 'InstanceId',
                # 'Value': 'i-078837de4b48dde7b'
                # },
            ],
            StartTime=datetime.now() - timedelta(hours=23, minutes=50),
            EndTime=datetime.now(),
            Period=86400,
            Statistics=[
                'Average',
            ],
            Unit='Percent'
        )
        for cpu in response['Datapoints']:
            if 'Average' in cpu:
                if(cpu['Average']<20):
                    # msg=msg+ins+" "+ str(cpu['Average'])+"<br>"
                    low[ins]=cpu['Average']
                    
                elif(cpu['Average']>80):
                    high[ins]=cpu['Average']
            
                else:
                    pass
               
                
    print(low)
    print(high)
    # email("this is awsdome")
    
