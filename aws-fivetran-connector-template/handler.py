import json
from datetime import datetime


def lambda_handler(request, context):

    # Read event data - get secret and state object from event
    secrets = request['secrets']
    state = request['state']
    data = []
    table_name = "table_name"

    # API call - get data from API try catch block
    try:
        # Authenticate API call - use secret to authenticate API call
        consumer_key = secrets["consumerKey"]
        consumer_secret = secrets["consumerSecret"]
        api_key = secrets["apiKey"]

        api_client = get_client(consumer_key, consumer_secret, api_key)

        # Process data - process data from API call and use state object to process data
        # Always confirm the state object is not empty
        count = 0 if not 'count' in request["state"] else int(
            request["state"]["count"])

        # Extract API data
        raw_data = get_data_from_api(api_client)

        # Transform API data
        data = transform_data(raw_data)

    except Exception as e:
        # Error handling - if error, return error message for Fivetran
        return {'state': {'count': count}, 'errorMessage': f"Error {str(e)}"}

    # Load API data - return data to Fivetran
    return {
        "state": {"count": count + 1},
        "insert":  {f"{table_name}": data},
        'schema':  {'primary_key': ['id', 'date']},
        'hasMore': False
    }


def get_client(consumer_key, consumer_secret, api_key):
    """
    Get client API
    """
    pass

def get_data_from_api(api_client):
    """
    Get data API
    """
    pass

def transform_data(raw_data):
    """
    Transform data API
    """
    pass

