import json
import boto3

#mqtt broker client
mqtt = boto3.client('iot-data', region_name='eu-central-1')

#post a message containing new measurement rate to mqtt esp32/sub topic
#it will be listened by esp32

def lambda_handler(event, context):
    
    body = json.loads(event["body"])
    
    message = dict()
    message['action'] = 'rate'
    
    if 'rate' in body:
        rate = int(body["rate"])
        message['rate'] = rate
        
        if 5 <= rate <= 120:
        
            response = mqtt.publish(
                    topic='esp32/sub',
                    qos=1,
                    payload=json.dumps({"rate": rate})
            )
            
            print(response)
            message['message'] = "Waiting for ESP32 acknowledgement ..."
        
        else:
            message['message'] = "Error: params invalid"
    
    else:
        message['message'] = "Error: required params missing"
    
    return {
        'statusCode': 200,
        'body': json.dumps(message).encode('utf-8')
    }