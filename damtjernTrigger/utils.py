from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials

def upload_message_to_cdf(message:str):
    client = get_cognite_client()
    
    timestamp = message["key"]
    current = message["value"] 
    waterheight = current_to_waterheight(current)
    return 
    #TODO create datapoints and upload to cdf
   
def current_to_waterheight(current:float):
    return 9-(18-current)*0.45

def get_cognite_client()-> CogniteClient:
    # Contact Project Administrator to get these
    TENANT_ID = "c03b82cf-f2d8-4d02-bf69-e766383bda52"
    CLIENT_ID = "5e71318d-c26b-4535-8ec7-1c6f27a43bda"
    CDF_CLUSTER = "az-power-no-northeurope"  # api, westeurope-1 etc
    COGNITE_PROJECT = "ringerikskraft"

    SCOPES = [f"https://{CDF_CLUSTER}.cognitedata.com/.default"]
    CLIENT_SECRET = os.getenv("MICROSOFT_PROVIDER_AUTHENTICATION_SECRET")  # secret stored in environment variable as application setting
    TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    BASE_URL = f"https://{CDF_CLUSTER}.cognitedata.com"

    creds=OAuthClientCredentials(token_url=TOKEN_URL, client_id= CLIENT_ID, scopes= SCOPES, client_secret= CLIENT_SECRET)
    cnf = ClientConfig(client_name="my-special-client", project=COGNITE_PROJECT, credentials=creds, base_url=BASE_URL)

    return CogniteClient(cnf)