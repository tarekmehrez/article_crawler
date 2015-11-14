import base64
import random
import pprint

from settings import USER_AGENT_LIST
from settings import PROXIES
from scrapy import log


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        #pprint.pprint(proxy)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            #pprint.pprint(request)            
        else:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            #print " no user pass " + request
        # uncommeitnng return, keeps in infinte loop
        # return request


class RandomUserAgentMiddleware(object):    
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        #log.msg('>>>> UA %s'%request.headers)
