import json
from urllib.parse import urlparse

from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
from neo4j import Auth

from .servicekind import NeptuneServiceKind


class NeptuneAuth(Auth):
    def __init__(
        self,
        credentials: Credentials,
        region: str,
        url: str,
        service: NeptuneServiceKind,
        **parameters,
    ):
        service_name = (
            "neptune-db" if service == NeptuneServiceKind.DB else "neptune-graph"
        )

        request = AWSRequest(method="GET", url=f"{url}/opencypher")

        parsed_url = urlparse(request.url)
        host = str(parsed_url.netloc) if parsed_url.netloc else ""
        request.headers.add_header("Host", host)

        signer = SigV4Auth(credentials, service_name, region)
        signer.add_auth(request)

        required_headers = [
            "Authorization",
            "X-Amz-Date",
            "X-Amz-Security-Token",
            "Host",
        ]

        auth_data = {
            header: request.headers[header]
            for header in required_headers
            if header in request.headers
        }
        auth_data["HttpMethod"] = request.method

        auth_json = json.dumps(auth_data)
        super().__init__("basic", "username", auth_json, "realm", **parameters)
