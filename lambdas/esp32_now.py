import json
from datetime import datetime, timedelta
import boto3

#db client
db = boto3.client('dynamodb')

#sends the last measurements to client
def lambda_handler(event, context):
    
    yesterday = int((datetime.now() - timedelta(days=1)).timestamp())
    
    data = db.query(
        TableName = 'esp32_mex',
        KeyConditionExpression= "#id = :section AND #ts >= :yesterday",
        ExpressionAttributeValues = {
            ':yesterday' : {
                'N' : str(yesterday)
            },
            ':section' : {
                'S' : 'weather'
            }
        },
        ExpressionAttributeNames={
            "#ts": "timestamp",
            "#id": "id",
            "#t" : "temp",
            "#h" : "humid",
            "#l" : "lum",
            "#r" : "rate"
        },
        Limit = 1,
        ScanIndexForward =  False,
        ProjectionExpression = '#ts, #t, #h, #l, #r'
    )
    
    if len(data['Items']) > 0:
        message = data['Items'][0]
    else:
        message = dict()
        message['message'] = "Error: no record found"
    
    message['action'] = 'now'
    
    return {
        'statusCode': 200,
        'body' : json.dumps(message).encode('utf-8')
    }