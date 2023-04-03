"""
app
"""


import os
from funcs import get_secret, refresh_token, set_secret

def handler(event,context):
    """
    main function called by container
    """

    token_data = get_secret(
        os.environ['AWS_SECRET_PATH_GOOGLE_TOKEN'],
        os.environ['AWS_DEFAULT_REGION']
    )

    creds_data = get_secret(
        os.environ['AWS_SECRET_PATH_GOOGLE_CRED'],
        os.environ['AWS_DEFAULT_REGION']
    )

    updated_token_data = refresh_token(
        creds_data,
        token_data
    )

    set_secret(
        os.environ['AWS_SECRET_PATH_GOOGLE_TOKEN'],
        updated_token_data,
        os.environ['AWS_DEFAULT_REGION']
    )

    return {
        'statusCode': 201, #request succeeded and made changes
        'body': 'success'
    }

#for debugging in vscode and calling this file directly
if __name__ == '__main__':
    handler(None,None)
