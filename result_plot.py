# -*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import csv
import math
import MySQLdb
import numpy as np
import copy

def trans(res, rd):
    resout = copy.deepcopy(res)
    resout[1] = res[1] * math.cos(rd) - res[2] * math.sin(rd)
    resout[2] = res[2] * math.cos(rd) + res[1] * math.sin(rd)
    resout[1] += 4.36
    resout[2] -= 1.7
    return resout
def trans1(res, rd):
    resout = copy.deepcopy(res)
    resout[1] = res[1] * math.cos(rd) - res[2] * math.sin(rd)
    resout[2] = res[2] * math.cos(rd) + res[1] * math.sin(rd)
    resout[1] += 4.25
    resout[2] -= 1.6
    return resout

def loadCsv(filename):
    f = open(filename, 'r')
    lines = csv.reader(f)
    dataset = list(lines)
    dataset1 = []
    for i in range(1,len(dataset)):
        dataset1.append([])
        try:
            for j in range(4):
                if j == 0:
                    dataset1[i-1].append(int(dataset[i][j])/(10**6))
                else:
                    dataset1[i-1].append(float(dataset[i][j]))
        except ValueError, e:
            print "ValueError at %d" % i
    f.close()
    return dataset1


def loadTxt(filename):
    dataset = []
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        dataset.append(line.split("\t"))
    for i in range(len(dataset)):
        try:
            for j in range(len(dataset[i])):
                if j == 0:
                    dataset[i][j] = int(float(dataset[i][j])*(10**3))
                else:
                    dataset[i][j] = float(dataset[i][j])
        except ValueError, e:
            print "ValueError at %d" % i
    f.close()
    return dataset
def loadTxt1(filename):
    dataset = []
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        dataset.append(line.split("\t"))
    for i in range(len(dataset)):
        try:
            for j in range(len(dataset[i])):
                if j == 0:
                    dataset[i][j] = int(float(dataset[i][j])/(10**6))
                else:
                    dataset[i][j] = float(dataset[i][j])
        except ValueError, e:
            print "ValueError at %d" % i
    f.close()
    return dataset

class mydataplot(object):
    def __init__(self, dbname):
        self.con = MySQLdb.connect(host='localhost',user='rsoot',passwd='23143425',db=dbname)
        self.cur = self.con.cursor()
    def __del__(self):
        self.dbcommit()
        self.cur.close()
        self.con.close()

    def readdata(self, file1, file2, table1, table2, rd):
        res1 = loadCsv(file1)
        res2 = loadTxt(file2)
        for i in range(1, len(res1)):

            self.insertdata(table1, res1[i])
        for i in range(1, len(res2)):
            res2[i] = trans(res2[i], rd)
            self.insertdata(table2, res2[i])
        self.dbcommit()
    def createtable(self, tablename):
        self.cur.execute("create tpython  rosbagable if not exists %s (timestamp bigint, x float, y float, z float)" % tablename)
        self.dbcommit()

    def insertdata(self, tablename, data):
        self.cur.execute("insert into %s (timestamp, x, y, z) values (%d, %f, %f, %f)" % (tablename, data[0], data[1], data[2], data[3]))

    def getdelta(self):
        self.cur.execute("select (d3_res1.x-d3_res2.x), (d3_res1.y- d3_res2.y), (d3_res1.z- d3_res2.z)  from d3_res1, d3_res2 where d3_res1.timestamp=d3_res2.timestamp")
        result = self.cur.fetchall()
        return result

    def dbcommit(self):
        self.con.commit()
    def getdata(self, tablename):
        self.cur.execute("select * from %s" % tablename)
        result = self.cur.fetchall()
        return result


def computederlta(res1, res2):
    deltax = []
    deltay = []
    deltaz = []
    l1 = len(res1)
    l2 = len(res2)
    i = 0
    j = 0

    while i < l1-1 and j < l2-1:
        try:
            while res2[j][0] < res1[i][0]:
                    j += 1
            while res2[j][0] > res1[i][0]:
                    i += 1
            if res2[j][0] == res1[i][0]:
                deltax.append(res1[i][1] - res2[j][1])
                deltay.append(res1[i][2] - res2[j][2])
                deltaz.append(res1[i][3] - res2[j][3])
            i += 1
            j += 1
        except:
            print i,j
    return (deltax, deltay, deltaz )









