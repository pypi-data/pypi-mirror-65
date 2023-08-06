from spell.api import base_client
from spell.api.utils import url_path_join

MODEL_URL = "model"


class ModelClient(base_client.BaseClient):
    def new_model(self, owner, name, resource, version):
        payload = {
            "name": name,
            "version": version,
            "resource": resource,
        }
        r = self.request("post", url_path_join(MODEL_URL, owner), payload=payload)
        self.check_and_raise(r)
