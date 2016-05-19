# -*- coding: utf-8 -*-
import os
import multiprocessing
from snownlp import SnowNLP

import sys

reload(sys)
sys.setdefaultencoding("utf-8")


class Counter:
    counter = 0
    total = 0

    def __init__(self):
        pass


def create_file(save_path, filename):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename
    open(path, "w+").close()


def string_list_save(save_path, filename, slist):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path + "/" + filename
    with open(path, "a+") as fp:
        for s in slist:
            fp.write("%s\t%s\n" % (s[0].encode('utf8'), s[1]))
        del slist[:]
    fp.close()


def estimate_sentiment(save_path, read_path, filename):
    # print "estimating sentiment for " + filename
    create_file(save_path, filename)
    fileHandle = open(read_path + "/" + filename)
    results = []
    newsinfo = fileHandle.readline()
    while len(newsinfo) <> 0:
        newstile = newsinfo.split("\t")[0]
        results.append([newstile, SnowNLP(newstile.decode('utf8')).corporate_sentiments])
        newsinfo = fileHandle.readline()
    fileHandle.close()
    string_list_save(save_path, filename, results)
    Counter.counter += 1
    os.system("clear")
    print str(Counter.counter) + " / " + str(Counter.total)


def sentimental_experiment(read_path, save_path):
    processing = []
    Counter.total = len(os.listdir(read_path)) - 1
    for filename in os.listdir(read_path):
        if filename == ".DS_Store":
            continue
        # processing.append(multiprocessing.Process(target=estimate_sentiment,
        #                                     args=(save_path, read_path, filename)))
        estimate_sentiment(save_path, read_path, filename)

    # for pro in processing:
    #     pro.daemon = True
    #     pro.start()
    #
    # for pro in processing:
    #     pro.join()

    print "Done!\ntell YRZ if there's something wrong."


if __name__ == '__main__':
    _read_path_ = u"News Collection"
    _save_path_ = u"Sentimental Experiment"
    sentimental_experiment(_read_path_, _save_path_)