def deltaplot():
    md = mydataplot("okvisdata")



    # createtable(cur, "rpython  rosbages1")
    # createtable(cur, "res2")
    # readdata("/home/lyw/data.csv", "/home/lyw/predict.txt", cur, con)
    result = md.getdelta()
    # delta = ([], [], [])
    # for i in range(len(result)):
    #     delta[0].append(result[i][0] - 4.7)
    #     delta[1].append(result[i][1] + 1.8)
    #     delta[2].append(result[i][2] - 0.92)
    resmat = np.mat(result)

    plt.figure(figsize=(10,10))
    plt.plot(range(len(result)), resmat[0, :])
    plt.plot(range(len(result)), resmat[1, :])
    plt.plot(range(len(result)), resmat[2, :])
    plt.legend()
    plt.show()

def compareplot():
    # rd = -0.176
    # md = mydataplot("okvisdata")
    # md.createtable("d3_res1")
    # md.createtable("d3_res2")
    # md.readdata("compare3/data.csv", "compare3/predict.txt","d3_res1", "d3_res2",rd)
    rd  = -2.3
    rd1 = -2.35
    # md = mydataplot("okvisdata")
    # res1 = md.getdata("d3_res1")
    # res2 = md.getdata("d3_res2")
    res1 = loadCsv("compare5/data.csv")
    res2 = loadTxt("compare5/predict.txt")
    res3 = loadTxt1("rovio_result.txt")



    for i in range(0, len(res2)):
        res2[i] = trans(res2[i], rd)

    for i in range(0, len(res3)):
        res3[i] = trans1(res3[i], rd1)
    # rovio_delta = computederlta(res1, res3)
    okvis_delta = computederlta(res1, res2)
    plt.figure(figsize=(10,10))
    # plt.plot(range(len(okvis_delta[0])), okvis_delta[0], label="rovio_x")

    # plt.plot(range(len(rovio_delta[0])), rovio_delta[0], label="rovio_x")
    # plt.plot(range(len(rovio_delta[0])), rovio_delta[1], label="rovio_y")
    # plt.plot(range(len(rovio_delta[0])), rovio_delta[2], label="rovio_z")
    plt.plot(range(len(okvis_delta[0])), okvis_delta[0], label="okvis_x")
    plt.plot(range(len(okvis_delta[0])), okvis_delta[1], label="okvis_y")
    plt.plot(range(len(okvis_delta[0])), okvis_delta[2], label="okvis_z")
    plt.xlabel("timestamp(s)")
    plt.ylabel("delta(m)")
    plt.title("error")
    plt.legend()
    plt.show()
def plottraj():
    rd  = -2.3
    rd1 = -2.35
    # md = mydataplot("okvisdata")
    # res1 = md.getdata("d3_res1")
    # res2 = md.getdata("d3_res2")
    res1 = loadCsv("compare5/data.csv")
    res2 = loadTxt("compare5/predict.txt")
    res3 = loadTxt1("rovio_result.txt")

    resmat1 = np.mat(res1)

    for i in range(0, len(res2)):
        res2[i] = trans(res2[i], rd)

    for i in range(0, len(res3)):
        res3[i] = trans1(res3[i], rd1)
    resmat3 = np.mat(res3)
    resmat2 = np.mat(res2)
    plt.figure(figsize=(10,10))
    plt.plot(resmat1[:, 1], resmat1[:, 2], label="groundtruth")
    plt.plot(resmat2[:, 1], resmat2[:, 2], label="okvis")
    plt.plot(resmat3[:, 1], resmat3[:, 2], label="rovio")
    plt.title("raw trajectory")
    plt.xlabel("x(m)")
    plt.ylabel("y(m)")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    compareplot()
    # plottraj()
    pass

