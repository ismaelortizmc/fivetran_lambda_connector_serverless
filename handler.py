from datetime import datetime
import logging
import requests
import uuid



def lambda_handler(request, context):
    """
        Lambda handler GET a list of Pokemon info from free Pokemon API
        and return data in JSON format.

        Note: This is a educational example.

        args: request, context  - request and context from Fivetran Connector

        return: JSON data - One Pokemon by call

        Pokemon API: https://pokeapi.co/docs/v2.html
    """

    # Read event data - get secret and state object from event
    secrets = request['secrets']
    state = request['state']
    data = []
    table_name = ""
    state_updated = {}

    # API call - get data from API try catch block
    try:
        # Authenticate API call - use secret to authenticate API call - always used this name
        consumer_key = secrets["consumerKey"]
        consumer_secret = secrets["consumerSecret"]
        api_key = secrets["apiKey"]

        api_client = get_client(consumer_key, consumer_secret, api_key)

        # Process data - process data from API call and use state object to process data
        # Extract API data
        raw = get_data_from_api(api_client, state)
        raw_data = raw['raw_data']
        state_updated = raw['state_updated']

        # Transform API data
        transformed = transform_data(raw_data)
        data = transformed["pokedex"]
        table_name = transformed["table_name"]

    except Exception as e:
        # Error handling - if error, return error message for Fivetran
        return {'state': state, 'errorMessage': f"Error API process: {str(e)}", 'hasMore': False}

    # Load API data - return data to Fivetran
    return {
        "state": state_updated,
        "insert":  {f"{table_name}": data},
        'schema':  {'primary_key': ['id', 'date']},
        'hasMore': False
    }


################# get client ###################################


def get_client(consumer_key: str, consumer_secret: str, api_key: str) -> str:
    """
        Get client API
        args: consumer_key, consumer_secret, api_key
        return: client
    """

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    logger.info('Confirming Fivetran Secrerts are valid - only educational: ')
    logger.info(f'Consumer Key: {consumer_key}')
    logger.info(f'Consumer Secret: {consumer_secret}')
    logger.info(f'API Key: {api_key}')

    # Create client - we don't need to authenticate for this example
    return "https://pokeapi.co/api/v2/pokedex/"


############################# get data form api #############################################


def get_data_from_api(api_client: str, state: dict) -> dict:
    """
        Get data API
        args: api_client, state
        return: raw_data, state_updated
    """
    # Pokedex - last region
    POKEDEX_LAST_REGION = 29

    # Porcess Fivetran state
    count = 0 if not 'count' in state else int(state["count"])
    count = 0 if count > POKEDEX_LAST_REGION else count

    # Get data from API
    res = requests.get(f"{api_client}{count}")
    raw_data = dict(res.json())

    return {"raw_data": raw_data, "state_updated": {"count": count + 1}}


############################# transform_data #############################################


def transform_data(raw_data: dict) -> dict:
    """
        Transform data API
        args: raw_data - data from API call
        return: data - list of pokemons and table name
    """

    # Extract data from API call
    pokemon_entries = list(raw_data["pokemon_entries"])
    pokedex = list(
        map(
            lambda x: {
                "id": str(uuid.uuid4()) ,
                "region_id": raw_data["id"],
                "name": raw_data["name"],
                "pokemon_entry_number": x["entry_number"],
                "pokemon_species": x["pokemon_species"]["name"],
                "pokemon_url": x["pokemon_species"]["url"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            pokemon_entries
        )
    )

    data = {"pokedex": pokedex, "table_name": raw_data["name"]}

    return data
