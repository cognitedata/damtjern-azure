import logging
import os
import azure.functions as func

from .utils import upload_message_to_cdf

external_id_current = "current"
external_id_waterheight = "waterheight"

def main(event: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                 event.get_body().decode('utf-8'))
    print(os.environ)
    message = event.get_body().decode('utf-8')
    upload_message_to_cdf(message)
    