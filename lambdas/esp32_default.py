import json

#return simple json ping message

def lambda_handler(event, context):
    message = dict()
    message['message'] = "Ping"
    return {
        'statusCode': 200,
        'body' : json.dumps(message).encode('utf-8')
    }