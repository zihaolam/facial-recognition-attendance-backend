import os

STAGE = os.environ.get('STAGE')
REGION = os.environ.get("REGION")
CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")
USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")

is_prod = STAGE == "prod"
