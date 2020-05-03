import os
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import ClientError


def send_email_with_json(event, context):
    execute(event)


def execute(event):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    print(f'Bucket name is: {bucket_name}')

    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    key = event['Records'][0]['s3']['object']['key']
    print(f'Key is: {key}')
    obj = s3.Object(bucket_name, key)
    file_content = obj.get()['Body'].read().decode('utf-8')

    filepath = f"/tmp/{key.replace('/', '')}"
    s3_client.download_file(bucket_name, key, filepath)

    SENDER = 'Laura Fernandez <laufergall@gmail.com>'
    RECIPIENT = 'laufergall@gmail.com'
    AWS_REGION = 'eu-central-1'

    SUBJECT = 'AWS generated JSON'
    ATTACHMENT = filepath
    BODY_TEXT = f'Hallo,\r\n\nHier ist die JSON Datei: {key}.'
    CHARSET = 'utf-8'

    # SES resource
    client = boto3.client('ses', region_name=AWS_REGION)
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    msg_body.attach(textpart)

    att = MIMEApplication(open(ATTACHMENT, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=key)
    msg.attach(msg_body)
    msg.attach(att)

    try:
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data': msg.as_string(),
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print(f"Email sent! Message ID: {response['MessageId']}")
