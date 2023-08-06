from .mailchimp import MailChimp


class Integration:
    def __init__(self, api_key: str = None, api_key_type: str = 'Bearer'):
        self.api_key = api_key
        self.api_key_type = api_key_type

    @property
    def mailchimp(self):
        return MailChimp(api_key=self.api_key, api_key_type=self.api_key_type)
