import json


class TokenCache:

    def __init__(self):
        self.data = []

    def contains(self, user_id):
        cached_token = [cached_token for cached_token in self.data if cached_token['user_id'] == user_id]
        return len(cached_token) > 0

    def get(self, user_id):
        cached_token = [cached_token for cached_token in self.data if cached_token['user_id'] == user_id]
        return cached_token[0]

    def set(self, user_id, refresh_token):
        cached_token = [cached_token for cached_token in self.data if cached_token['user_id'] == user_id]
        if len(cached_token) == 0:
            cached_token = {
                "user_id": user_id,
                "refresh_token": refresh_token,
            }
            print "create a new cache:"
            print json.dumps(cached_token, indent=4)
            self.data.append(cached_token)
        else:
            cached_token[0]["refresh_token"] = refresh_token
            print "update an existing cache:"
            print json.dumps(cached_token[0], indent=4)
