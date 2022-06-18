import json
from datetime import datetime, timedelta
import boto3

#db client
db = boto3.client('dynamodb')

#send the requested history data to client
def lambda_handler(event, context):
    
    body = json.loads(event["body"])
    
    message = dict()
    message['action'] = 'history'
    
    if 'graph' in body and 'hours' in body:
        
        graph = str(body["graph"])
        try:
            hours = int(body["hours"])
        except:
            hours = 0
        
        message['graph'] = graph
        message['hours'] = hours
        
        if graph in ['temp', 'humid', 'lum', 'rate'] and 1 <= hours <= 24 :
            
            low_time = int((datetime.now() - timedelta(hours=hours)).timestamp())
            data = db.query(
                TableName = 'esp32_mex',
                KeyConditionExpression= "#id = :section AND #ts >= :low_time",
                ExpressionAttributeValues = {
                    ':low_time' : {
                        'N' : str(low_time)
                    },
                    ':section' : {
                        'S' : 'weather'
                    }
                },
                ExpressionAttributeNames={
                    "#id": "id",
                    "#ts": "timestamp",
                    "#attr": graph
                },
                ScanIndexForward =  True,
                ProjectionExpression = '#ts, #attr'
            )
            
            message['data'] = data['Items']
        else:
            message['message'] = "Error:  graphic params invalid"
    else:
        message['message'] = "Error: required params missing"
        
    return {
        'statusCode': 200,
        'body' : json.dumps(message).encode('utf-8')
    }
