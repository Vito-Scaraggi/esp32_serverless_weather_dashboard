import json
import boto3

#db client
client = boto3.client('dynamodb')

#remove client from connected devices table
def lambda_handler(event, context):
    connectionId = event["requestContext"]["connectionId"]
    data = client.delete_item(
        TableName='devices',
        Key={
            'connectionId': {
                'S' : str(connectionId)
            }
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Disconnected')
    }