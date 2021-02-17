import json
import boto3
from datetime import datetime, timedelta


def lambda_handler(event, context):
    client = boto3.client('cloudwatch')
    l=[]
    result=[]
    ec2 = boto3.resource('ec2')
    send_string=" "
    for instance in ec2.instances.all():
        if(instance.state['Name']=='running'):
            #print (instance.id)
            l.append(instance.id)
    # print(l)
    for ins in l:
        
        response = client.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName='CPUUtilization',
            Dimensions=[
                {
                'Name': 'InstanceId',
                'Value': ins
                },

            ],
            StartTime=datetime.now() - timedelta(hours=48, minutes=50),
            EndTime=datetime.now(),
            Period=86400,
            Statistics=[
                'Average',
            ],
            Unit='Percent'
        )
        if(response['Datapoints'][0]['Average']>80):

            result.append(ins)
            send_string=send_string+ins+" : "+str(response['Datapoints'][0]['Average'])+"<br>"

    # ec2.instances.filter(InstanceIds = result).stop()                   //uncomment for stop the instance
     

    
    SENDER = "aakashsagar640@gmail.com"
    RECIPIENT = "aakashsagar640@gmail.com"
    AWS_REGION = "ap-south-1"
    CHARSET = "UTF-8"
    SUBJECT = "Instance report"
    BODY_TEXT=send_string
    BODY_HTML = """<html>
    <head></head>
    <body>
    <h1>CPU High Utilization</h1>
    <p><b>IDs and Its Utilization:<br>"""+BODY_TEXT+"""
    </b>
    </p>
    </body>
    </html>
            """   
    ses_client = boto3.client('ses',region_name=AWS_REGION)
    
    
    return ses_client.send_email(
        Destination={
            'ToAddresses': [
                'aakashsagar640@gmail.com',
            ],
        },
        Message={
            'Body': {
                'Html': {
                    'Charset': CHARSET,
                    'Data': BODY_HTML
                },
               
            },
            'Subject': {
                'Charset': CHARSET,
                'Data': SUBJECT,
            },
        },
        Source=SENDER,

        )

  
