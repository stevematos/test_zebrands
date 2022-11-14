from botocore.client import BaseClient
from botocore.exceptions import ClientError

from boto3 import client
import logging
from json import dumps
from config.aws import get_client
from config.environment import config_env


import logging


logger = logging.getLogger('debug')

CHARSET = "UTF-8"


def send_plain_email(
    email: str, subject: str, body: str, ses_client: BaseClient | None = None
) -> bool:
    sender = "Admin <steve.matos.1998@gmail.com>"
    if not ses_client:
        ses_client = get_client(service="ses", endpoint_url=config_env().AWS_SES_ENDPOINT_URL)

    try:
        ses_client.send_email(
            Destination={
                "ToAddresses": [
                    email,
                ],
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": body,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": subject,
                },
            },
            Source=sender,
        )
    except ClientError as error:
        logger.error(f"Error sending plain e-mail. [error={error}]")
        return False
    return True