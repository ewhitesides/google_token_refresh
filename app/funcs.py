"""
funcs
"""

import json
from dataclasses import dataclass,asdict
import boto3
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow


def get_secret(secret_id: str,region_name: str) -> dict:
    """
    Get json string from AWS Secrets Manager and return as dict
    when getting the secret, it is decrypted using the associated KMS key
    """

    session = boto3.session.Session()

    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
        SecretId=secret_id
    )

    output = json.loads(get_secret_value_response['SecretString'])

    return output

def refresh_token(creds_data: dict, token_data: dict) -> str:
    """
    attempt refreshing the token. If it fails, recreate the token.
    """

    #create credentials object from token data
    creds = Credentials(
        token = token_data['token'],
        refresh_token = token_data['refresh_token'],
        token_uri = token_data['token_uri'],
        client_id = token_data['client_id'],
        client_secret = token_data['client_secret']
    )

    @dataclass
    class TokenItem:
        """
        Dataclass for token item
        """
        token: str
        refresh_token: str
        token_uri: str
        client_id: str
        client_secret: str

    try:
        print('refreshing token')
        creds.refresh(Request())
        token_item = TokenItem(
            token = creds.token,
            refresh_token = creds.refresh_token,
            token_uri = creds.token_uri,
            client_id = creds.client_id,
            client_secret = creds.client_secret
        )
    except RefreshError:
        print('recreating token')
        flow = InstalledAppFlow.from_client_config(
            creds_data,
            scopes = [
                'https://www.googleapis.com/auth/calendar.events'
            ]
        )
        flow_output = flow.run_local_server(port=0)
        token_item = TokenItem(
            token = flow_output.token,
            refresh_token = flow_output.refresh_token,
            token_uri = flow_output.token_uri,
            client_id = flow_output.client_id,
            client_secret = flow_output.client_secret
        )

    output = asdict(token_item)
    return output

def set_secret(secret_id:str, data: dict, region_name: str):
    """
    Set secret to AWS Secrets Manager
    """

    session = boto3.session.Session()

    client = session.client(
        service_name = 'secretsmanager',
        region_name = region_name
    )

    #Convert dict to json string
    json_str = json.dumps(data)

    _ = client.put_secret_value(
        SecretId=secret_id,
        SecretString=json_str
    )
