#!/usr/bin/env python
import hashlib
import hmac
import time
import datetime
from anaconda_project.requirements_registry.network_util import urlparse
# import urlparse
import urllib

from bravado.client import SwaggerClient
from bravado.requests_client import RequestsClient
from bravado.requests_client import Authenticator
#from BitMEXAPIKeyAuthenticator import APIKeyAuthenticator
#from offcial-http BitMEXAPIKeyAuthenticator import APIKeyAuthenticator
import json
import pprint
def local2utc(local_st):
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st
class APIKeyAuthenticator(Authenticator):
    """?api_key authenticator.
    This authenticator adds BitMEX API key support via header.
    :param host: Host to authenticate for.
    :param api_key: API key.
    :param api_secret: API secret.
    """

    def __init__(self, host, api_key, api_secret):
        super(APIKeyAuthenticator, self).__init__(host)
        self.api_key = api_key
        self.api_secret = api_secret

    # Forces this to apply to all requests.
    def matches(self, url):
        if "swagger.json" in url:
            return False
        return True

    # Add the proper headers via the `expires` scheme.
    def apply(self, r):
        # 5s grace period in case of clock skew
        expires = int(round(time.time()) + 5)
        r.headers['api-expires'] = str(expires)
        r.headers['api-key'] = self.api_key
        prepared = r.prepare()
        body = prepared.body or ''
        url = prepared.path_url
        # print(json.dumps(r.data,  separators=(',',':')))
        r.headers['api-signature'] = self.generate_signature(self.api_secret, r.method, url, expires, body)
        return r

    # Generates an API signature.
    # A signature is HMAC_SHA256(secret, verb + path + nonce + data), hex encoded.
    # Verb must be uppercased, url is relative, nonce must be an increasing 64-bit integer
    # and the data, if present, must be JSON without whitespace between keys.
    #
    # For example, in psuedocode (and in real code below):
    #
    # verb=POST
    # url=/api/v1/order
    # nonce=1416993995705
    # data={"symbol":"XBTZ14","quantity":1,"price":395.01}
    # signature = HEX(HMAC_SHA256(secret, 'POST/api/v1/order1416993995705{"symbol":"XBTZ14","quantity":1,"price":395.01}'))
    def generate_signature(self, secret, verb, url, nonce, data):
        """Generate a request signature compatible with BitMEX."""
        # Parse the url so we can remove the base and extract just the path.
        parsedURL = urllib.parse.urlparse(url)
        # parsedURL = urlparse.urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query
        # print("verb = "+str(verb))
        # print("path = "+str(path))
        # print("nonce = "+str(nonce))
        # print("data = "+str(data))
        message = bytes(verb + path + str(nonce) + data,'utf-8')
        secret = bytes(secret,'utf-8')
        #message = bytes(verb + path + str(nonce) + data).encode('utf-8')
        # print("Computing HMAC: %s" % message)
        # print("message type = " + str(type(message)))
        # print("secret type = " + str(type(secret)))
        signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()
        return signature

class bitmexclient():
    def __init__(self):
        self.initTradeSide = "Buy"
        HOST = "https://www.bitmex.com"
        SPEC_URI = HOST + "/api/explorer/swagger.json"

        config = {
          'use_models': False,
          'validate_responses': False,
          'also_return_response': True,
        }
        bitMEX = SwaggerClient.from_url(
          SPEC_URI,
          config=config)
        API_KEY = ''
        API_SECRET = ''
        request_client = RequestsClient()
        print("websocket start")
        request_client.authenticator = APIKeyAuthenticator(HOST, API_KEY, API_SECRET)
        self.bitMEXAuthenticated = SwaggerClient.from_url(
          SPEC_URI,
          config=config,
          http_client=request_client)
        print("websocket end")
        # Basic authenticated call
        print('\n---A basic Position GET:---')
        print('The following call requires an API key. If one is not set, it will throw an Unauthorized error.')
        self.avgPrice = 0
        self.pos = 0
    def order(self,count=1,side="Buy"):
        print("order")
        print("count = "+str(count)+" side = "+str(side))
        try:
            res, http_response = self.bitMEXAuthenticated.Order.Order_new(side=side,ordType='Market',symbol='XBTUSD', orderQty=count).result()
            print(res)
        except Exception as aa:
            print(aa)
    def orderauto(self,count=1):
        print("orderauto")
        side = "Buy"
        if self.pos==0:
            side = self.initTradeSide
        else:
            Buy = "Buy"
            Sell = "Sell"
            if self.pos>0:
                side=Buy
            elif self.pos<0:
                side = Sell
        print("side = "+side)
        self.order(count,side)

    def orderClose(self):
        print("orderClose")
        try:
            res, http_response = self.bitMEXAuthenticated.Order.Order_new(ordType='Market',symbol='XBTUSD',execInst="Close").result()
            print(res)
        except Exception:
            print(Exception)
        self.getpos()

    def getpos(self):
        try:
            res, http_response = self.bitMEXAuthenticated.Position.Position_get().result()
            print("res-------------------", res)
            if res == None:
                self.avgPrice = 0
                return 0
            if len(res)==0:
                self.avgPrice = 0
                return 0
            self.avgPrice = res[0]["avgCostPrice"]
            return res[0]["currentQty"]
        except Exception as e:
            print("res===============================")
            print("exception-----------------", e.__context__)
            print("exception-----------------", e.__cause__)
            #return self.getpos()
    def getKline(self):
        tt = datetime.datetime.now()-datetime.timedelta(minutes=10)
        utctime = local2utc(tt)
        print("utctime = "+str(utctime))
        res, http_response = self.bitMEXAuthenticated.Trade.Trade_getBucketed(binSize='1m',partial=False,symbol='XBTUSD', count=3,startTime=utctime).result()
        print(res)
# bc = bitmexclient()
# bc.getKline()

