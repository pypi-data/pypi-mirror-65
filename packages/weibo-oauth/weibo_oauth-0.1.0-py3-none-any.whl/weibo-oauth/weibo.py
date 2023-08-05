import requests
import logging
import json
import os

# logging.basicConfig(level=logging.INFO)

class Weibo:
    def __init__(self, app_id, app_key, redirect_uri=None):
        super().__init__()
        self.app_id = app_id
        self.app_key = app_key
        self.redirect_uri = redirect_uri
        self.tokenfile = "token.json"
        self.access_token = None
        if redirect_uri is None:
            self.redirect_uri = "https://api.weibo.com/oauth2/default.html"
        self.load_from_file()
        logging.debug("weibo api docs: https://open.weibo.com/wiki/2")

    def get_authorize_url(self):
        path = "oauth2/authorize"
        url = f"https://api.weibo.com/oauth2/authorize?client_id={self.app_id}&redirect_uri={self.redirect_uri}"
        logging.debug(url)
        return url

    def get_access_token(self, code):
        path = ""
        url = f"https://api.weibo.com/oauth2/access_token"
        logging.debug(url)
        data = {
            "redirect_uri": self.redirect_uri,
            "code": code,
            "client_id": self.app_id,
            "client_secret": self.app_key,
            "grant_type": "authorization_code"
        }
        logging.debug(f"api url:{url}\ndata:{data}")
        resp = requests.post(url, data)
        logging.debug(resp.text)

        j = resp.json()
        if resp.status_code == 200:
            self.access_token = j.get("access_token")
            self.remind_in = j.get("remind_in")
            self.expires_in = j.get("expires_in")
            self.uid = j.get("uid")

            with open(self.tokenfile, "w") as f:
                f.write(json.dumps(j))
                logging.debug(f"save token to {self.tokenfile}.. ")
            return self.access_token
        else:
            logging.info(f"authorize fail:{j.message}")
            return None

    def load_from_file(self):
        if os.path.exists(self.tokenfile):
            with open(self.tokenfile, "r") as f:
                j = json.loads(f.read())
                self.access_token = j.get("access_token")
                self.remind_in = j.get("remind_in")
                self.expires_in = j.get("expires_in")
                self.uid = j.get("uid")
                logging.debug(f"load token from {self.tokenfile}..")

    def get_token_info(self):
        pass

    def revoke(self):
        os.remove(self.tokenfile)
        logging.debug(f"delete {self.tokenfile}..")
        resp = requests.get(
            f"https://api.weibo.com/oauth2/revokeoauth2?access_token={self.access_token}")
        if resp.json().get("result") == "true":
            logging.debug("request revoked token..")

    def renew(self):
        logging.debug("凭证续期")
        pass

    def is_expire(self):
        pass

    def get(self, url, **params):
        url = f"https://api.weibo.com/2/{url}.json"
        params["access_token"] = self.access_token
        resp = requests.get(url=url, params=params)
        return resp.json()

    def post(self, url, **data):
        url = f"https://api.weibo.com/2/{url}.json"
        data["access_token"] = self.access_token
        resp = requests.post(url=url, data=data)
        return resp.json()
