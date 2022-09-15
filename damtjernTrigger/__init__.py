from datetime import datetime
import logging
import pytz
import azure.functions as func

from .utils import get_cognite_client, pressure_to_waterheight_interpolated

external_id_pressure_damtjern = "02.314.001:trykk_damtjern"
external_id_waterheight_damtjern = "02.314.001:vannstand_damtjern"

def main(event: func.EventHubEvent):
    
    logging.info('Message recieved')
    timestamp = datetime.now(pytz.timezone("Europe/Oslo"))
    message = eval(event[0].get_body().decode('utf-8'))
    pressure_value = message["level"]
    
    if pressure_value < 3.9:
        logging.info(f"Low level {pressure_value} ")
    elif pressure_value == 0:
        logging.info("Pressure value is zero, no update")
        return
    water_height = pressure_to_waterheight_interpolated(pressure_value)
    
    c = get_cognite_client()
    c.datapoints.insert([(timestamp, pressure_value)], external_id = external_id_pressure_damtjern)
    c.datapoints.insert([(timestamp, water_height)], external_id = external_id_waterheight_damtjern)
    logging.info('Python EventHub trigger processed an event: %s', message)
    