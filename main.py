import re, pickle
import json
import urllib.request
import os.path


class Av_Queue:
    def __init__(self):
        self.set = set()
        self.minmax = None

    def append(self, singleAv):
        if type(singleAv) == Av:
            self.set.add(singleAv)
        else:
            pass

    def checkmax(self,string):
        if not self.minmax:
            self.minmax = len(string)
        elif self.minmax > len(string):
            self.minmax = len(string)

    def download(self):
        for av_ in self.set:
            av_.download_pic(self)


class Av:
    def __init__(self, name, id_, url, pic):
        self.name = name
        self.id_ = id_
        self.url = url
        self.pic = pic

    def download_pic(self, Avqueue):
        try:
            urllib.request.urlretrieve(self.pic, os.path.join("./img", self.id_ + " " + self.name + ".jpg"))
        except OSError:
            Avqueue.checkmax(self.id_ + " " + self.name + ".jpg")
            urllib.request.urlretrieve(self.pic, os.path.join("./img", self.id_ + ".jpg"))

    def __repr__(self):
        return self.id_

    def __hash__(self):
        return hash(self.__repr__())

if __name__ == "__main__":
    with open("avmo.json") as data_file:
        all_av = data_file.readline()
        pattern = re.compile("{.+?}")
        all_ = Av_Queue()
        for i in re.findall(pattern, all_av):
            single_av = json.loads(i)
            av = Av(single_av['name'], single_av['id_'], single_av['url'], single_av['pic'])
            all_.append(av)
        all_.download()


    with open("avmo.pickle","wb") as p:
        pickle.dump(all_, p)
    p.close()
    data_file.close()
    print(all_.minmax)
