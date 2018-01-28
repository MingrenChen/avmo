import requests
from bs4 import BeautifulSoup
import pymysql
import urllib.parse
import urllib.request
from stem import Signal
from stem.control import Controller
import re
import os


def renew():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)


def myequal(str1, str2):
    def ignore(str):
        return re.search('[a-zA-Z]{2,5}', str).group(0) + "-" + re.search('\d{2,5}', str).group(0)
    if ignore(str1).upper() == ignore(str2).upper():
        return ignore(str1).upper()
    else:
        return None


def try_request(url):
    USER_AGENT_LIST = [
        {"User-Agent":'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7'},
        {"User-Agent": 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0'},
        {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10'}
    ]

    res = requests.get(url, headers=USER_AGENT_LIST[0],
                       proxies={'http': "http://127.0.0.1:8123", 'https': "https://127.0.0.1:8123"})
    while res.status_code != 200:
        print("failed on ", url, "error: ", res.status_code, 'retry.')
        renew()
        res = requests.get(url, headers=USER_AGENT_LIST[0],
                           proxies={'http': "http://127.0.0.1:8123", 'https': "https://127.0.0.1:8123"})
    print("success on", url)
    return res


class Avs(object):
    def __init__(self):
        self.db = pymysql.connect("localhost", "root", "6966xx511", "testDB", charset='utf8mb4', )
        self.cursor = self.db.cursor()
        self.cursor.execute("select id, name, pic from testDB.AV;")
        self.db.commit()
        self.avList = []
        count = 0
        av_list = self.cursor.fetchall()
        for av in av_list:
            count += 1
            print("{} out of {}".format(count, len(av_list)))
            self.downloadMagnet(av[0])
            self.downloadPic(av[0], av[1], av[2])

    def downloadPic(self, id, name, url):
        try:
            path = os.path.join("./picture", id + " " + name + ".jpg")
            urllib.request.urlretrieve(url, path)
            print("download pic", id)
        except OSError:
            path = os.path.join("./picture", id + ".jpg")
            urllib.request.urlretrieve(url, path)
            print("download pic", id)

    def find_magnet(self, url):
        res = try_request(url)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup.find('textarea').getText()

    def downloadMagnet(self, id_):
        url = urllib.parse.urljoin("https://btso.pw/search/", id_)
        res = try_request(url)
        soup = BeautifulSoup(res.text, 'lxml')
        try:
            for link in soup.find_all(class_="data-list")[0].find_all(class_ = "row"):
                if link.find("a", href=True) is None:
                    pass
                else:
                    magnet_page_url = (link.find("a", href=True).get('href'))
                    title = link.find("a", title=True).get('title')
                    try:
                        title_re = re.match("[a-zA-Z]{2,5}-*\d{2,5}", title).group(0)
                        web_re = re.match("[a-zA-Z]{2,5}-*\d{2,5}", title).group(0)
                        id_ = myequal(title_re, web_re)
                        if id_:
                            with open(r"/home/mingren/project/avmo/avmo/picture/" + id_ + ".txt", 'a') as f:
                                mag = self.find_magnet(magnet_page_url)
                                f.write(title + '\n')
                                f.write(mag + '\n')
                                self.cursor.execute(
                                    "ALTER TABLE AV CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;")
                                sql = """UPDATE AV SET magnet = '{}' where id = '{}';
                                                """.format(mag, id_)

                                try:
                                    self.cursor.execute(sql)
                                    self.db.commit()
                                except:
                                    pass
                            f.close()
                            break
                        else:
                            pass
                    except AttributeError:
                        pass
        except IndexError:
            pass




a = Avs()
