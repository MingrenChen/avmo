import re
import json

if __name__ == "__main__":
    with open("avmo.json") as data_file:
        all_av = data_file.readline()
        # print(type(a))
        pattern = re.compile("{.+?}")
        all_ = []
        for i in re.findall(pattern, all_av):
            all_.append(json.loads(i))

        # print(all_)
        print(type(all_[0]))
        # data = json.load(data_file)
    # print(data)
