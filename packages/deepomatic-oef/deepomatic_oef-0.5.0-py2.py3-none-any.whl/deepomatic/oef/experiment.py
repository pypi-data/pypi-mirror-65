import os
import requests
from google.protobuf.json_format import MessageToDict

from deepomatic.oef.utils import serializer
from deepomatic.oef.protos import experiment_pb2

class Experiment(serializer.Serializer):
    """An experiment object

    Keyword arguments:
    dataset -- the dataset used to train or evaluate
    """

    def launch(self, dataset_slug, model_name, url_prefix=None, api_key=None):
        if url_prefix is None:
            url_prefix = os.getenv('DEEPOMATIC_STUDIO_API_PREFIX', 'https://studio.deepomatic.com/api')
        if api_key is None:
            api_key = os.getenv('DEEPOMATIC_API_KEY')
            if api_key is None:
                raise Exception("Could not find API key, please set environment variable 'DEEPOMATIC_API_KEY'.")

        # Get the commit ID
        url = 'datasets/{}/commits/'.format(dataset_slug)
        commits = self._request_(url_prefix, url, api_key)
        assert commits['count'] == 1
        commit_id = commits['results'][0]['uuid']

        # Trigger the training
        url = 'datasets/{}/commits/{}/models/train/'.format(dataset_slug, commit_id)
        body = {
            'model_name': model_name,
            'experiment': MessageToDict(self._msg),
        }
        return self._request_(url_prefix, url, api_key, body)

    def _request_(self, url_prefix, url, api_key, body=None):
        url = os.path.join(url_prefix, url)
        headers = {
            'X-API-KEY': api_key
        }
        if body is None:
            r = requests.get(url, headers=headers)
        else:
            r = requests.post(url, json=body, headers=headers)
        if r.status_code == 200:
            return r.json()
        else:
            raise Exception('Invalid status code {} for url {}, response: {}'.format(r.status_code, url, r.text))


serializer.register_all(__name__, experiment_pb2)
