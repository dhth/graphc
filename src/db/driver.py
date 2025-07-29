from neo4j import GraphDatabase, Driver
import os
from boto3 import Session
from domain import NeptuneAuth, NeptuneServiceKind


def get_db_driver(db_uri: str) -> Driver:
    if "neptune.amazonaws.com" in db_uri:
        session = Session()
        region = os.environ.get("AWS_REGION", "us-east-1")
        auth_token = NeptuneAuth(
            credentials=session.get_credentials(),
            region=region,
            url=db_uri,
            service=NeptuneServiceKind.DB,
        )

        return GraphDatabase.driver(db_uri, auth=auth_token, encrypted=True)
    else:
        user_name = os.environ.get("DB_USER", "neo4j")
        password = os.environ.get("DB_PASSWORD", "password")
        return GraphDatabase.driver(db_uri, auth=(user_name, password))
