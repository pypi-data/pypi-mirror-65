from .core import models, synchable_models
from .integrations import Integration
from .videos import Video

__all__ = [
    'models',
    'synchable_models',
    'Congressy',
]


class Congressy:
    def __init__(self, api_key: str = None, api_key_type: str = 'Bearer'):
        self.api_key = api_key
        self.api_key_type = api_key_type

    @property
    def video(self):
        return Video(api_key=self.api_key, api_key_type=self.api_key_type)

    @property
    def integration(self):
        return Integration(api_key=self.api_key,
                           api_key_type=self.api_key_type)
