import json
import boto3
from datetime import datetime

#db client
client = boto3.client('dynamodb')

#save client to connected devices table
def lambda_handler(event, context):
    
    connectionId = event["requestContext"]["connectionId"]
    data = client.put_item(
    TableName='devices',
    Item={
        'connectionId' : {
            'S' : str(connectionId)
        },
        'timestamp': {
            'S' : str(datetime.now())
        }
    }
  )
    return {
        'statusCode': 200,
        'body': json.dumps('Connected')
    }
