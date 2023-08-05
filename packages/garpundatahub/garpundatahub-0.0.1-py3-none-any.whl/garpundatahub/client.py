from requests import Response

from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account as SA


class DataHubClient(object):
    def __init__(self, credentials: SA.Credentials):
        self.credentials = credentials

    @classmethod
    def from_service_account_file(cls, cred_file_path: str, **kw):
        credentials: SA.Credentials = SA.Credentials.from_service_account_file(cred_file_path, scopes=["garpundatahub"], **kw)
        return cls(credentials)

    def call_metaql(self, query: str, shard_key: int = None) -> Response:
        url = "https://datahub-api.garpun.com/v1/metaql/query"
        session: AuthorizedSession = AuthorizedSession(credentials=self.credentials)
        json_data = {"query": query, "shardKey": shard_key}
        return session.post(url, stream=True, json=json_data)
