import os

from boto3 import Session
from neo4j import Driver, GraphDatabase

from domain import NeptuneAuth, NeptuneServiceKind


def get_db_driver(db_uri: str) -> Driver:
    if "neptune.amazonaws.com" in db_uri:
        session = Session()
        region = os.environ.get("AWS_REGION", "us-east-1")
        auth = NeptuneAuth(
            credentials=session.get_credentials(),
            region=region,
            uri=db_uri,
            service=NeptuneServiceKind.DB,
        )

        return GraphDatabase.driver(db_uri, auth=auth, encrypted=True)
    else:
        user_name = os.environ.get("DB_USER", "neo4j")
        password = os.environ.get("DB_PASSWORD", "password")
        return GraphDatabase.driver(db_uri, auth=(user_name, password))
