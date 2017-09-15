import re, pickle
import json,os
from PIL import Image
import urllib.request
import os.path
import urllib.parse
from scrapy.cmdline import execute
import pymysql

class Av_Queue:
    def __init__(self):
        self.dict = []
        self.minmax = None
        self.photos = os.listdir(r"/home/mingren/project/avmo/avmo/picture/")

    def append(self, singleAv):
        if type(singleAv) == Av:
            if single_av not in self.dict:
                self.dict.append(singleAv)
        else:
            pass

    def checkin(self, Av):
        if (Av.id_ + ".jpg" in self.photos) or (Av.id_ + " " + Av.name + ".jpg" in self.photos):
            return True
        return False

    def checkmax(self, string):
        if not self.minmax:
            self.minmax = len(string)
        elif self.minmax > len(string):
            self.minmax = len(string)

    def findSimilar(self):
        def check(name1, name2):
            c1 = re.search("[a-zA-Z]{2,5}-\d{2,4}", name1).group(0)
            c2 = re.search("[a-zA-Z]{2,5}-\d{2,4}", name2).group(0)
            if c1 == c2:
                return True
            else:
                return False
        j = 0
        while j < len(self.photos):
            i = j + 1
            while i < len(self.photos):
                if check(self.photos[j],self.photos[i]):
                    print(self.photos[j], " and ", self.photos[i])
                i += 1
            j += 1


    def download(self):
        i = 0
        db = pymysql.connect("localhost", "root", "6966xx511", "testDB", charset='utf8mb4', )
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS AV")

        sql = """CREATE TABLE AV (
                         ID  VARCHAR(255) NOT NULL,
                         name  VARCHAR(255),
                         url  VARCHAR(255),
                         IMAGE  VARCHAR(255));"""
        cursor.execute(sql)
        cursor.execute("ALTER TABLE AV CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;")
        for av_ in self.dict:
            av_.download_pic(cursor)
            i += 1
            print("已下载{}张，还差{}张。".format(i, len(self.dict) - i))

    def create_url_book(self):
        with open("./spiders/urls.txt", "w") as d:
            for av_ in self.dict:
                d.write(urllib.parse.urljoin("https://btso.pw/search/", av_.id_))
                d.write("\n")
        d.close()

    def add_to_db(self):
        db = pymysql.connect("localhost", "root", "6966xx511", "testDB", charset='utf8mb4',)
        cursor = db.cursor()
        cursor.execute("DROP TABLE IF EXISTS AV")

        sql = """CREATE TABLE AV (
                 ID  VARCHAR(255) NOT NULL,
                 name  VARCHAR(255),
                 url  VARCHAR(255),
                 IMAGE  VARCHAR(255));"""

        cursor.execute(sql)
        cursor.execute("ALTER TABLE AV CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;")

        for single_av in self.dict:
            single_av.add_to_db(cursor)
        db.commit()
        db.close()

    def change_path(self):
        for av in self.dict:
            av.downpic = os.path.join(os.path.dirname(os.path.abspath(__file__)), av.downpic[1:])

class Av:
    def __init__(self, name, id_, url, pic, avq):
        self.avq = avq
        self.name = name
        self.id_ = id_
        self.url = url
        self.pic = pic
        self.mag = None
        self.downpic = None

    def download_pic(self):
        try:
            path = os.path.join("./picture", self.id_ + " " + self.name + ".jpg")
            urllib.request.urlretrieve(self.pic, path)
            self.downpic = path
        except OSError:
            path = os.path.join("./picture", self.id_ + ".jpg")
            urllib.request.urlretrieve(self.pic, path)
            self.downpic = path

    def __repr__(self):
        return self.id_

    def __hash__(self):
        return hash(self.id_)

    def add_to_db(self, cursor):
        sql = """INSERT INTO AV(ID,name,url,IMAGE)
                          VALUES ('{}','{}','{}','{}');""".format(self.id_, self.name, self.url, self.downpic)
        cursor.execute(sql)


if __name__ == "__main__":
    # execute(['scrapy', 'crawl', 'javlibrary'])
    with open("avmo.json") as data_file:
        all_av = data_file.readline()
        pattern = re.compile("{.+?}")
        all_ = Av_Queue()

        for i in re.findall(pattern, all_av):
            single_av = json.loads(i)
            av = Av(single_av['name'], single_av['id_'], single_av['url'], single_av['pic'], all_)
            all_.append(av)
    # print(all_.photos)
    all_.add_to_db()
    # all_.download()
    # b = open('save.p', 'wb')
    # pickle.dump(all_, b)
    # c = pickle.load(open('save.p','rb'))
    # c.change_path()
    # c.add_to_db()
    # all_.findSimilar()
    # execute(['scrapy', 'crawl', 'btso'])
    # with open("avmo.pickle","wb") as p:
    #     pickle.dump(all_, p)
    # p.close()
    # data_file.close()
    #
    # with open("avmo.pickle","rb") as p:
    #     avs = pickle.load(p)
    # avs.create_url_book()
    # p.close()
    #