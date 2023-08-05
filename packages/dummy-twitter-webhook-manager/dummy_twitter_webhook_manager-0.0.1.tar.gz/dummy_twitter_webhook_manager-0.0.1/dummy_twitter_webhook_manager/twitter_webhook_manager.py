import json
from tweepy.error import TweepError
from tweepy import OAuthHandler
import requests

class WebhooksManager:
    _protocol = "https:/"
    _host = "api.twitter.com"
    _version = "1.1"
    _product = "account_activity"

    def __init__(self, token_file=None, tokens_dict=None):
        if (token_file is not None) and (tokens_dict is not None):
            raise Exception('You can pass the tokens as json file or dictionary but not both together')

        elif token_file:
            with open(token_file) as f:
                twitter_tokens = json.load(f)

        elif tokens_dict:
            twitter_tokens = tokens_dict

        else:
            raise Exception('You have to pass the tokens as json file or dictionary')

        self._consumer_key = twitter_tokens['consumer_key']
        self._consumer_secret = twitter_tokens['consumer_secret']
        self._access_token = twitter_tokens['access_token']
        self._access_token_secret = twitter_tokens['access_token_secret']
        self._env_name = twitter_tokens['env_name']

        self._auth = OAuthHandler(
            bytes(self._consumer_key, 'ascii'), bytes(self._consumer_secret, 'ascii')
        )

        self._auth.set_access_token(
            bytes(self._access_token, 'ascii'), bytes(self._access_token_secret, 'ascii')
        )

    def api(self, method: str, endpoint: str, data: dict = None):
        """
        :param method: GET or POST
        :param endpoint: API Endpoint to be specified by user
        :param data: POST Request payload parameter
        :return: json
        """
        try:
            with requests.Session() as r:
                response = r.request(
                    url="/".join(
                        [
                            self._protocol,
                            self._host,
                            self._version,
                            self._product,
                            endpoint,
                        ]
                    ),
                    method=method,
                    auth=self._auth.apply_auth(),
                    data=data,
                )
                return response
        except TweepError:
            raise

    def register_webhook(self, callback_url: str):
        try:
            return self.api(
                method="POST",
                endpoint=f"all/{self._env_name}/webhooks.json",
                data={"url": callback_url},
            )
        except Exception:
            raise

    # Get all webhooks we have
    def get_webhooks(self):
        return self.api(
            method="GET",
            endpoint=f"all/webhooks.json",
        ).json()

    # Delete webhook by id
    def delete_webhook(self, id_):
        del_ = self.api(
            method="DELETE",
            endpoint=f"all/{self._env_name}/webhooks/{id_}.json",
        )

        return str(del_)

    def subscribe(self):
        try:
            return self.api(
                method="POST",
                endpoint=f"all/{self._env_name}/subscriptions.json",
            )
        except Exception:
            raise