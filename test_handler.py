from handler import lambda_handler


def test_lambda_handler(tabla_name):
    """
        Test lambda_handler function
    """
    # Create event data
    event = {
        'secrets': {    
            'consumerKey': 'test_consumerKey',
            'consumerSecret': 'test_consumerSecret',
            'apiKey': 'test_apiKey' 
        },
        'state': {
            'count': '29',
        }
    }
    # Create context data
    context = {
        'aws_request_id': '',
        'function_name': '',
        'log_group_name': '',
        'log_stream_name': '',
        'memory_limit_in_mb': '',
        'function_version': '',
        'invokeid': '',
        'invoked_function_arn': ''
    }


    # Call lambda_handler function
    response = lambda_handler(event, context)

    # Check response
    assert response['state']['count'] == 30
    assert response['hasMore'] == False
    assert tabla_name in response['insert']  
    return True


print(test_lambda_handler('crown-tundra'))