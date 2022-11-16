import logging

from botocore.client import BaseClient
from botocore.exceptions import ClientError
from config.aws import get_client
from config.environment import AWS_SES_ENDPOINT_URL

logger = logging.getLogger("debug")

CHARSET = "UTF-8"


def send_plain_email(
    emails: list[str],
    subject: str,
    body: str,
    ses_client: BaseClient | None = None,
) -> bool:
    sender = "Admin <steve.matos.1998@gmail.com>"
    if not ses_client:
        ses_client = get_client(
            service="ses", endpoint_url=AWS_SES_ENDPOINT_URL
        )

    for email in emails:
        try:
            ses_client.send_email(
                Destination={
                    "ToAddresses": [email],
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
    return True
