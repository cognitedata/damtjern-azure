import numpy as np
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthClientCredentials
import os

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

def pressure_to_waterheight(pressure_value:float):
    return 9.73 - (18.459 - pressure_value) * 0.46;

def pressure_to_waterheight_interpolated(pressure_value: float):
    manual_readings = [5.02, 9.19, 9.42, 9.68, 9.73, 9.95]
    digital_readings = [8.2, 17.274, 17.708, 18.345, 18.459, 18.641]
    default_linear_factor = 0.46
    if pressure_value < digital_readings[0]:
        return manual_readings[0] + (pressure_value-digital_readings[0]) * default_linear_factor
    elif pressure_value > digital_readings[-1]:
        return manual_readings[-1] + (pressure_value-digital_readings[-1]) * default_linear_factor
    return np.interp(pressure_value, digital_readings, manual_readings)