import json
import boto3
from datetime import datetime, timedelta

#client for communication with websocket connected devices
client = boto3.client('apigatewaymanagementapi', endpoint_url = 'https://tx3bpj2xt4.execute-api.eu-central-1.amazonaws.com/dev')
#db client
db = boto3.client('dynamodb')

#broadcasts message to all websocket connected devices

def broadcast(message):
    devices = db.scan(
            TableName = 'devices',
            AttributesToGet=[
            'connectionId',
            ],
        )
        
    cids = devices['Items']
    for cid in cids:
            connectionId = cid['connectionId']['S']
            client.post_to_connection(ConnectionId = connectionId, Data = json.dumps(message).encode('utf-8'))

'''
if event type is 'data':
    it stores received data in dynamodb and broadcasts them to websocket connected devices
if event type is 'ack':
    it broadcasts to websocket connected devices that esp32 has upgraded its measurement rates
''' 

def lambda_handler(event, context):
        
    if event['type'] == 'data':
        timestamp = int(datetime.now().timestamp())
        expireTime = int( (datetime.now() + timedelta(days=1)).timestamp())
        new_item = {
            'id' : {
                'S' : 'weather'
            },
            
            'timestamp': {
                'N' : str(timestamp)
            },
            
            'ttl' : {
                'N' : str(expireTime)
            },
            
            'temp' : {
                'S' : str(event['weather']['temp'])
            },
            
            'humid' : {
                'S' : str(event['weather']['humid'])
             },
             
            'lum' : {
                'N' : str(event['weather']['lum'])
            },
            
            'rate' : {
                'N' : str(event['info']['rate'])
            }
            
        }
      
        data = db.put_item(
            TableName='esp32_mex',
            Item= new_item
        )
      
        message = new_item
        message['action'] = 'now'
        message['message'] = 'New data received'
        broadcast(message)
    
    if event['type'] == "ack":
        message = dict()
        message['action'] = 'ack'
        message['message'] = 'Measurement rate now at {} mins'.format(event['rate'])
        message['rate'] = event['rate']
        broadcast(message)
        
    return {
        'statusCode': 200
    }