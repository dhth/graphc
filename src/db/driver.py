import os

from boto3 import Session
from botocore.exceptions import BotoCoreError
from neo4j import Driver, GraphDatabase

from domain import NeptuneAuth, NeptuneServiceKind
from errors import AWSAuthError


def get_db_driver(db_uri: str) -> Driver:
    if "neptune.amazonaws.com" in db_uri:
        region = os.environ.get("AWS_REGION", "").strip()

        if region == "":
            raise RuntimeError("AWS_REGION needs to be set")

        session = Session()
        try:
            session.get_credentials().token
        except BotoCoreError as e:
            raise AWSAuthError(f"couldn't authenticate AWS client: {e}")

        # TODO: add support for neptune graph
        auth = NeptuneAuth(
            credentials=session.get_credentials(),
            region=region,
            uri=db_uri,
            service=NeptuneServiceKind.DB,
        )

        return GraphDatabase.driver(
            db_uri,
            auth=auth,
            encrypted=True,
            connection_timeout=5,
            connection_acquisition_timeout=5,
        )
    else:
        user_name = os.environ.get("DB_USER")
        password = os.environ.get("DB_PASSWORD")

        if user_name is None and password is None:
            raise RuntimeError("DB_USER and DB_PASSWORD need be set")
        elif user_name is None:
            raise RuntimeError("DB_USER needs be set")
        elif password is None:
            raise RuntimeError("DB_PASSWORD needs be set")

        return GraphDatabase.driver(db_uri, auth=(user_name, password))
