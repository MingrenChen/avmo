# coding:utf-8

import requests
from bs4 import BeautifulSoup as bf
import threading
import queue


class Get_ips:
    def __init__(self,page):
        self.ips=[]
        self.urls=[]
        # for i in range(3):
        self.urls.append("https://free-proxy-list.net/")
        self.header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'}
        #self.file=open("ips",'w')
        self.q=queue.Queue()
        self.Lock=threading.Lock()

    def get_ips(self):
        with open("list.txt", "w") as l:
            res = requests.get(self.urls[0], headers=self.header)
            soup = bf(res.text, 'lxml')
            a = soup.find_all('tbody')[0].find_all('tr')
            # count = 0
            for element in a:
                # if count < 30:
                    ips = element.find_all('td')
                    ip_temp = "https://" + ips[0].contents[0] + ":" + ips[1].contents[0]
                    self.q.put(str(ip_temp))
                    l.write(ip_temp)
                    l.write("\n")
                    # count += 1
        l.close()



    # def review_ips(self):
    #     i = 10
    #     while i>0:
    #         ip=self.q.get()
    #         try:
    #             print(123123)
    #             proxy={"https": ip}
    #             #print proxy
    #             res = requests.get("https://btso.pw/", proxies=proxy,timeout=5)
    #             self.Lock.acquire()
    #             if res.status_code == 200:
    #                 print('succcess: ',ip)
    #                 # self.ips.append(ip)
    #                 # with open("list.txt", "a") as l:
    #                 #     l.write(ip)
    #                 #     l.write("\n")
    #                 # l.close()
    #                 # print(ip)
    #                 # i-=1
    #                 # self.Lock.release()
    #         except Exception as e:
    #             print('failed: ', e)
    # def main(self):
    #     self.get_ips()
    #     threads=[]
    #     for i in range(40):
    #         # pass
    #         threads.append(threading.Thread(target=self.review_ips,args=[]))
    #     for t in threads:
    #         t.start()
    #     for t in threads:
    #         t.join()
    #     return self.ips

def get_ip():
    my=Get_ips(4)

    return my.get_ips()

a = get_ip()
