from __future__ import print_function


#lambda authorizer
#return a policy object for client

'''
the policy effect will be 'Allow' only if the querystring parameter 
'authorizerToken' matches the value of req_token variable '''

def lambda_handler(event, context):
    
    req_token = "<insert here access token>"
    token = str(event.get('queryStringParameters', None).get('authorizationToken', None) )
    principalId = 'user'
    tmp = event['methodArn'].split('/')
    resource_arn = tmp[0] + '/*/*'
    
    policy = AuthPolicy(principalId, resource_arn)
    
    if( req_token == token):
        authResponse = policy.build(True)
    else:
        authResponse = policy.build(False)

    return authResponse


class HttpVerb:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    ALL = '*'


#Auth policy class

class AuthPolicy(object):
    version = '2012-10-17'
    
    def __init__(self, principalId, resource_arn):
        self.principalId = principalId
        self.resource_arn = resource_arn
        self.allowMethods = [HttpVerb.ALL]
        self.denyMethods = [HttpVerb.ALL]

    def build(self, flag):
        
        '''Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy.'''

        if ((self.allowMethods is None or len(self.allowMethods) == 0) and
                (self.denyMethods is None or len(self.denyMethods) == 0)):
            raise NameError('No statements defined for the policy')
        
        permission = "Allow" if flag else "Deny"
        
        statement = {
            "Action" : [
                "execute-api:*",
                "sts:*"
            ],
            "Effect" : permission,
            "Resource" : self.resource_arn
        }
        
        policy = {
            'principalId': self.principalId,
            'policyDocument': {
                'Version': self.version,
                'Statement': [statement]
            }
        }

        return policy