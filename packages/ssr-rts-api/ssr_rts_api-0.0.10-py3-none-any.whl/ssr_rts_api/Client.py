import requests
import base64
from urllib import parse


class Client:

    """Client class for requesting the rts ssr api"""
    # todo add data validation

    url = "https://api.srgssr.ch/oauth/v1/accesstoken"
    querystring = {"grant_type": "client_credentials"}

    def __init__(self, obj=None,
                 username=None,
                 password=None,
                 api_url="https://api.srgssr.ch/rts-archives/v3/broadcasts"):

        # todo: enable username & passord params
        self.auth_credentials = self.unpack_credentials_object(**obj)
        self.token = self.request_token()
        self.api_url = api_url
        self.document_count = int()
        self.save_results = ""

    def unpack_credentials_object(self, **kwargs):
        auth_credentials = u"{}:{}".format(kwargs['username'], kwargs['password'])
        base64_credentials = base64.b64encode(auth_credentials.encode("utf-8"))
        return base64_credentials

    def request_token(self):

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Authorization': "Basic {}".format(self.auth_credentials.decode()),
            'Accept': "*/*",
            'Host': "api.srgssr.ch",
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "0",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        response = requests.request("POST", self.url, headers=headers, params=self.querystring)
        if response.status_code == '404':
            print("Erreur: Vérifier nom d'utilisateur et mot de passe")
        else:
            res = response.json()
            token = res["access_token"]
            return token

    def request(self, request_object):

        """
        request data
        don't forget to re indicate the query in the request object
        todo: add exclude field param
        """

        headers = {
            'Authorization': "Bearer {}".format(self.token),
            'User-Agent': "PostmanRuntime/7.19.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "50136156-1af6-4550-8544-e8f23fed5f2a,1aae6b3d-491e-48d8-a20e-d9b8ccd66b3c",
            'Host': "api.srgssr.ch",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        query_obj = request_object
        query_obj['query'] = parse.quote(query_obj['query'])

        response = requests.request("GET", self.api_url, headers=headers, params=query_obj)
        self.document_count = response.json()['meta']['count']
        return response

    def filter_data(self, data, location, value, to_pop=None):

        """
        filter data
        :param: data : data list()
        :param: location : list(), indicates field location in json dataset
        :param: value : str()
        :return: data filtered : json()
        :todo: enable *args with to_pop arg
        """

        filtered = []
        data = data
        res = ''

        for ind, doc in enumerate(data):
            try:
                tmp = doc['program']['id']
                lookup_data = doc
                for k in location:
                    lookup_data = lookup_data[k]
                if lookup_data == value:
                    filtered.append(doc)
            except KeyError:
                pass
        if to_pop:
            try:
                [doc.pop(to_pop) for doc in filtered]
            except KeyError:
                pass

        return filtered

    @classmethod
    def save_data(cls, data_set, mongo_collection, file_name=None):

        """
        save data to a mongodb database or to a file
        :param data_set : array()
        :param mongo_collection : mongodb collection
        :param file_name : str()
        :return Mongodb InsertOneResult or InsertManyResult
        todo: enable file_name option
        """

        if len(data_set) == 1:
            res = mongo_collection.insert_one(data_set[0])
            return res
        else:
            res = mongo_collection.insert_many(data_set)
            return res
