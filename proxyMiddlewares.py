import random
import scrapy
import logging
class proxMiddleware(object):
    proxy_list=[
        "http://210.26.54.43:808",
        "http://61.135.217.7:80",
        "http://110.77.88.37:80",
        "http://49.221.196.137:8118",
        "http://119.144.14.211:8118",
        "http://112.111.201.197:8118",
        "http://106.111.132.61:8118",
        "http://139.208.199.207:8118",
        "http://182.43.203.28:4306",
        "http://111.222.33.27:80",
        "http://110.183.244.230:8118",
        "http://124.119.93.192:8118",
        "http://61.167.147.218:80",
        "http://124.164.142.68:80",
        "http://27.22.48.113:808"]
    def process_request(self,request,spider):
        # if not request.meta['proxies']:
        ip = random.choice(self.proxy_list)
        #print 'ip=' %ip
        request.meta['proxy'] = ip
        spider.logger.info('using ip:{}'.format(ip))