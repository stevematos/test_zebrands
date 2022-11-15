import logging

from boto3 import client
from botocore.client import BaseClient
from config.environment import (
    AWS_ACCESS_KEY,
    AWS_REGION,
    AWS_SECRET_ACCESS_KEY,
)


def get_client(
    service: str,
    endpoint_url: str | None = None,
    region: str | None = AWS_REGION,
    aws_access_key_id: str | None = AWS_ACCESS_KEY,
    aws_secret_access_key: str | None = AWS_SECRET_ACCESS_KEY,
) -> BaseClient:
    if endpoint_url:
        logging.debug(
            f"Using specific endpoint url for AWS service. "
            f"[service={service}, endpoint_url={endpoint_url}]"
        )
        return client(
            service,
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    if region:
        logging.debug(
            f"Using specific region for AWS service. "
            f"[service={service}, region={region}]"
        )
        return client(
            service,
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    logging.debug(
        f"Using default endpoint url for AWS service. " f"[service={service}]"
    )
    return client(
        service,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )
