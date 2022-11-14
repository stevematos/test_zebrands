from botocore.client import BaseClient
# from botocore.exceptions import ClientError
from boto3 import client
import logging


def get_client(
    service: str,
    endpoint_url: str | None = None,
    region: str | None = None,
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
) -> BaseClient:
    if endpoint_url:
        logging.debug(
            f"Using specific endpoint url for AWS service. [service={service}, endpoint_url={endpoint_url}]"
        )
        return client(
            service,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    if region:
        logging.debug(
            f"Using specific region for AWS service. [service={service}, region={region}]"
        )
        return client(
            service,
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    logging.debug(f"Using default endpoint url for AWS service. [service={service}]")
    return client(
        service,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )


